[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/afox63375-maker/news-image-20261124-entry/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/afox63375-maker/news-image-20261124-entry/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# Tuesday 24 November 2026 — The World in One Day

One 1024×1024 front page that sums up Tuesday 24 November 2026 in a
single image: 35 world stories, every one of them reported — or still
developing — on that Tuesday in at least one time zone.

The page follows the classic newspaper shape: a giant serif dateline, a
red stat strip, a regional count bar, a weather strip for the story
cities, three large illustrated lead stories, ten illustrated mini
cards, a dotted world map with numbered pins, a list of the other 22
stories, and a DATE CHECK box that names the stale news left out on
purpose (the Sunday hockey and squash results, Monday's warrant and
the COP31 collapse among them).

## Stories inside

- **Leads:** Sikhs mark Guru Nanak's 557th birth anniversary in
  Amritsar · Nvidia reinstates Jensen Huang as chief executive, shares
  up 31% · Indonesia names its vice-presidential candidates.
- **Cards:** the Karthigai Deepam lamp lit at Thiruparankundram · the
  Supreme Court's Godhra bail order · India's 52% startup growth ·
  an India–Egypt trade pact · a Karnataka MLA's resignation · FIFA
  naming the 2031 and 2035 Women's World Cup hosts · India women
  facing China in the Asian Champions Trophy · ten films vying for the
  IFFI Gandhi Medal · the India–France TRISHNA satellite · the IMD's
  fog and heavy-rain warnings.
- **Plus 22 briefs**, from the Supreme Court's anti-defection PIL to
  the Pope's meeting with President Milei.

Full sourcing and the date check for every story live in
[`STORIES.md`](STORIES.md).

## How it is built

- `draw.py` renders `entry.png` with Pillow (build time only). Every
  picture, the map and the icons are drawn in code — no stock photos,
  no external assets. Run it again and the bytes come out identical.
- `main.py` is the entrypoint and uses only the Python standard
  library. It validates `entry.png` (PNG structure and chunk CRCs,
  exactly 1024×1024, under 1 MiB) and copies it unchanged to
  `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run

```sh
python3 draw.py            # render entry.png (deterministic)
python3 main.py            # validate and copy to $MAKEFUN_OUTPUT_DIR
python3 main.py --check-only
```

Python 3.12 and Pillow are all `draw.py` needs; `main.py` needs no
third-party package at all.

## Verification

- `draw.py` run twice produces byte-identical `entry.png`
  (sha256 `0c38004f11b387f35f271d4216036f0b00e185f7b309446d573b9542c7c703c4`,
  182,783 bytes, 1024×1024).
- `main.py` run twice to two different output directories copies the
  same bytes (sha256 match on both).
- `main.py` imports only `hashlib`, `os`, `struct`, `sys` and `zlib` —
  standard library only, verified with `ast`.

## Licence

MIT — see [`LICENSE`](LICENSE).

---

Built for the make.fun bounty
[news-image-20261124](https://make.fun/bounty/news-image-20261124) —
sum up 24 November's world news in one image. Play make.fun yourself:
https://make.fun/r/1hh4a8y6
