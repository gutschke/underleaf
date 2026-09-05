#!/usr/bin/env python3
"""Ep 6 prop set — "The Duck Has You".

Produces one print-ready PDF: a two-page rules sheet, then ten pages of cards,
ten to a page, cut along the dashes. Components at the table are the cards, a
rubber duck, five blank slips and a pen. Nothing else — the board, the meeples
and the dice were all cut after playtesting.

Decks: CALLER 12 (one set aside for round four) · ROSA 4 (fixed order, never
shuffled) · BONUS 6 · ROUND 24 (five per PC, in order; slot 2 has four because
her fifth is GM-held) · QUESTION 20 · WHO HAS THE DUCK 7 · ALAIA 3 + WINNIE 3 ·
ADOPTED 10 · GM ONLY 3.

PCs are written as {{pc:N}} throughout, per the repo convention. Run it with no
arguments and the cards print the tokens, which is what you want if you are
adapting this for your own table. Pass --map to substitute real names:

    ./make-dance-game.py --map party-mapping.json --out dance-game.pdf

The map is {"slots": {"1": {"pc": "Firstname"}, ...}} and is yours to keep
private; it is deliberately not in this repository.

Requires a Chrome or Chromium on PATH for the HTML-to-PDF step.
"""
import argparse, json, pathlib, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent

ap = argparse.ArgumentParser(description="Build the Ep 6 dance-game prop PDF.")
ap.add_argument("--map", type=pathlib.Path, default=None,
                help="JSON slot->PC-name map; without it the cards keep {{pc:N}} tokens")
ap.add_argument("--out", type=pathlib.Path, default=HERE / "dance-game.pdf",
                help="output PDF (default: dance-game.pdf beside this script)")
ap.add_argument("--keep-html", action="store_true",
                help="leave the intermediate HTML next to the PDF instead of a temp file")
args = ap.parse_args()

if args.map:
    SLOTS = json.loads(args.map.read_text())["slots"]
    PC = {i: SLOTS[str(i)]["pc"] for i in range(1, 6)}
else:
    PC = {i: "{{pc:%d}}" % i for i in range(1, 6)}

PCS = [(i, PC[i]) for i in range(1, 6)]

CALLS = [
    ("Long lines forward and back!", "", ""),
    ("Neighbour swing — give weight!", "", ""),
    ("Right hand star, all the way round!", "", ""),
    ("Do-si-do your neighbour — don't touch, just go round —", "", ""),
    ("Circle left, three places — and back the other way!", "", ""),
    ("Balance the ring — and everybody swing!", "", ""),
    ("Gents — sorry — LARKS, allemande left once and a half!", "", ""),
    ("That's the dance! Let's try it with music — band, when you're ready!", "", ""),
    ("New neighbours! Find your new neighbours!", "", ""),
    ("You're on your own now.",
     "ROUND 4 &middot; ALWAYS &middot; THE CALLER STOPS",
     "<b>Set this aside and play it as the round-four call, every time.</b> The room keeps dancing in silence, correctly. <b>No shout.</b> Whoever has the duck asks their <b>own</b> question &mdash; and finally gets a straight answer to it."),
    ("Down the hall four in line, turn as a couple, come on back!",
     "TWO OF YOU",
     "Draw <b>one</b> duck card as usual &mdash; then <b>the player on their left shares it.</b> The two of them get <b>one sentence between them</b> and have to agree on it out loud, in front of everybody. <b>Only the drawn card is set aside.</b> If it is SHE GOES PAST, run the pass as normal &mdash; the twist is spent."),
    ("Larks and robins, allemande left!",
     "NO TIME",
     "The shout happens in <b>one word each</b>. Nothing longer. Whoever has the duck builds a sentence out of the four words shouted at them."),
]

