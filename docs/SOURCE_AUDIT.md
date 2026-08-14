# Source audit

- Paper: *Barriers to Counterfactual Credit Attribution for Autoregressive Models*
- Authors: Aloni Cohen; Chenhao Zhang
- arXiv record: [2605.01425](https://arxiv.org/abs/2605.01425)
- Pinned version: `v1`
- Local source artifact: `docs/primary.pdf`
- SHA-256: `bb03dbafca39e5c0cf19d44bf6b1982d65736a6314370d6ec90d1e87c3890f34`
- PDF pages: 27
- License: CC BY 4.0 as listed by the arXiv record

The repository stores the paper PDF rather than an arXiv TeX source archive.
The PDF supplies the theorem and definition anchors used by the audit. A
repository scan found no author Python, R, Julia, shell, or notebook
executable. The files under `repro/` are independent clean-room code written
for this audit and are not presented as author code.

The challenge claim contract is stored at
`repro/configs/live_claims.json` and is hash-recorded in `sources.json`.
