#!/usr/bin/env python3
"""Validate and report the Vaidika krt semantic-operation classification."""

from __future__ import annotations

from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Data, Krt, Pratipadika, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
CONFIG = HERE / "vaidika_krt_operations.json"
CLASSIFICATION = HERE / "krt_classification.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This audit requires Vidyut 0.4.0")
    config = json.loads(CONFIG.read_text())
    prior = json.loads(CLASSIFICATION.read_text())
    metadata_deferred = set(prior["vedic_only"])
    source_recovered = {"kvasu"}
    if set(config["identifiers"]) != metadata_deferred | source_recovered:
        raise ValueError("The Vaidika classification must cover the metadata-deferred set plus source-recovered kvasu")
    covered = [identifier for operation in config["operations"] for identifier in operation["identifiers"]]
    if set(covered) != set(config["identifiers"]):
        raise ValueError("Every identifier must occur in at least one semantic operation")
    entries = Data(str(ARCHIVE)).load_dhatu_entries()
    grammar = Vyakarana(log_steps=False, is_chandasi=True, use_svaras=True, nlp_mode=False)
    diagnostics = []
    for identifier in config["identifiers"]:
        roots = forms = 0
        samples = []
        for entry in entries:
            output = sorted({
                result.text for result in grammar.derive(
                    Pratipadika.krdanta(entry.dhatu, getattr(Krt, identifier))
                )
            })
            if output:
                roots += 1; forms += len(output)
                if len(samples) < 2:
                    samples.append({"source_code": entry.code, "forms_slp1": output[:2]})
        diagnostics.append({
            "identifier": identifier, "source_entries_with_output": roots,
            "output_forms": forms, "samples": samples,
        })
    strategies = Counter(operation["engine_strategy"] for operation in config["operations"])
    report = {
        "date": config["date"], "identifier_count": len(config["identifiers"]),
        "engine_metadata_deferred_identifiers": len(metadata_deferred),
        "source_recovered_identifiers": sorted(source_recovered),
        "semantic_operation_count": len(config["operations"]),
        "operation_strategy_counts": dict(sorted(strategies.items())),
        "operations": config["operations"], "engine_diagnostics": diagnostics,
        "interpretation": "An engine zero records a coverage gap, not a grammatical prohibition. Multiple identifiers attached to one operation are alternative formal realizations unless the source assigns distinct meanings.",
        "engine": {"name": "Vidyut", "version": "0.4.0", "commit": json.loads(MANIFEST.read_text())["generator_commit"]},
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (CONFIG, CLASSIFICATION, MANIFEST, Path(__file__))},
    }
    (RESULTS / "vaidika_krt_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Vaidika कृत्प्रत्यय Classification", "",
        f"The **{len(metadata_deferred)} identifiers deferred by engine metadata**, together with **क्वसु (kvasu)** recovered from the source-level domain review, express **{len(config['operations'])} source-defined semantic operations**. The ledger therefore counts meanings by operation, not by the number of suffix spellings or accent variants.", "",
        "| Operation | Identifiers | Rule | Engine path |", "|---|---|---|---|",
    ]
    for operation in config["operations"]:
        lines.append(
            f"| {operation['operation_id']} | {', '.join(operation['identifiers'])} | "
            f"{', '.join(operation['rule_refs'])} | {operation['engine_strategy']} |"
        )
    lines.extend(["", "A zero-output identifier remains unresolved by the pinned engine. It is not rejected and contributes zero to the admitted count until a reproducible generator implements its source condition.", ""])
    (RESULTS / "vaidika_krt_classification.md").write_text("\n".join(lines))
    print(f"Classified {len(config['identifiers'])} identifiers as {len(config['operations'])} semantic operations.")


if __name__ == "__main__":
    main()
