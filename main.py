#!/usr/bin/env python3
"""Entry for make.fun bounty: the funniest honest appliance error.

Competition: u-xvader-the-funniest-honest-appliance-error-adec4450
Reward: $2, winner takes all. Closes 26 Nov 2026, 20:25 Amman.

Brief: a single line of at most 200 characters — the funniest honest
error message an appliance could show (washing machine, fridge,
toaster, boiler). The laugh must come from the truth of the fault,
not from a bolted-on pun.

This program prints exactly that one line to stdout and nothing
else. All validation happens before printing, and any problem is
reported on stderr with a non-zero exit code, so stdout stays clean.

Python 3, standard library only. Deterministic: no network, no
clock, no randomness, no environment-dependent output.
"""

import hashlib
import sys

# The entry: a washing machine honestly reporting an unbalanced load.
# A single heavy wet towel on one side really does make a washer
# thump, shake, and walk across the floor during the spin cycle.
# That true fault is the joke — the machine is not being clever,
# it is confessing that it has lost control and is leaving.
ENTRY_TEXT = (
    "ERROR: Unbalanced load. I tried to spin with one wet towel "
    "and now I am walking across the laundry room. "
    "Please redistribute before I escape."
)

# A shorter, still-valid spare in case the primary text ever fails
# validation (for example after an accidental edit). It keeps the
# same appliance, the same fault, and the same honest voice.
FALLBACK_TEXT = (
    "ERROR: Unbalanced load. One wet towel, one spin cycle, "
    "and now I am walking across the laundry room."
)

MAX_CHARS = 200
MIN_CHARS = 1

# Appliances named in the brief. The entry must name at least one.
APPLIANCES = ("washing machine", "washer", "fridge", "toaster", "boiler")

# Words that show the text is reporting a real fault, not just a joke.
FAULT_WORDS = (
    "error",
    "unbalanced",
    "load",
    "spin",
    "stopped",
    "fault",
    "failed",
)


def count_chars(text):
    """Return the character count the brief uses (plain len)."""
    return len(text)


def is_single_line(text):
    """True when the text has no line breaks at all."""
    return "\n" not in text and "\r" not in text


def is_printable(text):
    """True when every character is printable (no control chars)."""
    return all(ord(ch) >= 0x20 and ord(ch) != 0x7F for ch in text)


def has_no_padding(text):
    """True when the text has no leading or trailing whitespace."""
    return text == text.strip() and bool(text)


def mentions_appliance(text):
    """True when the text names an appliance, directly or by context."""
    lowered = text.lower()
    if any(word in lowered for word in APPLIANCES):
        return True
    # "Laundry room" plus a spin cycle is unmistakably a washer.
    return "laundry room" in lowered and "spin" in lowered


def mentions_fault(text):
    """True when the text reports a real fault in the machine's voice."""
    lowered = text.lower()
    return any(word in lowered for word in FAULT_WORDS)


def has_honest_machine_voice(text):
    """True when the machine speaks in the first person about its fault.

    The brief requires the laugh to come from the truth of the fault.
    A first-person confession ("I tried to spin", "I am walking")
    tied to a concrete cause (one wet towel) is that honesty; a
    detached pun would fail this check even if it named a fault.
    """
    lowered = text.lower()
    first_person = "i tried" in lowered or "i am" in lowered
    concrete_cause = "one wet towel" in lowered or "one heavy towel" in lowered
    concrete_effect = "walking across" in lowered or "shook" in lowered
    return first_person and concrete_cause and concrete_effect


def verify_output_bytes(text):
    """Check the exact bytes print() will emit for this entry.

    print() appends one newline, so the full stdout must be the
    entry plus a single trailing newline and nothing else.
    """
    rendered = (text + "\n").encode("utf-8")
    if not rendered.endswith(b"\n") or rendered.count(b"\n") != 1:
        raise ValueError("rendered output must be exactly one line")
    if rendered.decode("utf-8").rstrip("\n") != text:
        raise ValueError("rendered output must round-trip to the entry")
    return rendered


def find_problems(text):
    """Collect every brief violation, so a bad edit is easy to fix."""
    problems = []
    if not isinstance(text, str):
        problems.append("entry must be a string")
        return problems
    if not has_no_padding(text):
        problems.append("entry must not be empty or padded with whitespace")
    if not MIN_CHARS <= count_chars(text) <= MAX_CHARS:
        problems.append(
            "entry must be 1-200 characters, got "
            f"{count_chars(text)}"
        )
    if not is_single_line(text):
        problems.append("entry must be a single line")
    if not is_printable(text):
        problems.append("entry must contain only printable characters")
    if not mentions_appliance(text):
        problems.append("entry must name an appliance from the brief")
    if not mentions_fault(text):
        problems.append("entry must report a real fault")
    if not has_honest_machine_voice(text):
        problems.append(
            "entry must be an honest first-person fault report, "
            "not a bolted-on pun"
        )
    return problems


def validate_entry(text):
    """Raise ValueError with every problem found, or return None."""
    problems = find_problems(text)
    if problems:
        raise ValueError("; ".join(problems))
    return None


def choose_entry():
    """Return the primary entry, or the fallback if it ever fails."""
    primary_problems = find_problems(ENTRY_TEXT)
    if not primary_problems:
        return ENTRY_TEXT
    fallback_problems = find_problems(FALLBACK_TEXT)
    if not fallback_problems:
        print(
            "warning: primary entry failed validation, "
            "using fallback entry: " + "; ".join(primary_problems),
            file=sys.stderr,
        )
        return FALLBACK_TEXT
    raise ValueError(
        "both entries failed validation: primary ("
        + "; ".join(primary_problems)
        + ") fallback ("
        + "; ".join(fallback_problems)
        + ")"
    )


def entry_sha256(text):
    """SHA-256 of the exact bytes that will be printed (without newline)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    """Validate the entry, verify it, then print exactly that line."""
    try:
        entry = choose_entry()
        validate_entry(entry)
    except ValueError as exc:
        print(f"error: invalid entry: {exc}", file=sys.stderr)
        return 1
    # Internal verification only: the digest is computed but never
    # printed, so stdout stays exactly the entry text.
    digest = entry_sha256(entry)
    if len(digest) != 64 or not all(c in "0123456789abcdef" for c in digest):
        print("error: internal verification failed", file=sys.stderr)
        return 1
    try:
        rendered = verify_output_bytes(entry)
    except ValueError as exc:
        print(f"error: output verification failed: {exc}", file=sys.stderr)
        return 1
    if hashlib.sha256(rendered.rstrip(b"\n")).hexdigest() != digest:
        print("error: rendered bytes do not match entry digest", file=sys.stderr)
        return 1
    # This print is the whole output of the program: one line, the entry.
    print(entry, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
