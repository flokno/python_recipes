custom_params = {
        'supercell_matrix': [[2, 0, 0],
                             [0, 2, 0],
                             [0, 0, 2]],
        'distance': 0.02,
        }

_default_params = {
        'supercell_matrix': [[1, 0, 0],
                             [0, 1, 0],
                             [0, 0, 1]],
        'symprec': 1e-5,
        'is_symmetry': True,
        'distance': 0.01,
        'q_mesh': [35, 35, 35]
        }

# concatenate params
params = {**_default_params, **custom_params}
