# Environment and verification boundary

## Pinned audit command

The repository's deterministic gate uses Python 3.12 and the pinned
requirements:

~~~sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r repro/requirements.txt
.venv/bin/python repro/src/publication_gate.py
~~~

The gate reruns the finite theorem producers, proof audits, focused tests,
evidence bundle, and artifact manifest. It does not use network access or
author executables.

## Lightweight final-state check

After the committed gate has been reviewed:

~~~sh
python3 verify_final.py
~~~

This check reads the committed artifacts and queries the live GitHub branch
state. It intentionally does not rerun the full producer suite.

## Resource boundary

This is a theory-paper audit. There is no GPU run, model training, dataset
pipeline, or checkpoint to reproduce. The finite LP and state-space checks are
deterministic CPU evidence for the displayed constructions.