# Drawn IN ORDER on a successful reach, rounds one to four. These are the
# load-bearing lines. Two more are GM-held and never enter this deck: "I've
# never met anyone else who does it" (after the stumble) and "No, it lives at
# the house" (as the band takes a break).
ANSWERS = [
    "My mother kept notebooks her whole life. I never asked her why. Mine's not the same thing — mine was already started when I got it.",
    "The handwriting at the front isn't mine. I can show you where mine starts.",
    "I don't know who stopped.",
    # "I've never met anyone else who does it." is NOT here. It is a GM card,
    # held all morning and played in the hush straight after the stumble.
    "Some of it I wrote because I saw it. Some of it I wrote because I couldn't not. I've never been able to tell you which was which — not from the inside.",
    # ROSA 6 is NOT in the round deck. It is the exit line, said as the band
    # takes a break: "No, it lives at the house. It's not the library's."
]

# SHUFFLED. Drawn when she sails past somebody, or on a 7-9. Texture, and it
# means a player whose meeple is down still gets something out of the round.
ASIDES = [
    "1979. I was working the backlog — boxes nobody had opened since the war.",
    "It wasn't catalogued as anything. It was in with a lot of estate paper.",
    "Vivian and I have talked at Christmas for sixty-five years. We've met once. I was three.",
    "She rang about you. She didn't say what it was about — she never does.",
    "My mother thought the birds knew. I never got anything useful out of that.",
    "I used to bring my daughter to this when she was small. She hated it.",
]

# Each PC's five. Roughly half are quirky texture and half are DO A THING cards
# that move the plot -- and the plot ones mostly get their answer from the ROOM,
# not from Rosa. Forty people have known her for decades. Mixed deliberately, so
# a player cannot tell which kind is coming.
# Each PC's five run IN ORDER, rounds one to five, and they are a small arc with
# a named partner rather than five unrelated one-liners: setup, complication,
# payoff. Green PLOT cards are a specific action with a specific result, and
# most of them get their answer from the room rather than from Rosa.
ROUNDS = {
 1: [
  "DEL, the caller — 70, hoarse, dry — is losing his microphone mid-sentence. He looks at the room. Nobody moves. <b>You are the only person here who could fix it.</b>",
  "You have it working. Del does not thank you; he just starts using it, which is better. <b>You are now standing at the table where Rosa left her bag.</b>",
  "PLOT — Rosa's little black planner is out by the bag. One page a day, post-it notes stuck three deep, pages torn out for scrap. <b>Look at it properly.</b>",
  "PLOT — <b>Ask Del how long Rosa has been coming.</b> He answers without having to think: <i>&ldquo;Since 1996. Longer than we've had the piano.&rdquo;</i> <b>Write it on a slip and push it to the middle.</b>",
  "Del, at the end, not looking at you: <i>&ldquo;You'll be here next week, then.&rdquo;</i>",
 ],
 2: [
  "HECTOR is 78 and doing something with his left knee that you would write up. <b>You open your mouth to say so &mdash; and stop yourself.</b> Tell us what you were about to say, and that you did not say it.",
  "He out-dances two men half his age, comes off the floor, catches you watching, and says: <i>&ldquo;It only does that going left. Forty years. I've made my peace.&rdquo;</i>",
  "A woman hands you her rings and walks off. Find somewhere on your body to put them.",
  "PLOT — Hector has decided he likes you. <b>Ask him what Rosa is like.</b> He thinks about it properly: <i>&ldquo;She's always half a step ahead of the music. Forty years I've watched her do it. Never worked out how she knows.&rdquo;</i>",
  # Round 5 is the stumble. It is a GM card, held all morning, and is NOT dealt.
 ],
 3: [
  "PLOT — The sign-in binder is in four different hands and nobody has ever filed it. <b>Go back through it.</b> The book starts in 1996 &mdash; and <b>Rosa's name is in every single year of it.</b> <b>Write it on a slip and push it to the middle.</b>",
  "JOYCE sits down next to you. <b>She has been meaning to sort that binder since 1998 and has never once started.</b> She talks the entire time and she is a delight.",
  "PLOT — Joyce points at the photo board by the door. <b>Find Rosa in the oldest ones.</b> 1997, the second year this ever ran &mdash; much younger, at the edge of the group, and under one arm <b>a book you have seen on her kitchen table.</b> <b>Write it on a slip and push it to the middle.</b>",
  "A receipt from 1996. Same coffee urn. Joyce is thrilled you found it.",
  "Joyce, seriously: <i>&ldquo;Do you do this professionally? Because we'd have you.&rdquo;</i>",
 ],
 4: [
  "WINNIE, 75, looks you up and down and announces to the room: <i>&ldquo;Ooh, a mouthy one.&rdquo;</i> <b>That is your name here now.</b>",
  "She introduces you to two more friends as the mouthy one. <b>They are equally delighted by everybody.</b>",
  "You escalate. <b>She pats your arm and asks if you want coffee.</b> <b>She likes you exactly as much as she did a minute ago, and exactly as much as she likes everybody else.</b>",
  "PLOT — <b>Ask the room, loudly, whether anybody else keeps notebooks like Rosa's.</b> Everyone is friendly. Nobody knows what you mean. <b>Not one person.</b>",
  "Del is hoarse and scanning the room, and his eye stops on you.",
 ],
 5: [
  "You are claimed for the next dance before this one has ended. Then the one after that.",
  "PLOT — BERNARD, in an extremely good waistcoat, starts telling you about the hall's lease and who wants the Saturday slot cut. <b>Keep him talking.</b> He mentions Rosa wrote something down about this building once, years back — <b>and she turned out to be right about it.</b> <b>Write it on a slip and push it to the middle.</b>",
  "<i>&ldquo;You're exactly the right height.&rdquo;</i> She means it as an actual compliment. <b>She is right.</b>",
  "Claimed again. You cannot decline gracefully and you are not really trying to.",
  "Two hours of being swung round by strangers and <b>your neck seizes &mdash; the old warehouse one.</b> Bernard sees it before you do and fetches a chair without being asked.",
 ],
}

