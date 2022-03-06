# 3D example of viewing aggregates from SA using VTK
import pyamg
import pyamg.vis

# retrieve the problem
data = pyamg.gallery.load_example('unit_cube')
A = data['A'].tocsr()
V = data['vertices']
E2V = data['elements']

# perform smoothed aggregation
AggOp, rootnodes = pyamg.aggregation.standard_aggregation(A)

# create the vtk file of aggregates
pyamg.vis.vis_coarse.vis_aggregate_groups(V=V, E2V=E2V, AggOp=AggOp,
                                          mesh_type='tet', fname='output_aggs.vtu')

# create the vtk file for a mesh
pyamg.vis.vtk_writer.write_basic_mesh(V=V, E2V=E2V,
                                      mesh_type='tet', fname='output_mesh.vtu')

# to use Paraview:
# start Paraview: Paraview --data=output_mesh.vtu
# apply
# under display in the object inspector:
#           select wireframe representation
#           select a better solid color
#           selecting surface with edges and low opacity also helps
# open file: output_aggs.vtu
# under display in the object inspector:
#           select surface with edges representation
#           select a better solid color
#           increase line width and point size to see these aggs (if present)
#           reduce the opacity, sometimes helps
