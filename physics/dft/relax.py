import numpy as np

from ase.io import read
from ase.constraints import UnitCellFilter
from ase.optimize import BFGSLineSearch as BFGS
from ase.calculators.socketio import SocketIOCalculator
from ase.calculators.aims import Aims

# read input geometry that should be relaxed
atoms = read("geometry.in", 0, "aims")

# user settings (adjust!)
# choose a name for an aims working directory
workdir = "aims"
port = 12345
log_name = "relax.log"
trajectory_name = "relax.traj"

usr_settings = {
    "aims_command": "srun aims.x",
    "species_dir": "/u/fknoop/working/species_defaults/light",
    "output_level": "MD_light",
    "outfilename": "aims.out",
}

# dft settings (adjust!)
dft_settings = {
    "xc": "pbe",
    "relativistic": "atomic_zora scalar",
    "vdw_correction_hirshfeld": True,
    "sc_accuracy_rho": 1e-6,
    "k_grid": [8, 8, 12],
    "compute_forces": True,
    "compute_analytical_stress": True,
}

# some more settings that can stay untouched
aux_settings = {"label": workdir, "use_pimd_wrapper": ("localhost", port)}

# create Aims calculator from the settings
calc = Aims(**usr_settings, **dft_settings, **aux_settings)

# Create a filter to expose the lattice degrees of freedom to the optimizer
opt_atoms = UnitCellFilter(atoms)

# choose an optimizer
optimizer = BFGS


# function to make sure the structure stays tetragonal
def tetragonalize(atoms):
    """ make the lattice of atoms object tetragonal """
    cell = atoms.cell
    scaled_pos = atoms.get_scaled_positions()

    a = (cell[0, 0] + cell[1, 1]) / 2
    c = cell[2, 2]

    new_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, c]])

    atoms.cell = new_cell
    atoms.set_scaled_positions(scaled_pos)


# run the optimization and write out every step
with SocketIOCalculator(calc, log="socketio.log", port=port) as calc:
    atoms.set_calculator(calc)
    # create the optimizer for the filtered atoms object
    opt = optimizer(opt_atoms, logfile=log_name, trajectory=trajectory_name)
    for ii, _ in enumerate(opt.irun(fmax=0.001, steps=20)):
        # tetragonalize the structure
        tetragonalize(atoms)
        # write out every intermediate structure (not necessary)
        atoms.write(f"{workdir}/geometry.in.next.{ii}", "aims", scaled=True)

# write final result
atoms.write("geometry.out", "aims", scaled=True)
