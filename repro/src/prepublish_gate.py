"""Fail-closed local gate for the four-claim reproduction."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PAPER="F8dIPCR1ly"
def need(ok:bool,msg:str)->None:
 if not ok: raise RuntimeError(msg)
def main()->None:
 verdict=json.loads((ROOT/"outputs/claim_verdicts.json").read_text())
 need(verdict["all_claims_complete"] is True and verdict["verdicts"]==["verified"]*4,"claims incomplete")
 bundle=ROOT/"outputs/evidence_bundle.jsonl"; need(bundle.is_file() and bundle.stat().st_size>0,"missing bundle")
 rows=[json.loads(x) for x in bundle.read_text().splitlines()]
 need(len(rows)==10 and len({r["path"] for r in rows})==10,"bundle records")
 for row in rows:
  data=(ROOT/row["path"]).read_bytes(); need(len(data)==row["bytes"],"bundle size drift"); need(hashlib.sha256(data).hexdigest()==row["sha256"],"bundle hash drift")
 meta=json.loads((ROOT/".trackio/metadata.json").read_text())
 need(meta["space_id"]==f"DineshAI/{PAPER}" and set(meta["tags"])=={"icml2026-repro",f"paper-{PAPER}"},"metadata")
 art=meta["local_path_artifacts"]; need(len(art)==1 and art[0]["path"]=="outputs/evidence_bundle.jsonl" and art[0]["size"]==bundle.stat().st_size,"artifact registration")
 pages={p.parent.name for p in (ROOT/".trackio/logbook/pages").glob("*/page.md")}
 need({"overview","claim-1","claim-2","claim-3","claim-4","methods","negative-controls","conclusion"}<=pages,"missing pages")
 c=(ROOT/".trackio/logbook/pages/conclusion/page.md").read_text()
 need(c.count('"pinned": true')==1 and "FULL_GATE_READY: F8dIPCR1ly" in c,"pinned conclusion")
 out={"paper":PAPER,"tests_passed":True,"gate":True,"publication_gate_passed":True,"bundle_bytes":bundle.stat().st_size,"bundle_sha256":hashlib.sha256(bundle.read_bytes()).hexdigest()}
 (ROOT/"outputs/PUBLICATION_GATE_PASSED.json").write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
