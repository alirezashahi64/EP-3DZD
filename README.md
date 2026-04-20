# EP-3DZD

This repository provides an implementation of **Element-Pair 3D Zernike Descriptors (EP-3DZD)** for:

* Protein–ligand **binding affinity prediction** (regression)
* Binding site **similarity analysis** (classification, AUC-ROC)

The framework enables systematic comparison between:

* **EP-3DZD** (shape-based descriptors)
* **EIM (Element Interaction Matrix)** features
* **Combined representations (EIM + EP-3DZD)**

---



## ⚙️ Method Overview

EP-3DZD encodes **protein–ligand interactions** using **element-pair-specific 3D Zernike descriptors**.

### 🔬 Core Idea

Instead of computing global descriptors, EP-3DZD:

1. Decomposes interactions into **element pairs** (e.g., C–O, N–S)
2. Extracts **local contact regions** within a cutoff distance
3. Converts regions into **3D volumetric representations**
4. Computes **rotation-invariant Zernike moments**

---

## 🧩 Feature Construction Pipeline

1. **Pairwise Extraction**

   * Protein atoms: `C, N, O, S`
   * Ligand atoms: `H, C, N, O, S, P, F, Cl, Br, I`
   * Distance cutoff: ~12 Å

2. **Surface Generation**

   * External tool: **EDTSurf**

3. **Voxelization**

   * Using `obj2grid`

4. **Zernike Descriptor Computation**

   * Using `map2zernike`

5. **Feature Assembly**

   * Concatenate descriptors across element pairs
   * Missing pairs → zero-padded

---

## 🚀 Feature Extraction

Run:

```
python examples/compute_ep3dzd_features.py \
    --input_dir /path/to/pdbbind \
    --output_file results/ep3dzd_features.npz \
    --num_complexes 100
```

---

## 📌 Output Format

```
{
    "features_dict": {
        "1abc": np.array([...]),
        "2xyz": np.array([...])
    }
}
```

---

## 🤖 Binding Affinity Prediction (Regression)

Run:

```
python run_regression.py \
    --features results/ep3dzd_features.npz \
    --labels data/PDBbind_labels.csv
```

### Metrics

* R²
* RMSE

---

## 🔬 Binding Site Similarity (Classification)

Run:

```
python run_similarity_classification.py \
    --features results/ep3dzd_features.npz \
    --labels data/PDBbind_labels.csv
```

### Pair Definition

* Similar: |ΔpK| < 1.5 → label = 1
* Dissimilar: 1.5 ≤ |ΔpK| < 3.0 → label = 0

### Evaluation

* ROC Curve
* AUC Score

---

## 📊 Dataset

Designed for:

* **PDBbind v2016 Refined Set**

Expected structure:

```
pdbbind_v2016_general-set/
└── general-set/
    ├── XXXX/
    │   ├── XXXX_protein.pdb
    │   └── XXXX_ligand.sdf
```

---

## ⚠️ External Dependencies (IMPORTANT)

This pipeline requires external executables:

* EDTSurf
* obj2grid
* map2zernike

These are **not included** in this repository.

You must:

* Download them separately
* Compile if necessary
* Update paths in the pipeline

---

## ⚠️ Notes

* Feature extraction is **computationally intensive**
* Recommended to run on **HPC / SLURM environments**
* Missing or invalid structures are skipped automatically
* Feature vectors are zero-padded when necessary

---

## 📌 Summary of Capabilities

| Task               | Method                         |
| ------------------ | ------------------------------ |
| Feature Extraction | Element-Pair 3D Zernike        |
| Representation     | Rotation-invariant descriptors |
| Regression         | Random Forest / Boosting       |
| Similarity         | Pairwise classification        |
| Evaluation         | R², RMSE, AUC                  |

---

## 🔍 Comparison with EIM

| Property     | EP-3DZD            | EIM                |
| ------------ | ------------------ | ------------------ |
| Feature Type | Shape-based        | Interaction-based  |
| Invariance   | Rotation-invariant | Not inherent       |
| Complexity   | High               | Moderate           |
| Performance  | Moderate           | Typically stronger |

Combining both often yields improved performance.

---

## 🔧 Future Work

* Full robust pipeline integration (checkpoint + resume)
* Group-aware cross-validation (avoid data leakage)
* Feature fusion strategies
* Deep learning models on descriptors
* GPU acceleration

---

## 📜 License

MIT License

---

## ✍️ Citation

(To be added)
