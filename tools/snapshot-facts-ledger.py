#!/usr/bin/env python3
"""Snapshot the master facts ledger into an episode's dm/ folder.

Usage: snapshot-facts-ledger.py <episode-dir> <N> "<what is new, one paragraph>"

Copies design/DM-ONLY/facts-ledger.md to <episode-dir>/dm/continuity-through-ep-N.md,
rewrites every relative link so it still points at the same file from the new
location, and replaces the master's banner with a snapshot banner.

Why this is a tool and not a sed line: the old procedure was a hand-typed sed list
that only knew five file names. Any link to a file not on the list broke silently,
and nothing checked. This rewrites links by resolving them, then REFUSES to write
the snapshot if any link that resolved in the master no longer resolves.
"""
import os
import re
import sys

LINK = re.compile(r'(\]\(|`)((?:\.\./|\./)?[A-Za-z0-9_\-./]+\.(?:md|json|html))(#[^)`\s]*)?([)`])')


# Deliberately broader than LINK: anything that looks like a relative markdown link
# target. If LINK misses a form, the link stays unrewritten and this count drops.
CHECK = re.compile(r'\]\(([^)\s#]+)|`([^`\s]+\.(?:md|json|html))`')


def resolvable(text, base):
    found = set()
    for m in CHECK.finditer(text):
        path = m.group(1) or m.group(2)
        if path.startswith(('http', '/', '#', 'mailto:')):
            continue
        target = os.path.normpath(os.path.join(base, path))
        if os.path.exists(target):
            found.add(target)
    return found


def rewrite(text, src_dir, dst_dir, repo_root):
    def fix(m):
        opener, path, frag, closer = m.group(1), m.group(2), m.group(3) or '', m.group(4)
        if path.startswith(('http', '/')):
            return m.group(0)
        old_abs = os.path.normpath(os.path.join(src_dir, path))
        if not old_abs.startswith(repo_root) or not os.path.exists(old_abs):
            return m.group(0)  # not a link that resolved in the master; leave it alone
        return f'{opener}{os.path.relpath(old_abs, dst_dir)}{frag}{closer}'

    return LINK.sub(fix, text)


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    ep_dir, n, whats_new = sys.argv[1], sys.argv[2], sys.argv[3]
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    master = os.path.join(repo_root, 'design', 'DM-ONLY', 'facts-ledger.md')
    dst_dir = os.path.abspath(os.path.join(ep_dir, 'dm'))
    if not os.path.isdir(dst_dir):
        sys.exit(f'refusing: {dst_dir} does not exist')
    text = open(master, encoding='utf-8').read()
    body = rewrite(text, os.path.dirname(master), dst_dir, repo_root)
    before = resolvable(text, os.path.dirname(master))
    after = resolvable(body, dst_dir)
    lost = before - after
    if lost:
        sys.exit('refusing: these files were linked from the master but the snapshot no '
                 'longer reaches them:\n  ' + '\n  '.join(sorted(os.path.relpath(x, repo_root) for x in lost)))
    master_rel = os.path.relpath(master, dst_dir)
    banner = (
        '> [!CAUTION]\n'
        '> **DM-ONLY — CAMPAIGN + FUTURE-EPISODE SPOILERS**\n'
        '>\n'
        f'> **Snapshot of the cross-campaign facts ledger as of Ep {n} prep.** The canonical '
        f'version lives at [`{master_rel}`]({master_rel}); this snapshot exists for the '
        "DM's binder and print bundle. **Do not edit this copy — edit the master and re-snapshot.**\n"
        '>\n'
        f'> **What is new since the last snapshot:** {whats_new}\n'
        '>\n'
        '> **Source uses `{{pc:N}}` template variables** per public-repo hygiene.\n\n'
    )
    out = os.path.join(dst_dir, f'continuity-through-ep-{n}.md')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(banner + body)
    print(f'wrote {os.path.relpath(out, repo_root)}')


if __name__ == '__main__':
    main()
