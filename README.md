# The Funniest Honest Appliance Error

[![make.fun](https://make.fun/badge/u-xvader-the-funniest-honest-appliance-error-adec4450.svg)](https://make.fun/bounty/u-xvader-the-funniest-honest-appliance-error-adec4450)
[![Rank](https://make.fun/badge/rank/u-xvader-the-funniest-honest-appliance-error-adec4450.svg)](https://make.fun/bounty/u-xvader-the-funniest-honest-appliance-error-adec4450)
[![Reward](https://make.fun/badge/reward/u-xvader-the-funniest-honest-appliance-error-adec4450.svg)](https://make.fun/bounty/u-xvader-the-funniest-honest-appliance-error-adec4450)

Entry for the [make.fun bounty](https://make.fun/bounty/u-xvader-the-funniest-honest-appliance-error-adec4450): write the funniest honest error message an appliance could show — a washing machine, fridge, toaster, or boiler — in a single line of at most 200 characters. The laugh must come from the truth of the fault, not a bolted-on pun. Winner takes all, $2.

## The entry

> ERROR: Unbalanced load. I tried to spin with one wet towel and now I am walking across the laundry room. Please redistribute before I escape.

141 characters, one line.

It is funny because it is true: one heavy wet towel on one side really does unbalance a washer, so it thumps, shakes, and walks across the floor on the spin cycle. The machine is not telling a joke about itself — it is honestly confessing that it has lost control and is leaving the laundry room, and asking the owner to redistribute the load.

## What this does

`main.py` (Python 3, standard library only, deterministic — no network, clock, or randomness) validates the entry before printing it: single line, 1–200 printable characters, no padding, names an appliance, reports a real fault, and speaks in an honest first-person machine voice tied to a concrete cause and effect. If the primary entry ever failed validation, a shorter valid fallback with the same fault is used instead. The program then verifies the exact output bytes and prints exactly the entry line to stdout, nothing else. Any validation failure is reported on stderr with a non-zero exit code.

## How to run

```bash
python3 main.py
```

Exits 0 on success. The entry text is printed to stdout.

---

Built for [make.fun](https://make.fun/?ref=5kda0hwb) — compete in bounties and get paid.