QUESTIONS = [
    "Who was writing in it before you?",
    "What happened to whoever stopped?",
    "Has anything you wrote ever come true?",
    "Do you know a Bea Ferro?",
    "Has anyone come asking about the book before us?",
    "What is the earliest date in it?",
    "Does anyone else have one?",
    "What did Vivian's father actually work on?",
    "Why were pages cut out of his notebook?",
    "Does your daughter know what you keep?",
    "What happens to it when you're gone?",
    "Have you ever been frightened of it?",
    "Does the name Farallon mean anything?",
    "Why did you stop?",
    "What made you keep going the first time?",
    "Who taught you to do it?",
    "Has anybody ever asked to see the book?",
    "What would make you stop writing in it?",
    "Do you keep anything else like it?",
    "Is there anything in it you wish you hadn't written?",
]

# The Alaia trade. It is NOT a punishment for a slip - it is a deal the players
# can see and choose. Say her daughter's name to Rosa and you lose this round's
# ROSA card, and in exchange you get a story, and then WINNIE retaliates on
# Rosa's behalf with something about young Rosa - which is real information and
# is the actual reason to pull the trigger.
ALAIA = [
    ("THE JUNIOR RANGER",
     "At nine she wrote to the Park Service demanding a job, got a form letter, and <b>framed it</b>. Then she made a clipboard and started citing the neighbours about their compost. <i>&ldquo;Mrs Ocampo got three. In one week. She kept them.&rdquo;</i>"),
    ("THE SUMMER OF THE TENT",
     "At eleven she camped in the back garden all summer &ldquo;to train&rdquo; and would not come inside. It ended with a skunk. <i>&ldquo;Six weeks. Two baths in tomato juice. She still says it was worth it.&rdquo;</i>"),
    ("THE WHISTLE",
     "At seven she was given a whistle and used it as her <b>only form of communication</b> for three weeks. <i>&ldquo;Her father gave it to her. I have never forgiven him.&rdquo;</i>"),
]

WINNIE_RETURNS = [
    "<i>&ldquo;Rosa. Tell them about the year you catalogued the whole hall's records and put them all back in the wrong boxes.&rdquo;</i> Rosa, without turning round: <i>&ldquo;They were not the wrong boxes. They were better boxes.&rdquo;</i>",
    "<i>&ldquo;She danced with a man for four years before she found out his name. Four years! She just never asked.&rdquo;</i> Rosa: <i>&ldquo;It never came up.&rdquo;</i>",
    "<i>&ldquo;She has been coming here since before you were born and has never once brought anybody. Not once. I have asked.&rdquo;</i> Rosa, evenly: <i>&ldquo;You have asked a great deal, Winnie.&rdquo;</i>",
]

