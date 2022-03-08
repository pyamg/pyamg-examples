In this this example, smoothed aggregation AMG is used to precondition the
LOBPCG eigensolver to find the lowest nine eigenmodes of a Poisson problem.
With preconditioning (`M=M` in the `loppcg` call), the computation of the
eigensubspace is extremely fast.
