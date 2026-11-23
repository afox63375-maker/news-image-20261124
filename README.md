[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/afox63375-maker/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/afox63375-maker/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# Tuesday 24 November 2026 — The World in One Day

A single-page newspaper front page that sums up Tuesday 24 November 2026
in 35 stories, built on the front-page discipline of the day's top-ranked
entry: a cream broadsheet sheet, a giant serif date, a strip of big red
numbers, and a regional count bar — with every story carried by a picture
that shows the story itself.

## What is on the page

- **Three lead stories, fully illustrated.** The Golden Temple glows for
  Guru Nanak's 557th Prakash Utsav in Amritsar; a chip and a soaring chart
  for Nvidia reinstating Jensen Huang as chief executive; a ballot box and
  Jakarta towers for Indonesia naming its vice-presidential candidates.
- **Ten more stories as illustrated cards** (4–13): the Karthigai Deepam
  flame on the Madurai hill, a courthouse and gavel for the Dhruv Rathee
  warrant, rising bars for India's startup boom, two flags and a handshake
  for the India–Egypt pact, an assembly hall and elephant for the Karnataka
  MLA resignation, a hockey pitch at 7–0, a squash court, a cinema screen
  for IFFI's Gandhi Medal race, the TRISHNA satellite, and fog and rain
  for the IMD alerts.
- **A Tuesday weather strip**: forecast highs and lows with drawn icons
  for Amritsar, New Delhi, Madurai, Jakarta, Sydney and London.
- **A dotted world map** whose numbered pins match the story numbers and
  are coloured by region, beside a 22-item brief list (14–35).
- **A date check box** stating the wire cut-off time and naming the
  stories left out as other days' news.

## How it is made

Every picture, the map and the icons are drawn in code with Pillow
primitives — no photographs and no image assets. The drawing is
deterministic: run it twice and the PNG is byte-identical.

`main.py` is the repository entrypoint. It uses only the Python
standard library: it validates the bundled `entry.png` (PNG signature,
chunk CRCs, an IHDR no larger than 1024×1024, at most 1 MiB, IDAT
present, IEND last) and copies the bytes unchanged to
`$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To re-render the picture from scratch:

```sh
python3 draw.py
```

## Story dates

Every story happened or was first reported on Tuesday 24 November 2026
in at least one time zone, or takes place that day. The research notes,
with a first-reported date and source for each story and the list of
stale stories deliberately left out, are in `STORIES.md`.