ADOPTED = [
    "The swing is faster than you expected and the room keeps going round for a second after you stop. Everyone nearby is delighted. <b>This happens to absolutely everybody.</b>",
    "Left and right stop working. Entirely. Del, over the microphone, without breaking rhythm: <i>&ldquo;&mdash; allemande RIGHT &mdash; that's your other right, love &mdash;&rdquo;</i>",
    "<b>It clicks.</b> You lean back against somebody's arm and discover you are being held up by momentum, going faster than you thought a body could go while holding onto an eighty-year-old, <b>and you are grinning like an idiot.</b>",
    "A man in an excellent waistcoat takes both your hands and asks where you're from. He is not letting go until you answer properly.",
    "Somebody puts a hand between your shoulder blades and simply places you where you are supposed to be, without looking at you.",
    "You go the wrong way round and walk directly into a stranger. You both say sorry. Neither of you stops moving.",
    "“Give me weight, dear. Lean back. I've got you.” She is about five foot nothing and she flings you round a full turn.",
    "You have been dancing enthusiastically with a completely different set of four for eight full seconds and have only just noticed.",
    "A woman tells you the entire history of the hall's floorboards while you dance. You will remember all of it.",
    "Somebody has brought a grandson, under protest, and he is the only other person here under sixty. He asks whether you are also here against your will.",
]

def card(kind, title, body, foot=""):
    return (f'<div class="card {kind}"><div class="kind">{title}</div>'
            f'<div class="body">{body}</div>'
            f'<div class="foot">{foot}</div></div>')

cards = []
for text, tag, eff in CALLS:
    cards.append(card("call", "THE CALLER" + (f" &middot; {tag}" if tag else ""),
                      f"&ldquo;{text}&rdquo;",
                      eff or "Read it out loud. Loudly. Over everybody."))
for i, a in enumerate(ANSWERS, 1):
    foot = ("<b>Round four.</b> If it does not fit what they asked, <b>answer them for real first</b>, then read this."
            if i == 4 else
            "Read it aloud as Rosa. It will not answer the question. <b>That is the game.</b>")
    cards.append(card("answer", f"ROSA &middot; {i} of 4 &middot; IN ORDER", f"&ldquo;{a}&rdquo;", foot))
LOAD_FOOT = {
    "1979.": "<b>Her ledger's origin.</b> This is where the book came from. Do not let it go past as filler.",
    "She rang about you.": "<b>Vivian's referral, confirmed.</b> The old woman in Sacramento really did send them. Not filler.",
}

for a in ASIDES:
    load = next((v for k, v in LOAD_FOOT.items() if a.startswith(k)), None)
    cards.append(card("aside", "BONUS &middot; ROSA, IN PASSING" + (" &middot; THIS ONE MATTERS" if load else ""),
                      f"&ldquo;{a}&rdquo;",
                      load or "Quirky, not useful. She is already going."))
for slot, pc in PCS:
    n = len(ROUNDS[slot])
    for i, r in enumerate(ROUNDS[slot], 1):
        plot = r.startswith("PLOT — ")
        body = r[len("PLOT — "):] if plot else r
        foot = ("Play it out. Then write it on a slip."
                if plot else "One line, then pass.")
        if i == 5:
            foot += " <b>Coda &mdash; four rounds, so this one is not dealt.</b>"
        if slot == 2 and i == n:
            foot += " <b>Her last dealt card. Her fifth is the stumble and it is in your hand.</b>"
        # Unmapped, the header carries a literal {{pc:N}} token, so the band's
        # text-transform has to be switched off for it or it prints {{PC:N}}.
        label = pc.upper() if args.map else f'<span style="text-transform:none">{pc}</span>'
        cards.append(card("round plot" if plot else "round",
                          f"{label} &middot; {'DO THIS' if plot else 'ROUND'} {i} of {n}"
                          f" &middot; IN ORDER", body, foot))
