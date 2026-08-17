# Normalized branch audit

The collection repository has exactly one published branch:

| Branch | Role | Publication boundary |
| --- | --- | --- |
| <code>main</code> | Canonical README, pinned paper, finite producers, tests, evidence, and publication gate | Default and only public branch |

There are no <code>master</code>, <code>orx/*</code>, experiment, author-code,
or stale queue branches. This is intentional: the repository is a clean-room
theory audit and does not hide alternative reproduction variants.

All reachable commits use:

    MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>

No co-author trailer is permitted. The final-state verifier checks the live
remote branch set, default branch, canonical history identity, and absence of
stale Git refs.
