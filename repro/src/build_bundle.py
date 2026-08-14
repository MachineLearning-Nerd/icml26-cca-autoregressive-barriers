"""Create the public, hash-bound evidence bundle."""
from __future__ import annotations
import base64, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PATHS=(
 "docs/primary.pdf","docs/independent_proof_audit.md","docs/CLAIM_EVIDENCE.md",
 "sources.json","outputs/theorem4_grid.csv","outputs/theorem5_hard_family.csv",
 "outputs/proof_audit.csv","outputs/claim_verdicts.json","repro/configs/live_claims.json",
 "repro/src/theorem4.py","repro/src/theorem5.py","repro/src/proof_audits.py",
 "repro/src/run_theorem4.py","repro/src/run_theorem5.py","repro/src/verify_claims.py",
)
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def main()->None:
 rows=[]
 for rel in PATHS:
  data=(ROOT/rel).read_bytes()
  rows.append({"path":rel,"bytes":len(data),"sha256":sha(data),"payload_b64":base64.b64encode(data).decode()})
 out=ROOT/"outputs/evidence_bundle.jsonl"
 out.write_text("\n".join(json.dumps(row,sort_keys=True,separators=(",",":")) for row in rows)+"\n")
 print(json.dumps({"records":len(rows),"bytes":out.stat().st_size,"sha256":sha(out.read_bytes())}))
if __name__=="__main__":main()
