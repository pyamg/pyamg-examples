In this example, we compute a partition of a basic cracked mesh (`crack_mesh.mat`)
using the Fiedler vector (the second lowest eigenmode of the graph laplacian).
We construct a SA-AMG preconditioner to assist LOBPCG in finding the Fiedler
vector.  Positive/negative values of the Fiedler vector are plotted in
different colors, illustrating the natural splitting this mesh.
