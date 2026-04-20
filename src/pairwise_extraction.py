"""
Extract pairwise atom environments for EP-3DZD.
"""

import numpy as np
from scipy.spatial.distance import cdist

PROTEIN_ATOMS = ['C', 'N', 'O', 'S']
LIGAND_ATOMS = ['H', 'C', 'N', 'O', 'S', 'P', 'F', 'Cl', 'Br', 'I']

def extract_pairs(protein_df, ligand_df, cutoff=12.0):
    pairs = {}

    for l_type in LIGAND_ATOMS:
        for p_type in PROTEIN_ATOMS:

            p_atoms = protein_df[protein_df['element'] == p_type]
            l_atoms = ligand_df[ligand_df['element'] == l_type]

            if len(p_atoms) == 0 or len(l_atoms) == 0:
                continue

            d = cdist(
                p_atoms[['x_coord','y_coord','z_coord']],
                l_atoms[['x_coord','y_coord','z_coord']]
            )

            if (d <= cutoff).any():
                pairs[f"{l_type}_{p_type}"] = True

    return pairs
