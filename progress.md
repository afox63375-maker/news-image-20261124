# progress.md — news-image-20261124

Built 24 Nov 2026, ~04:00–04:35 WIB, by the builder subagent.
Parent runs git/GitHub/bundle/check/submit afterwards — nothing here
is committed, bundled or submitted yet.

## What was done
- Studied the 22 Nov remake front page (image + README) and recreated
  its design system in original code: cream broadsheet, giant serif
  date, red stat strip, regional count bar, weather strip, 3 illustrated
  leads + 10 illustrated cards, dotted numbered map, DATE CHECK box.
- Researched real news with web search; wire cut-off 21:00 UTC Mon
  23 Nov. Every story is dated Tue 24 Nov 2026 in at least one time
  zone or takes place that day; date-checks and exclusions are in
  STORIES.md (incl. the Nvidia US-Monday / Australia-Tuesday and
  Nikkei 18:42 UTC timezone notes).
- `draw.py` (Pillow, build-time only) renders `entry.png`; all pictures,
  the map and the icons are drawn in code. Fixed after visual review:
  scenes clipped to their panels, lead tag chips right-aligned, hockey
  scoreboard moved off the number chip, footer shortened.
- `main.py` is standard library only; it validates entry.png and copies
  it unchanged to $MAKEFUN_OUTPUT_DIR/entry.png.

## Verification (all passed)
- entry.png: exactly 1024x1024, 161,360 bytes (< 1 MiB),
  sha256 4a61bb42241a7a5e8780a5e5d28ccc8e2093d036dd3363a762040ec68dcc9cd0
- main.py run twice into two different output dirs: identical sha256
- draw.py run twice: identical sha256 (renderer deterministic)
- main.py imports only os, struct, sys, zlib (all stdlib)
- entry.png opened and inspected: text legible, no garbling, no
  overlapping panels; map pins readable; DATE CHECK box fits in 2 lines

## Story count
35 stories: 3 leads + 10 cards + 22 briefs. Regions: Asia-Pacific 26,
Europe 3, Middle East 2, Americas 2, World 2.
Leads: (1) Guru Nanak 557th Prakash Utsav, Amritsar; (2) Nvidia
reinstates Jensen Huang, chip stocks +13%; (3) Indonesia names VP
candidates, Jakarta.