# ONE STACK, interleaved and numbered 1-6: each Alaia story is immediately
# followed by the Winnie return that answers it. Mid-game there is no other way
# to tell which Winnie belongs to which story, so the number is on the card.
for j, ((lead, story), w) in enumerate(zip(ALAIA, WINNIE_RETURNS)):
    cards.append(card("alaia", f"ALAIA &middot; STACK {2*j+1} of 6 &middot; {lead}",
                      f"<i>&ldquo;Alaia sent you? <b>My</b> Alaia?&rdquo;</i><br>{story}",
                      f"No ROSA card &mdash; deal two next round. Stop at a real confession or 30 sec, "
                      f"then <b>STACK {2*j+2}</b>, the next card down."))
    cards.append(card("winnie", f"WINNIE &middot; STACK {2*j+2} of 6 &middot; GETS HER OWN BACK", w,
                      "Draw the moment somebody confesses. <b>This is what the trade bought.</b> "
                      "<b>Next trade starts at the next card down.</b>"))
for a in ADOPTED:
    cards.append(card("adopted", "ADOPTED", a,
                      "Ten seconds, then move on."))
for q in QUESTIONS:
    cards.append(card("question", "SOMETHING YOU WANT TO KNOW", q,
                      "Shout it in your own words &mdash; or shout something else."))
for slot, pc in PCS:
    cards.append(card("duck", "WHO HAS THE DUCK", f"<b>{pc}</b>",
                      "Set it aside."))
for _ in range(2):
    cards.append(card("duck past", "WHO HAS THE DUCK", "<b>SHE GOES PAST</b>",
                      "Nobody reaches her this round. Read a <b>BONUS</b> aside &mdash; she says it over her shoulder, already going &mdash; and everybody still gets their round card. <b>DEAL TWO ROSA CARDS NEXT ROUND</b>, exactly as after an Alaia story, or the deck runs a card short and round four breaks."))
cards.append(card("stumble held", "GM ONLY &middot; 3 of 3 &middot; AS THE BAND TAKES A BREAK",
    "&ldquo;No, it lives at the house. It's not the library's.&rdquo;",
    "The exit line. <b>It is on no other card and it has to land.</b>"))
cards.append(card("stumble held", "GM ONLY &middot; 2 of 3 &middot; PLAY IT STRAIGHT AFTER THE STUMBLE",
    "&ldquo;I've never met anyone else who does it.&rdquo;",
    "<b>You say this, as Rosa, in the hush &mdash; not a player off a card.</b> She says it while looking at the one who just caught her. <b>That adjacency is the whole episode: she states she is alone to the person who has just proved she is not.</b>"))
cards.append(card("stumble", "GM ONLY &middot; 1 of 3 &middot; HOLD ALL MORNING",
    "Rosa stumbles &mdash; half a second, nothing &mdash; and you are already moving. Nobody in this hall is looking.<br><b>Rosa steadies faster and more completely than a stumble should let her.</b> You are a nurse; you know what catching somebody looks like, and this was not that.<br>Rosa knows exactly what happened and says nothing. <b>She sits out the next dance. She never sits out.</b>",
    "<b>NO CALL. NO SHOUT. NO COUNTDOWN.</b> Put the duck in front of her and say nothing."))

