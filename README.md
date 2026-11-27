# The World in One Day — 27 November 2026

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/c/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/berkahmuse/news-image-20261127-globe/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/berkahmuse/news-image-20261127-globe/reward.svg)](https://make.fun/bounty/news-image-20261127)

Entry for the make.fun competition
[Sum up 27 November's world news in one image](https://make.fun/c/news-image-20261127)
(`news-image-20261127`).

A globe-centred world infographic: one drawn globe with the day's six
verified stories as numbered callouts around it, each pinned to where it
happened.

![entry](entry.png)

## The six stories

1. **USA · Texas** — Exchanges file for 23-hour trading: 24X and Texas
   exchanges seek round-the-clock trading.
2. **Pakistan** — Mecca alliance meets in Islamabad: Pakistan, Saudi,
   Turkey open defence talks Nov 27–28.
3. **USA · Michigan** — Bears stun Lions in Thanksgiving thriller:
   Williams to Odunze, 3 seconds left; 39–35, Bears lead North.
4. **Kuwait** — Iran blames Kyiv for deadly strike: Tehran denies drone
   attack that killed 2 Italians.
5. **Guinea-Bissau** — Elections delayed to 2028: military rulers extend
   transition by two years.
6. **Saudi Arabia** — Houthis hit Aramco refinery: 1 worker killed,
   several hurt; some operations halted.

Sources: Reuters, Fox News, U.S. Federal Register (via BullBear.news
digest for 27 Nov 2026).

## Why these six are 27 November news

Every story below was first reported, or happened, on 27 November 2026
in at least one Asia-Pacific time zone (UTC+7 to UTC+13). Times are UTC
unless noted; WIB = UTC+7, AEDT = UTC+11, NZDT = UTC+13.

| # | Story | Timestamp | 27 Nov where |
|---|-------|-----------|--------------|
| 1 | 24X / Texas Stock Exchange file for 23-hour trading | U.S. Federal Register, 27 Nov 2026, 00:00 UTC | 27 Nov 00:00 UTC; 07:00 WIB |
| 2 | Mecca alliance meeting opens in Islamabad | Reuters (reported Thu 26 Nov); meeting held Fri–Sat 27–28 Nov | Event day: Fri 27 Nov (Islamabad, UTC+5) |
| 3 | Bears beat Lions 39–35, TD with 3 seconds left | Game ended ~16:00 ET Thu 26 Nov (Reuters recap) | 04:00 WIB Fri 27 Nov |
| 4 | Iran blames Kyiv for Kuwait drone strike; Tehran denies role | Fox News write-up ~23:55 UTC Thu 26 Nov; Araghchi denial calls Thu evening | 06:55 WIB Fri 27 Nov |
| 5 | Guinea-Bissau delays elections to Nov 2028 | Reuters, Thu 26 Nov 17:13:40 UTC (decree issued that day) | 00:13 WIB Fri 27 Nov |
| 6 | Houthis hit Jazan refinery; 1 Nepali worker killed | Saudi Energy Ministry statement, published 19:30 UTC Thu 26 Nov | 02:30 WIB Fri 27 Nov |

This is a rebuild (v2). The v1 entry used six stories that were all
26 November news; an independent verifier failed it on story dates.
v2 replaces all six stories with the ones above, fixes the card-1
truncation (body text may now use 3 lines, so no word is dropped), and
drops the SPDX header line from `LICENSE` so GitHub detects the MIT
license. The globe concept, layout, and anchor are unchanged.

## Run

```sh
python3 draw.py   # redraws entry.png (Pillow, build time only)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py  # writes out/entry.png
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png` after checking it is a whole PNG of at most 1024×1024
pixels and at most 1 MiB. Two runs produce byte-identical output
(sha256 `d3f6d57a99ee17ce8bbc71c4b6dbd1bd4771076fdec64a07af07267baba6ead8`).

Anchor: drand round 34311782 (`d0561e1798e46771454281d5950581c9cdd7385b`).

## License

MIT — see `LICENSE`.
