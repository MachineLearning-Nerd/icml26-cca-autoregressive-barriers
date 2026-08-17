#!/usr/bin/env python3
"""Verify the CCA dossier and live GitHub publication state."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = "icml26-cca-autoregressive-barriers"
CANONICAL = (
    "MachineLearning-Nerd",
    "MachineLearning-Nerd@users.noreply.github.com",
)
EXPECTED_BRANCHES = {"main"}
EXPECTED_STATUSES = [
    "verified_scoped",
    "verified_scoped",
    "verified_scoped",
    "verified_scoped",
]
SOURCE_PDF_SHA = "bb03dbafca39e5c0cf19d44bf6b1982d65736a6314370d6ec90d1e87c3890f34"
CONTRACT_SHA = "20dd0d213a796b540a690aad581bc705dc7b24444c0264688efe3bf58c278fec"
CLAIM_VERDICTS_SHA = "87ffc8594bc0f9c0e749fb22eae56db485204b8b72034180854b7ef663964594"
EVIDENCE_BUNDLE_SHA = "18034f2d65e664a7e04128c616d1e026b0dc4874149ce5019274abc7b1825fa4"
ARTIFACT_MANIFEST_SHA = "92eb76da3b65a53d1e05fcf75feacb856eeb1cfa2d8d7b0347f0eaffa31cd283"
REQUIRED_PATHS = [
    ".gitignore",
    "README.md",
    "STATUS.md",
    "sources.json",
    "publication_gate.json",
    "AUTONOMOUS_STATE.json",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "REPORT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "BRANCH_AUDIT.md",
    "branch-audit.md",
    "claims.json",
    "EVIDENCE_MANIFEST.json",
    "verify_final.py",
    "docs/BRANCH_AUDIT.md",
    "docs/CLAIM_EVIDENCE.md",
    "docs/PUBLICATION_GATE.md",
    "docs/SOURCE_AUDIT.md",
    "docs/independent_proof_audit.md",
    "docs/primary.pdf",
    "outputs/CUMULATIVE_SCIENCE_GATE.json",
    "outputs/PUBLICATION_GATE_PASSED.json",
    "outputs/artifact_manifest.json",
    "outputs/claim_verdicts.json",
    "outputs/evidence_bundle.jsonl",
    "outputs/proof_audit.csv",
    "outputs/publication_gate.json",
    "outputs/theorem4_grid.csv",
    "outputs/theorem5_hard_family.csv",
    "repro/configs/live_claims.json",
    "repro/requirements.txt",
    "repro/src/artifact_manifest.py",
    "repro/src/build_bundle.py",
    "repro/src/proof_audits.py",
    "repro/src/publication_gate.py",
    "repro/src/run_theorem4.py",
    "repro/src/run_theorem5.py",
    "repro/src/theorem4.py",
    "repro/src/theorem5.py",
    "repro/src/verify_claims.py",
    "repro/tests/test_theorem4.py",
    "repro/tests/test_theorem5.py",
]


def fail(message: str) -> None:
    print(f"FINAL_AUDIT=FAILED {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"command failed: {' '.join(args)}\n{result.stderr.strip()}")
    return result.stdout


def current_bytes(path: str) -> bytes:
    local = ROOT / path
    if local.exists():
        return local.read_bytes()
    result = subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode:
        fail(f"required path is unavailable: {path}")
    return result.stdout


def current_json(path: str) -> object:
    try:
        return json.loads(current_bytes(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
    return None


def sha256(path: str) -> str:
    return hashlib.sha256(current_bytes(path)).hexdigest()


def verify_manifest() -> None:
    manifest = current_json("EVIDENCE_MANIFEST.json")
    require(isinstance(manifest, dict), "manifest is not an object")
    require(manifest.get("schema_version") == 1, "unsupported manifest schema")
    require(manifest.get("hash_algorithm") == "sha256", "manifest hash algorithm changed")
    entries = manifest.get("entries")
    require(isinstance(entries, list) and entries, "evidence manifest is empty")
    seen = set()
    for entry in entries:
        require(isinstance(entry, dict), "manifest entry is not an object")
        path = entry.get("path")
        expected = entry.get("sha256")
        require(isinstance(path, str), "manifest path is missing")
        require(
            not Path(path).is_absolute() and ".." not in Path(path).parts,
            f"unsafe manifest path: {path}",
        )
        require(isinstance(expected, str) and len(expected) == 64, f"bad manifest hash for {path}")
        require(path not in seen, f"duplicate manifest path: {path}")
        seen.add(path)
        require((ROOT / path).exists(), f"manifest path is missing: {path}")
        require(sha256(path) == expected, f"manifest hash mismatch: {path}")
    require("AUTONOMOUS_STATE.json" not in seen, "state must not create a hash cycle")


def verify_git_state() -> tuple[int, int]:
    origin = run("git", "config", "--get", "remote.origin.url").strip()
    require(
        origin in {
            f"https://github.com/MachineLearning-Nerd/{REPOSITORY}.git",
            f"git@github.com:MachineLearning-Nerd/{REPOSITORY}.git",
        },
        f"unexpected origin: {origin}",
    )
    require(
        "ref: refs/heads/main\tHEAD" in run("git", "ls-remote", "--symref", "origin", "HEAD"),
        "origin/HEAD is not main",
    )

    remote_heads = {}
    for line in run("git", "ls-remote", "--heads", "origin").splitlines():
        commit, ref = line.split("\t", 1)
        require(ref.startswith("refs/heads/"), f"unexpected remote ref: {ref}")
        remote_heads[ref.removeprefix("refs/heads/")] = commit
    require(set(remote_heads) == EXPECTED_BRANCHES, "remote branch set changed")
    for branch in EXPECTED_BRANCHES:
        require(
            remote_heads[branch] == run("git", "rev-parse", f"origin/{branch}").strip(),
            f"origin/{branch} differs from the live remote tip",
        )

    local_heads = set(
        run(
            "git",
            "for-each-ref",
            "--format=%(refname:strip=2)",
            "refs/heads",
        ).splitlines()
    )
    require(local_heads <= EXPECTED_BRANCHES, "unexpected local branch")
    require(run("git", "branch", "--show-current").strip() == "main", "current branch is not main")
    refs = run("git", "for-each-ref", "--format=%(refname)", "refs").splitlines()
    require(not any("refs/original/" in ref for ref in refs), "refs/original remains")

    identities = set()
    for line in run("git", "log", "--all", "--format=%an\t%ae\t%cn\t%ce").splitlines():
        if line.strip():
            identities.add(tuple(line.split("\t")))
    require(
        identities == {(CANONICAL[0], CANONICAL[1], CANONICAL[0], CANONICAL[1])},
        f"non-canonical reachable identity: {sorted(identities)}",
    )
    require(
        "co-authored-by:" not in run("git", "log", "--all", "--format=%B").lower(),
        "co-author trailer found",
    )
    commit_count = int(run("git", "rev-list", "--count", "--all").strip())
    require(commit_count >= 11, f"unexpectedly short history: {commit_count}")
    return len(remote_heads), commit_count


def verify_artifacts() -> None:
    for path in REQUIRED_PATHS:
        require((ROOT / path).exists(), f"required path missing: {path}")

    sources = current_json("sources.json")
    require(isinstance(sources, dict), "sources.json is not an object")
    paper = sources.get("paper", {})
    require(
        paper.get("openreview_id") == "F8dIPCR1ly"
        and paper.get("arxiv_id") == "2605.01425"
        and paper.get("arxiv_version") == "v1",
        "paper source pin changed",
    )
    repository = sources.get("repository", {})
    require(
        repository.get("owner") == "MachineLearning-Nerd"
        and repository.get("final_name") == REPOSITORY
        and repository.get("default_branch") == "main"
        and repository.get("former_name") == "icml26-repro-F8dIPCR1ly-cca-autoregressive-barriers",
        "repository metadata changed",
    )
    source_artifact = sources.get("source_artifact", {})
    require(
        source_artifact.get("path") == "docs/primary.pdf"
        and source_artifact.get("sha256") == SOURCE_PDF_SHA,
        "primary PDF pin changed",
    )
    contract = sources.get("challenge_contract", {})
    require(
        contract.get("path") == "repro/configs/live_claims.json"
        and contract.get("sha256") == CONTRACT_SHA,
        "claim contract pin changed",
    )
    audit = sources.get("audit", {})
    require(
        audit.get("type") == "clean-room"
        and audit.get("network_access") is False
        and audit.get("author_executable_files") == [],
        "clean-room boundary changed",
    )

    claims = current_json("claims.json")
    require(isinstance(claims, dict), "claims.json is not an object")
    require(
        claims.get("repository") == f"MachineLearning-Nerd/{REPOSITORY}",
        "claims repository mismatch",
    )
    require(claims.get("publication_allowed") is False, "publication block changed")
    rows = claims.get("claims")
    require(isinstance(rows, list) and len(rows) == 4, "claims.json must contain four rows")
    require([row.get("status") for row in rows] == EXPECTED_STATUSES, "claim statuses changed")

    state = current_json("AUTONOMOUS_STATE.json")
    require(isinstance(state, dict), "state is not an object")
    require(state.get("phase") == "published_and_verified", "state is not final")
    require(state.get("publication_allowed") is False, "state publication block changed")
    require(state.get("branch_set") == ["main"], "state branch set changed")
    require(state.get("last_known_git_commit"), "state has no checkpoint commit")
    require(
        state.get("claim_statuses") == dict(zip(["C1", "C2", "C3", "C4"], EXPECTED_STATUSES)),
        "state claim statuses changed",
    )

    root_gate = current_json("publication_gate.json")
    output_gate = current_json("outputs/publication_gate.json")
    require(root_gate == output_gate, "root and output publication gates differ")
    require(
        root_gate.get("status") == "SCOPED_PASS"
        and root_gate.get("strict_status") == "NOT_READY"
        and root_gate.get("overall_status")
        == "VERIFIED_SCOPED_WITH_EXACT_FINITE_CONSTRUCTION_AUDIT"
        and root_gate.get("publication_gate_passed") is True
        and root_gate.get("score_forecast") is None,
        "publication gate changed",
    )
    require(
        "not a machine-checked replacement" in " ".join(root_gate.get("limitations", [])),
        "formal-proof limitation changed",
    )
    require(
        root_gate.get("source", {}).get("primary_pdf_sha256") == SOURCE_PDF_SHA
        and root_gate.get("source", {}).get("claim_contract_sha256") == CONTRACT_SHA
        and root_gate.get("source", {}).get("author_executable_files") == [],
        "publication source pins changed",
    )
    require(
        root_gate.get("verification", {}).get("claim_verdicts_sha256") == CLAIM_VERDICTS_SHA
        and root_gate.get("verification", {}).get("proof_audit_cells") == 108
        and root_gate.get("verification", {}).get("theorem4_witnesses") == 42
        and root_gate.get("verification", {}).get("theorem5_cells") == 3048,
        "publication verification counts changed",
    )

    verdicts = current_json("outputs/claim_verdicts.json")
    require(
        verdicts.get("all_claims_complete") is True
        and verdicts.get("possible_points") == 8
        and verdicts.get("verdicts") == ["verified"] * 4
        and verdicts.get("theorem4_witnesses") == 42
        and verdicts.get("theorem5_cells") == 3048,
        "claim verdict artifact changed",
    )
    require(sha256("outputs/claim_verdicts.json") == CLAIM_VERDICTS_SHA, "claim verdict hash changed")
    require(sha256("outputs/evidence_bundle.jsonl") == EVIDENCE_BUNDLE_SHA, "evidence bundle hash changed")
    require(sha256("outputs/artifact_manifest.json") == ARTIFACT_MANIFEST_SHA, "artifact manifest hash changed")
    require(len(current_bytes("outputs/evidence_bundle.jsonl").splitlines()) == 15, "evidence record count changed")

    require(len(current_bytes("outputs/theorem4_grid.csv").splitlines()) == 43, "Theorem 4 row count changed")
    require(
        len(current_bytes("outputs/theorem5_hard_family.csv").splitlines()) == 3049,
        "Theorem 5 row count changed",
    )
    require(len(current_bytes("outputs/proof_audit.csv").splitlines()) == 109, "proof audit row count changed")

    readme = current_bytes("README.md").decode()
    require("formal proof" in readme.lower(), "README proof boundary missing")
    require("author executable" in readme.lower(), "README author-code boundary missing")
    require("does not train" in readme.lower(), "README empirical boundary missing")

    tracked = run("git", "ls-files").splitlines()
    require(
        not any(
            path == ".trackio"
            or path.startswith(".trackio/")
            or path == "logbook.json"
            or path.endswith("/logbook.json")
            or "__pycache__" in path
            or path.startswith(".venv/")
            for path in tracked
        ),
        "stale private or generated state is tracked",
    )


def main() -> None:
    branches, commits = verify_git_state()
    verify_artifacts()
    verify_manifest()
    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={branches} commits={commits} "
        "claims=C1:verified_scoped,C2:verified_scoped,C3:verified_scoped,"
        "C4:verified_scoped publication_allowed=false"
    )


if __name__ == "__main__":
    main()
