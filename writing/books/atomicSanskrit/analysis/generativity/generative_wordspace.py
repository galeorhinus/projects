#!/usr/bin/env python3
"""Reproduce the schematic word-space arithmetic used by the endnote audit."""

DHATUS = 2_168
PREFIX_STATES = 23  # no prefix plus 22 listed upasargas
LAKARAS = 10
PERSON_NUMBER_SLOTS = 9
PADA_SERIES = 2
NOMINAL_DERIVATION_PLACEHOLDERS = 10
CASE_NUMBER_SLOTS = 24


def main() -> None:
    finite_verb_slots = (
        DHATUS * PREFIX_STATES * LAKARAS * PERSON_NUMBER_SLOTS * PADA_SERIES
    )
    nominal_slots = (
        DHATUS
        * PREFIX_STATES
        * NOMINAL_DERIVATION_PLACEHOLDERS
        * CASE_NUMBER_SLOTS
    )
    total_slots = finite_verb_slots + nominal_slots

    print(f"finite verb slots: {finite_verb_slots:,}")
    print(f"nominal slots:     {nominal_slots:,}")
    print(f"combined slots:    {total_slots:,}")
    print("These are formal grid slots, not a count of valid or distinct Sanskrit words.")


if __name__ == "__main__":
    main()
