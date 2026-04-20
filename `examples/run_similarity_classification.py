#!/usr/bin/env python
"""
Run binding similarity classification using EP-3DZD features.
"""

import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

def load_features(path):
    data = np.load(path, allow_pickle=True)
    return data['features_dict'].item()

def create_pairs(labels_df, threshold=1.5):
    pairs = []

    pdbids = labels_df['PDBID'].tolist()
    pk = labels_df['pK'].tolist()

    for i in range(len(pdbids)):
        for j in range(i+1, len(pdbids)):
            diff = abs(pk[i] - pk[j])

            if diff < threshold:
                label = 1
            elif diff < 3.0:
                label = 0
            else:
                continue

            pairs.append((pdbids[i], pdbids[j], label))

    return pairs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--features', type=str, required=True)
    parser.add_argument('--labels', type=str, required=True)
    args = parser.parse_args()

    feat_dict = load_features(args.features)
    labels_df = pd.read_csv(args.labels)

    pairs = create_pairs(labels_df)

    X, y = [], []

    for p1, p2, label in pairs:
        if p1 in feat_dict and p2 in feat_dict:
            f1, f2 = feat_dict[p1], feat_dict[p2]

            # Improved representation
            feat = np.concatenate([f1, f2, np.abs(f1 - f2)])

            X.append(feat)
            y.append(label)

    X = np.array(X)
    y = np.array(y)

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    aucs = []

    for train, test in cv.split(X, y):
        model.fit(X[train], y[train])
        pred = model.predict_proba(X[test])[:, 1]
        aucs.append(roc_auc_score(y[test], pred))

    print(f"AUC: {np.mean(aucs):.4f} ± {np.std(aucs):.4f}")


if __name__ == "__main__":
    main()
