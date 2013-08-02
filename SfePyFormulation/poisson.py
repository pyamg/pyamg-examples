from sfepy.fem.utils import refine_mesh
filename_mesh =  'cylinder.mesh'
refinement_level = 2
filename_mesh = refine_mesh(filename_mesh, refinement_level)

material_2 = {
    'name' : 'coef',
    'values' : {'val' : 1.0},
}

region_1000 = {
    'name' : 'Omega',
    'select' : 'elements of group 6',
}

region_03 = {
    'name' : 'Gamma_Left',
    'select' : 'nodes in (x < 0.00001)',
}

region_4 = {
    'name' : 'Gamma_Right',
    'select' : 'nodes in (x > 0.099999)',
}

field_1 = {
    'name' : 'temperature',
    'dtype' : 'real',
    'shape' : (1,),
    'region' : 'Omega',
    'approx_order' : 1,
}

variable_1 = {
    'name' : 't',
    'kind' : 'unknown field',
    'field' : 'temperature',
    'order' : 0, # order in the global vector of unknowns
}

variable_2 = {
    'name' : 's',
    'kind' : 'test field',
    'field' : 'temperature',
    'dual' : 't',
}

ebc_1 = {
    'name' : 't1',
    'region' : 'Gamma_Left',
    'dofs' : {'t.0' : 2.0},
}

ebc_2 = {
    'name' : 't2',
    'region' : 'Gamma_Right',
    'dofs' : {'t.0' : -2.0},
}

integral_1 = {
    'name' : 'i1',
    'kind' : 'v',
    'order' : 2,
}

equations = {
    'Temperature' : """dw_laplace.i1.Omega( coef.val, s, t ) = 0"""
}

#! Linear solver parameters
#! ---------------------------
solver_0a = {
    'name' : 'pyamg',
    'kind' : 'ls.pyamg',
    'method' : 'smoothed_aggregation_solver',
    'accel' : 'cg',
    'eps_r' : 1e-12,
}

#solver_0b = {
#    'name' : 'cg',
#    'kind' : 'ls.scipy_iterative',
#
#    'method' : 'cg',
#    'precond' : None,
#    'callback' : None,
#    'i_max' : 1000,
#    'eps_r' : 1e-12,
#}



#! Nonlinear solver parameters
#! ---------------------------
solver_1 = {
    'name' : 'newton',
    'kind' : 'nls.newton',

    'i_max'      : 1,
    'eps_a'      : 1e-10,
    'eps_r'      : 1.0,
    'macheps'   : 1e-16,
    'lin_red'    : 1e-2, # Linear system error < (eps_a * lin_red).
    'ls_red'     : 0.1,
    'ls_red_warp' : 0.001,
    'ls_on'      : 1.1,
    'ls_min'     : 1e-5,
    'check'     : 0,
    'delta'     : 1e-6,
    'is_plot'    : False,
    'problem'   : 'nonlinear', # 'nonlinear' or 'linear' (ignore i_max)
}

#! Options
#! -------
options = {
    'nls' : 'newton',
    'ls' : 'pyamg',
}
