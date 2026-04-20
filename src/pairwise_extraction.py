import os
import numpy as np
from scipy.spatial.distance import cdist

PROTEIN_ATOMS = ['C', 'N', 'O', 'S']
LIGAND_ATOMS = ['C', 'N', 'O', 'S', 'P', 'F', 'Cl', 'Br', 'I']


def extract_pairwise_pdbs(base_dir, pdbid, cutoff=12.0):
    folder = os.path.join(base_dir, pdbid)
    out_dir = os.path.join(folder, "pairwise")
    os.makedirs(out_dir, exist_ok=True)

    # Dummy placeholder (replace with your real extraction)
    # Here we just create fake files so pipeline runs
    for l in LIGAND_ATOMS:
        for p in PROTEIN_ATOMS:
            fname = os.path.join(out_dir, f"{l}_{p}.pdb")
            with open(fname, "w") as f:
                f.write("END\n")

    return out_dir