HTML = f"""<meta charset="utf-8"><title>The Duck Has You</title>
<style>
 @page {{ size: letter; margin: 0.45in; }}
 body {{ font-family:"Helvetica Neue",Arial,sans-serif; margin:0; color:#2f2b22;
        font-size:9.6pt; line-height:1.36; }}
 h1 {{ font-size:16pt; letter-spacing:.13em; text-transform:uppercase; margin:0 0 4px; }}
 h2 {{ font-size:8.6pt; letter-spacing:.13em; text-transform:uppercase; color:#8a5a10;
       border-bottom:1px solid #d8d1bf; padding-bottom:2px; margin:13px 0 6px; }}
 .sub {{ font-size:10.5pt; margin:0 0 10px; color:#2f2b22; }}
 ol,ul {{ margin:0 0 6px 1.2em; padding:0; }} li {{ margin:3px 0; }}
 .read {{ background:#f0f7ec; border-left:4px solid #7aa06b; padding:8px 11px; margin:8px 0;
          font-family:Charter,Georgia,serif; font-style:italic; }}
 .read b {{ font-style:normal; }}
 .stop {{ background:#fdeeea; border-left:5px solid #b3261e; padding:6px 10px; margin:8px 0; }}
 .stop::before {{ content:"MISS THIS AND IT BREAKS"; display:block; font-size:6.4pt;
                 letter-spacing:.14em; font-weight:700; color:#b3261e; margin-bottom:2px; }}
 .note {{ border-left:2px solid #d8d1bf; padding:2px 0 2px 9px; margin:7px 0; }}
 .setup {{ background:#f2f1ed; border:1px solid #d8d1bf; padding:6px 9px; margin:11px 0 0;
           font-size:8.8pt; color:#4a463c; }}
 .pagebreak {{ page-break-before:always; }}
 .grid {{ display:flex; flex-wrap:wrap; }}
 .card {{ width:3.7in; height:2.0in; box-sizing:border-box; border:1px dashed #9c9484;
         padding:7px 9px; display:flex; flex-direction:column; page-break-inside:avoid;
         background:#fff; }}
 .kind {{ font-size:6.8pt; letter-spacing:.13em; font-weight:700; color:#fff;
          background:#6b6250; margin:-7px -9px 5px; padding:3px 9px; }}
 .card .body {{ flex:1; font-size:9.6pt; line-height:1.34; }}
 .card .foot {{ font-size:7pt; color:#8a8272; line-height:1.22; }}
 .call    .kind {{ background:#1f5fa8; }}
 .answer  .kind {{ background:#5b2d90; }}
 .aside   .kind {{ background:#0e6f74; }}
 .plot    .kind {{ background:#2f7d32; }}
 .round   .kind {{ background:#6b6250; }}
 .alaia   .kind, .winnie .kind {{ background:#b3261e; }}
 .adopted .kind {{ background:#7a4a1f; }}
 .duck    .kind {{ background:#8a6d00; }}
 .stumble .kind {{ background:#111; }}
 .question .kind {{ background:none; color:#6b6250; border-bottom:1px solid #6b6250;
                    margin:0 0 4px; padding:0 0 2px; }}
 .answer .body, .aside .body {{ font-style:italic; }}
 .question .body {{ font-size:11pt; font-weight:600; }}
 .duck .body {{ font-size:15pt; text-align:center; padding-top:12px; }}
 .past .body {{ font-size:12pt; }}
 /* SHE GOES PAST is shuffled into the DUCK deck and read from the back.
    It must never get its own colour, border or fill. Do not style .past further. */
 .plot {{ border:1px solid #2f7d32; }}
 .stumble {{ border:2px solid #111; }}
</style>

<h1>The Duck Has You</h1>
<p class="sub"><b>Rosa is in a line of forty dancers and the dance keeps taking her away.
The duck is Rosa.</b> Once a round it lands in front of one player, the other four shout
what they want asked, and that player gets <b>one sentence.</b>
Four rounds. <b>There is nothing to solve.</b></p>

<div class="stop">
<b>Four decks are in a fixed order. Never shuffle them &mdash; not at setup, not between rounds, not while tidying:</b>
<b>ROSA</b> (1&ndash;4) &middot; <b>ROUND</b> (five stacks by name, numbered) &middot; <b>ALAIA/WINNIE</b> (one stack, numbered 1&ndash;6) &middot; <b>GM ONLY</b> (three cards, in your hand, never in any deck).
<b>Every card in those four prints its own position, so a stack that gets mixed can always be put back.</b><br>
<b>Shuffle freely:</b> the other eleven CALLER &middot; DUCK &middot; QUESTION &middot; ADOPTED &middot; BONUS.
</div>

<div class="note"><b>Five cards, four rounds &mdash; that is correct and nothing is missing.</b>
Each player's ROUND stack is a small arc, and <b>the fifth card is a coda that does not get dealt.</b>
Three of those four codas can simply be left in the box. <b>{PC[1]}'s fifth is the payoff</b> &mdash;
hand it over at the end of the dance rather than losing it.
<b>{PC[2]}'s stack has four, not five.</b> That fifth card is <b>the stumble &mdash; GM ONLY 1 of 3</b>, held in
your hand all morning and played in silence in Scene 5. <b>It is deliberately not a round card; that is the beat.</b></div>

<h2>Do this first</h2>
<div class="setup">
<b>1.</b> Sort the <b>ROUND</b> cards into five stacks by name, <b>each in numbered order</b>, and deal one per player per round. <b>Never hand anybody their whole stack.</b><br>
<b>2.</b> Stack the <b>ROSA</b> cards 1&ndash;2&ndash;3&ndash;4 and <b>do not shuffle them, ever.</b><br>
<b>3.</b> Take the <b>CALLER STOPS</b> card out of the caller deck and set it aside for round four. Shuffle the other eleven.<br>
<b>4.</b> Shuffle the <b>DUCK</b> deck &mdash; five names and two SHE GOES PAST.<br>
<b>5.</b> Keep the <b>three GM ONLY</b> cards in your hand. They never go into any deck.<br>
<b>6.</b> Put <b>five blank slips and a pen</b> in the middle of the table, and the <b>rubber duck</b> beside them.<br>
<b>7.</b> Deal each player <b>three QUESTION cards, face down and private</b> (keep the rest as a draw pile; reshuffle the discards if it runs out) and <b>one ADOPTED card, face down</b> &mdash; that is their first time through the dance. <b>Have them read those out before round one.</b><br>
<b>8.</b> <b>ALAIA and WINNIE are one stack, numbered 1 to 6</b>, kept in that order and drawn off the top when the trade fires &mdash; a story, then the Winnie return that answers it. <b>Two trades' worth, and a spare pair.</b> <b>BONUS</b> is a loose pile you draw from whenever she passes without stopping, or at the top of any quiet gap.
</div>

<h2>Read this to the table &mdash; thirty seconds, then start</h2>
<div class="read">
<b>This duck is Rosa.</b> She is somewhere in a line of forty dancers and the dance keeps
taking her away.<br><br>
Each round the duck lands in front of one of you. <b>That is not your turn to ask a question.
That is the whole party's one chance this round, and you get one sentence.</b> Everybody else
gets ten seconds to shout at you what they want asked &mdash; all at once, over each other
&mdash; and you pick one and say it <b>in your own words.</b> Then you read me her answer off
a card.<br><br>
You have three cards in front of you. <b>Shout those, or shout anything else.</b>
And nobody writes anything down out there. You would look unhinged.
</div>
<div class="note"><b>That is everything they need. Start round one.</b> They will find out the
rest by playing: that she answers whatever she likes, that one of them will not get her, that
the mangled version is funnier. <b>Do not explain any of it in advance.</b></div>

<h2>The round &mdash; run this four times</h2>
<ol>
<li><b>THE CALL.</b> Whoever had the duck last round reads a CALLER card, loud, over
everybody. <i>(Round one: anybody. Round four: always the CALLER STOPS card &mdash; no shout,
they ask their own question, they get a straight answer.)</i></li>
<li><b>THE DUCK LANDS.</b> Draw one DUCK card, set it aside, put the duck in front of that
player. <i>&ldquo;The figure brings you round and Rosa is right there.&rdquo;</i>
<b>In round four only: if you draw SHE GOES PAST, set it aside and draw again</b> &mdash;
somebody always reaches her on the round the caller stops.</li>
<li><b>THE SHOUT.</b> Ten seconds &mdash; count down from three, out loud. Everyone
<i>except</i> the duck-holder yells what they want asked. <b>Overlapping is correct.</b>
A shouted QUESTION card is discarded and replaced.</li>
<li><b>ONE SENTENCE.</b> The duck-holder says it to Rosa in their own words. Not their own
question unless nobody shouted one.</li>
<li><b>ROSA ANSWERS.</b> They read the top ROSA card aloud as her. Take the duck back
mid-word. She is gone down the line.</li>
<li><b>ROUND CARDS.</b> One each, face up, <b>including whoever had the duck.</b> Play out
<b>exactly one</b> green DO THIS card properly &mdash; about forty seconds. The rest are one
line each and you move on fast.</li>
<li><b>THE GAP.</b> Two or three minutes. Water, coffee, changing partners. <b>The party can
finally reach each other. Shut up and let them.</b> Rosa is never free here &mdash; somebody
intercepts her within fifteen seconds, delighted, wanting to tell her about a hip.</li>
</ol>

<div class="stop"><b>FOUR rounds, then the stumble. Never five.</b>
<b>Past twenty minutes of dancing at the end of round two, drop to three.</b> Then <b>round three becomes the CALLER STOPS round, and you read ROSA 3 and ROSA 4 back to back.</b></div>

<div class="stop"><b>An ALAIA story or a SHE GOES PAST card costs this round's ROSA card.
Deal TWO ROSA cards next round.</b> Otherwise the deck runs short and round four breaks.</div>

<h2>The slips &mdash; put these in the middle of the table</h2>
<div class="note"><b>Five blank slips and a pen, in the centre.</b> Every time a green DO THIS
card turns up a fact about Rosa, <b>the player who got it writes it on a slip in their own
words and pushes it to the middle.</b><br>
<b>This is the only thing on the table that changes.</b> The shout has something to argue
from, the gap has something to point at, and by the last round they can look down and see what
they have built. <b>Do not write on the slips yourself and do not correct what they write.</b></div>

<h2>Two things they can trade a round for</h2>
<div class="note"><b>Say Alaia's name to Rosa</b> &mdash; she is delighted, and you lose this
round's ROSA card for a story. Draw an ALAIA card. <b>She stops when whoever said it admits
something true and embarrassing about themselves, or after thirty seconds.</b> Then draw a
WINNIE card: the room gets its own back on Rosa's behalf, <b>and that is what they bought.</b></div>
<div class="note"><b>Anything else the dance will not give them</b> &mdash; say what you are
doing. The answer is yes, it costs the duck this round, and they draw an ADOPTED card.</div>

<h2>If something goes sideways</h2>
<div class="note"><b>Never stop to look anything up. Every answer here is one line and none of
them needs undoing.</b><br>
<b>Nobody shouts?</b> The duck-holder asks their own. &middot;
<b>Two people talk over each other?</b> The duck-holder picks; you do not adjudicate. &middot;
<b>They say three sentences?</b> Let it go and take the duck back. &middot;
<b>You owe two ROSA cards and the deck is short?</b> Read the owed ones back to back &mdash; she answers, catches herself, answers again &mdash; or drop the middle one. <b>Never touch the GM-held cards.</b> &middot;
<b>A green card's fact is already on a slip?</b> Play the card anyway; it costs nothing. &middot;
<b>You forgot whose turn it was to read the CALLER card?</b> Anybody reads it.<br>
<b>And if you are ever unsure of anything at all: she is gone, deal the round cards, go to the
gap.</b> Nothing in this game breaks by moving forward, and nothing needs to be taken back.</div>

<div class="pagebreak"></div>
<h1 style="margin-bottom:10px">Cards &mdash; cut along the dashes</h1>
<div class="grid">{''.join(cards)}</div>
"""
out_pdf = args.out.resolve()
if args.keep_html:
    out_html = out_pdf.with_suffix(".html")
else:
    out_html = pathlib.Path(tempfile.mkdtemp(prefix="duck-")) / "dance-game.html"
out_html.write_text(HTML)
chrome = next((c for c in ("google-chrome", "chromium", "chromium-browser",
                           "google-chrome-stable") if shutil.which(c)), None)
if chrome is None:
    sys.exit("no Chrome/Chromium on PATH — needed to render the PDF")
subprocess.run([chrome,"--headless","--disable-gpu","--no-sandbox",
                "--no-pdf-header-footer",f"--print-to-pdf={out_pdf}",f"file://{out_html}"],
               check=True, capture_output=True)
n = len(cards)
print(f"Wrote {out_pdf} ({out_pdf.stat().st_size//1024} KB) — {n} cards")
