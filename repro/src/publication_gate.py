"""Run the deterministic current-evidence publication gate."""
from __future__ import annotations

import base64
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = ROOT / "outputs"
PAPER = "F8dIPCR1ly"
ARXIV = "2605.01425v1"
EXPECTED_BUNDLE_RECORDS = 15
EXPECTED_PROOF_ROWS = 108


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def run(script: str, *args: str) -> None:
    env = {**os.environ, "PYTHONPATH": str(ROOT / "repro" / "src")}
    subprocess.run([sys.executable, str(ROOT / script), *args], cwd=ROOT, env=env, check=True)


def source_metadata() -> dict:
    source = json.loads((ROOT / "sources.json").read_text())
    paper = source["paper"]
    artifact = source["source_artifact"]
    require(paper["openreview_id"] == PAPER, "OpenReview id drift")
    require(f'{paper["arxiv_id"]}{paper["arxiv_version"]}' == ARXIV, "arXiv version drift")
    source_path = ROOT / artifact["path"]
    require(source_path.is_file() and sha256(source_path) == artifact["sha256"], "primary source drift")
    contract = ROOT / source["challenge_contract"]["path"]
    require(sha256(contract) == source["challenge_contract"]["sha256"], "claim contract drift")
    require(source["audit"]["author_executable_files"] == [], "author executable unexpectedly present")
    require(not (ROOT / ".trackio").exists(), "private Trackio export present")
    return {
        "openreview_id": PAPER,
        "arxiv": ARXIV,
        "primary_pdf_sha256": sha256(source_path),
        "claim_contract_sha256": sha256(contract),
        "author_executable_files": [],
    }


def verify_results() -> dict:
    verdict = json.loads((OUTPUTS / "claim_verdicts.json").read_text())
    require(verdict["all_claims_complete"] is True, "claims incomplete")
    require(verdict["verdicts"] == ["verified"] * 4, "claim verdict drift")
    require(verdict["possible_points"] == 8, "point contract drift")
    theorem4 = list(csv.DictReader((OUTPUTS / "theorem4_grid.csv").open()))
    theorem5 = list(csv.DictReader((OUTPUTS / "theorem5_hard_family.csv").open()))
    proof = list(csv.DictReader((OUTPUTS / "proof_audit.csv").open()))
    require(len(theorem4) == 42, "Theorem 4 grid drift")
    require(len(theorem5) == 3048, "Section 5 grid drift")
    require(len(proof) == EXPECTED_PROOF_ROWS, "proof-audit row drift")
    return {
        "claim_verdicts_sha256": sha256(OUTPUTS / "claim_verdicts.json"),
        "theorem4_witnesses": len(theorem4),
        "theorem5_cells": len(theorem5),
        "proof_audit_cells": len(proof),
        "claim_outcomes": verdict["verdicts"],
    }


def verify_bundle() -> dict:
    bundle = OUTPUTS / "evidence_bundle.jsonl"
    require(bundle.is_file(), "missing evidence bundle")
    records = [json.loads(line) for line in bundle.read_text().splitlines() if line]
    require(len(records) == EXPECTED_BUNDLE_RECORDS, "bundle record count drift")
    seen = set()
    for record in records:
        relative = record["path"]
        require(relative not in seen, "duplicate bundle path")
        seen.add(relative)
        path = ROOT / relative
        data = path.read_bytes()
        require(path.is_file() and len(data) == record["bytes"], "bundle size drift")
        require(sha256(path) == record["sha256"], "bundle hash drift")
        require(base64.b64decode(record["payload_b64"]) == data, "bundle payload drift")
    require("sources.json" in seen and "docs/CLAIM_EVIDENCE.md" in seen, "missing public bundle records")
    return {"records": len(records), "bytes": bundle.stat().st_size, "sha256": sha256(bundle)}


def verify_manifest() -> dict:
    manifest_path = OUTPUTS / "artifact_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    records = manifest["files"]
    require(len(records) >= 28, "artifact manifest unexpectedly small")
    seen = set()
    for record in records:
        relative = record["path"]
        require(relative not in seen, "duplicate artifact path")
        seen.add(relative)
        path = ROOT / relative
        require(path.is_file(), f"missing artifact: {relative}")
        require(path.stat().st_size == record["bytes"] and sha256(path) == record["sha256"], f"artifact drift: {relative}")
    require("sources.json" in seen and "docs/primary.pdf" in seen, "source artifacts missing")
    require(not any(".trackio" in relative for relative in seen), "private export in manifest")
    return {"files": len(records), "sha256": sha256(manifest_path)}


def hygiene() -> dict:
    secret = re.compile(r"(?i)(hf_[a-z0-9]{20,}|github_pat_[a-z0-9_]{20,}|api[_-]?key\s*[:=]\s*['\"][^'\"]+)")
    private_fragments = ("/home/" + "dineshai/", "Dinesh" + "AI/")
    bad = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", ".venv", ".pytest_cache", ".trackio", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() not in {".py", ".json", ".jsonl", ".md", ".txt", ".csv"}:
            continue
        text = path.read_text(errors="replace")
        if secret.search(text) or any(fragment in text for fragment in private_fragments):
            bad.append(path.relative_to(ROOT).as_posix())
    require(not bad, f"hygiene failure: {bad}")
    return {"passed": True}


def main() -> None:
    run("repro/src/run_theorem4.py")
    run("repro/src/run_theorem5.py")
    run("repro/src/proof_audits.py")
    run("repro/src/verify_claims.py")
    tests = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "repro/tests"],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "repro" / "src")},
        text=True,
        capture_output=True,
    )
    if tests.returncode:
        raise RuntimeError(tests.stdout + tests.stderr)
    run("repro/src/build_bundle.py")
    run("repro/src/artifact_manifest.py")
    gate = {
        "gate_version": "publication-v1",
        "paper": PAPER,
        "status": "SCOPED_PASS",
        "overall_status": "VERIFIED_SCOPED_WITH_EXACT_FINITE_CONSTRUCTION_AUDIT",
        "strict_status": "NOT_READY",
        "publication_gate_passed": True,
        "verified_claims": 4,
        "possible_points": 8,
        "earned_points": 8,
        "source": source_metadata(),
        "verification": verify_results(),
        "evidence_bundle": verify_bundle(),
        "artifact_manifest": verify_manifest(),
        "hygiene": hygiene(),
        "tests_passed": True,
        "tests": "python -m pytest -q repro/tests: passed",
        "limitations": [
            "Finite numerical checks support the displayed constructions; they are not a machine-checked replacement for the analytical proofs.",
            "The repository contains no author executable, dataset pipeline, model checkpoint, or empirical benchmark.",
            "The Section 5 producer grid ends at ell=7; the asymptotic lower bound still relies on the paper's proof.",
        ],
        "score_forecast": None,
    }
    serialized = json.dumps(gate, indent=2, sort_keys=True) + "\n"
    for path in (
        ROOT / "publication_gate.json",
        OUTPUTS / "publication_gate.json",
        OUTPUTS / "PUBLICATION_GATE_PASSED.json",
        OUTPUTS / "CUMULATIVE_SCIENCE_GATE.json",
    ):
        path.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
