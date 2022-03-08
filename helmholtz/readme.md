The example focusses on the indefinite Helmholtz wave problem.  The first
part highlights the value in using waves to represent the near-null space, `B`.
In addition, we observe the waves to resemble the  (lowest) right singular vectors
of the problem.

In the case of 2D, discontinuous Galerkin is used, yielding multiple
degrees of freedom at each spatial location.  As a result,
the fine level (level-0) aggregates of the discontinuous
elements, largely group neighboring vertices.  The wave-like near
null-space is then enforced on the first coarse grid (level-1), resulting
in four modes.
