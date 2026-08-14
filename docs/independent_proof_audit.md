# Independent proof audit

This audit re-derives the logical steps used for the two universal claims. It
uses the definitions in arXiv:2605.01425 rather than any author implementation.

## Theorem 4.3

Fix an uncredited trace `w=((x_j,C'_j))_{j=1}^L`. Let `P` be the trace law
with the document and `Q` the no-document trace law. Autoregressive calls only
receive prior tokens, not prior credit sets, hence

`P(w_j | w_{<j}) = M_S(w_j | x_{<j})`.

Since the trace is uncredited, write `E_j={s_i not in C'_j}`. Factor every
term as

`M_S(w_j | x_{<j}) = M_S(w_j | E_j,x_{<j}) P(E_j | x_{<j})`.

The per-token epsilon-CCA hypothesis gives

`M_S(w_j | E_j,x_{<j}) >= exp(-epsilon) M_{S-i}(w_j | x_{<j})`.

Multiplying the `L` terms and applying the chain rule to `Q` yields

`P(w) >= exp(-L epsilon) Q(w) product_j P(E_j | x_{<j})`.

Summing over every trace with the same generated output and credit set, then
dividing by `P(s_i not credited)`, gives exactly the lower bound printed in
Theorem 4.3. If the rollout is epsilon-prime-CCA, its opposite likelihood
bound implies the theorem after a logarithm and maximum over uncredited
outputs. `proof_audits.py` independently evaluates this multiplication and
normalization on 24 branching trace systems; `theorem4.py` evaluates the
paper's strict counterexample separately.

## Lemmas 5.6, 5.8, and 5.9 imply Theorem 5.5

For a fixed prompt, preserve the original output law `p_y` and let `r_y` be
the conditional probability of withholding credit after output `y`. Writing
`R=sum_y r_y p_y`, the two pure-CCA likelihood inequalities become the linear
constraints

`exp(-epsilon) q_y R <= r_y p_y <= exp(epsilon) q_y R`.

Thus maximizing `R` is exactly minimizing credit. For the published hard
family, the exceptional `z||0` output has

`p_y/q_y = exp(-epsilon)(1-gamma)`.

It follows for any feasible point that `R <= 1-gamma`. The interval
construction in Appendix B attains this bound; independently formulated
HiGHS LPs recover credit `gamma` in every one of the 72 recorded
`(ell,z,epsilon,gamma)` proof-audit cells (`ell=2..7`). The broader producer
grid records all 3,048 hard-family cells for `ell=1..7`.

For Lemma 5.8, until querying the sole exceptional prompt `z`, every model in
the `2^ell`-member family returns the identical full distribution. Under a
uniform hidden `z`, `q` exceptional queries and one final guess have success
at most `(q+1)/2^ell`; success at least `2/3` requires
`q >= ceil(2*2^ell/3-1)`, an Omega(`2^ell`) lower bound.

Lemma 5.9 supplies a prefix-recovery algorithm from an alpha-approximate
augmentation: correct prefixes have credit probability `gamma`, incorrect
ones zero. Thresholding estimates at `gamma/2` uses
`O(ell log(ell)/(gamma-2 alpha)^2)` samples by Hoeffding plus a union bound.
Composing any retrofit oracle with this recovery procedure contradicts the
Lemma-5.8 query lower bound unless it makes

`Omega(2^ell (gamma-2 alpha)^2 /(ell log(12 ell)))`

base-model queries. For every `alpha<1/2`, selecting a permitted
`gamma in (2 alpha,1)` gives the stated exponential lower bound.
