The smoothed aggregation solver supports nonsymmetric (i.e., non-Hermitian) and
indefinite matrices, through recent advances in multigrid research. The
demo highlighted here constructs a solver for a small nonsymmetric
recirculating flow problem.  The out-of-the-box example diverges,
while more advanced options yield a convergent solver.

Using

```python
python demo.py --solver 1
```

we observe the following convergence history.
