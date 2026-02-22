"""
estimator_credibility.py

Credibility diagnostics for information estimators (Simple_Binning, KSG).

What it reports
---------------
1) Subsample stability curve (mean/std vs sample size)
2) Bootstrap confidence interval (percentile CI)
3) Permutation (surrogate) null test and p-value
4) Sensitivity sweep (KSG k sweep; optional binning parameters)
5) Optional synthetic ground-truth benchmarks

Usage examples
--------------
# Example 1: run on synthetic Gaussian MI
python -m on_Model.Utils.estimator_credibility --synthetic gaussian_mi --rho 0.6 --N 5000

# Example 2: run on saved ensemble file (CSV-like / txt) with named columns
python -m on_Model.Utils.estimator_credibility --data path/to/ensemble.npy --vars X Y --estimator ksg --k 10

Design notes
------------
- "Credibility" here means numerical stability + uncertainty, not philosophical truth.
- High-dimensional conditioning can have huge variance; the script reveals that via instability.
"""

from __future__ import annotations
import argparse
import math
import os
import sys
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

# Optional: use scipy for digamma / stats if available
try:
    import scipy.linalg
except Exception:
    scipy = None


# ----------------------------
# Synthetic data generators
# ----------------------------
def synth_gaussian_mi(N: int, rho: float, seed: int = 0) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Bivariate Gaussian with correlation rho.
    Ground truth MI: I = -0.5 * log(1 - rho^2)   (nats)
    """
    rng = np.random.default_rng(seed)
    mean = np.zeros(2)
    cov = np.array([[1.0, rho], [rho, 1.0]])
    XY = rng.multivariate_normal(mean, cov, size=N)
    I_true = -0.5 * math.log(1.0 - rho * rho)
    return XY, {"I_true_nats": I_true, "rho": rho}


def synth_gaussian_cmi(N: int, rho_xy: float, rho_xz: float, rho_yz: float, seed: int = 0) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Trivariate Gaussian (X,Y,Z) with specified pairwise correlations.
    Ground truth CMI: I(X;Y|Z) = -0.5 * log(1 - rho_xy·z^2)
    where rho_xy·z is the partial correlation.

    Note: correlation matrix must be PSD; caller should choose valid parameters.
    """
    rng = np.random.default_rng(seed)
    R = np.array([
        [1.0,   rho_xy, rho_xz],
        [rho_xy, 1.0,   rho_yz],
        [rho_xz, rho_yz, 1.0],
    ])
    # draw
    mean = np.zeros(3)
    XYZ = rng.multivariate_normal(mean, R, size=N)

    # partial correlation rho_xy·z:
    # rho_xy·z = (rho_xy - rho_xz*rho_yz) / sqrt((1-rho_xz^2)(1-rho_yz^2))
    denom = math.sqrt((1.0 - rho_xz**2) * (1.0 - rho_yz**2))
    rho_partial = (rho_xy - rho_xz * rho_yz) / denom
    I_true = -0.5 * math.log(1.0 - rho_partial**2)
    return XYZ, {"I_true_nats": I_true, "rho_partial": rho_partial}


def synth_binary_channel(N: int, p: float, q: float, seed: int = 0) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Discrete binary channel:
    X ~ Bernoulli(p)
    Y = X flipped with prob q
    Computes ground truth MI (nats) from exact distribution.
    """
    rng = np.random.default_rng(seed)
    X = (rng.random(N) < p).astype(int)
    flip = (rng.random(N) < q).astype(int)
    Y = (X ^ flip).astype(int)

    # exact distribution
    # P(X=1)=p
    # P(Y=1|X=1)=1-q, P(Y=1|X=0)=q
    # P(Y=1)= p(1-q)+(1-p)q
    py1 = p * (1 - q) + (1 - p) * q
    py0 = 1 - py1

    # joint
    p11 = p * (1 - q)
    p10 = p * q
    p01 = (1 - p) * q
    p00 = (1 - p) * (1 - q)

    # MI = sum pxy log(pxy/(px py))
    def term(pxy, px, py):
        return 0.0 if pxy <= 0 else pxy * math.log(pxy / (px * py))

    I = (
        term(p11, p, py1) +
        term(p10, p, py0) +
        term(p01, 1 - p, py1) +
        term(p00, 1 - p, py0)
    )
    E = np.column_stack([X, Y])
    return E, {"I_true_nats": I, "p": p, "q": q}


# ----------------------------
# Utility diagnostics
# ----------------------------
@dataclass
class DiagnosticResult:
    point_estimate: float
    bootstrap_ci: Optional[Tuple[float, float]]
    perm_pvalue: Optional[float]
    stability_curve: Optional[List[Tuple[int, float, float]]]
    sensitivity: Optional[List[Tuple[str, float]]]


def bootstrap_ci(estimator_fn: Callable[[np.ndarray], float],
                 data: np.ndarray,
                 B: int = 200,
                 seed: int = 0,
                 alpha: float = 0.05) -> Tuple[float, float]:
    rng = np.random.default_rng(seed)
    N = data.shape[0]
    vals = np.empty(B, dtype=float)
    for b in range(B):
        idx = rng.integers(0, N, size=N)
        vals[b] = estimator_fn(data[idx])
    lo = np.quantile(vals, alpha / 2)
    hi = np.quantile(vals, 1 - alpha / 2)
    return float(lo), float(hi)


def permutation_test(estimator_fn: Callable[[np.ndarray], float],
                     data: np.ndarray,
                     y_col: int,
                     P: int = 200,
                     seed: int = 0) -> Tuple[float, float]:
    """
    Permute one column (usually Y) to destroy dependence.
    Returns (p_value, null_mean).
    """
    rng = np.random.default_rng(seed)
    obs = estimator_fn(data)
    N = data.shape[0]
    null = np.empty(P, dtype=float)
    for p in range(P):
        perm = rng.permutation(N)
        d = data.copy()
        d[:, y_col] = d[perm, y_col]
        null[p] = estimator_fn(d)
    # two-sided p-value
    pval = (np.sum(np.abs(null) >= abs(obs)) + 1) / (P + 1)
    return float(pval), float(null.mean())


def stability_curve(estimator_fn: Callable[[np.ndarray], float],
                    data: np.ndarray,
                    sizes: Sequence[int],
                    R: int = 30,
                    seed: int = 0) -> List[Tuple[int, float, float]]:
    """
    For each subsample size n, compute R estimates and report mean/std.
    """
    rng = np.random.default_rng(seed)
    N = data.shape[0]
    out: List[Tuple[int, float, float]] = []
    for n in sizes:
        n = int(n)
        if n >= N:
            n = N
        vals = np.empty(R, dtype=float)
        for r in range(R):
            idx = rng.choice(N, size=n, replace=False)
            vals[r] = estimator_fn(data[idx])
        out.append((n, float(vals.mean()), float(vals.std(ddof=1))))
    return out


# ----------------------------
# Wrappers for your estimators
# ----------------------------
def make_ksg_estimator(k: int):
    """
    Minimal wrapper: expects your on_Model.InfoDyn_lib.Estimators.KSG.Estimator
    to accept parameter k (adjust if your signature differs).
    """
    from on_Model.InfoDyn_lib.Estimators import KSG
    est = KSG.Estimator(k=k) if "k" in KSG.Estimator.__init__.__code__.co_varnames else KSG.Estimator(k)
    return est


def make_binning_estimator(Q: int, dimension: int):
    from on_Model.InfoDyn_lib.Estimators import Simple_Binning
    return Simple_Binning.Estimator(Q, dimension)


def estimator_fn_from_spec(spec: str,
                           measure: str,
                           var_names: List[str],
                           known_names: List[str],
                           k: int,
                           Q: int) -> Callable[[np.ndarray], float]:
    """
    Returns a function f(data_array)-> estimate (float).

    Assumes `data_array` columns correspond to var_names in the same order.
    """
    measure = measure.lower()

    if spec == "ksg":
        est = make_ksg_estimator(k)

        def f(arr: np.ndarray) -> float:
            # Build a temporary Source-like structure expected by your KSG estimator
            # Your KSG expects est.Source.Ensemble and est.Source.Variable_Names.
            est.Source.Ensemble = arr
            est.Source.Variable_Names = var_names
            if measure == "h":
                return float(est.Entropy(For=[var_names[0]]))
            if measure == "mi":
                return float(est.Mutual_Information(For=[var_names[0], var_names[1]]))
            if measure == "cmi":
                return float(est.Conditional_Mutual_Information(For=[var_names[0], var_names[1]], Known=known_names))
            raise ValueError(f"Unknown measure: {measure}")
        return f

    if spec == "binning":
        # For binning, Q and dimension must match the joint dimension you will feed.
        # Here we assume all variables are discrete scalars and dimension = number of columns in arr.
        dim = len(var_names)
        est = make_binning_estimator(Q=Q, dimension=dim)

        def f(arr: np.ndarray) -> float:
            est.Source.Ensemble = arr.astype(int)
            est.Source.Variable_Names = var_names
            if measure == "h":
                return float(est.Entropy(For=[var_names[0]]))
            if measure == "mi":
                return float(est.Mutual_Information(For=[var_names[0], var_names[1]]))
            if measure == "cmi":
                # if your binning estimator supports CMI; otherwise compute from entropies:
                # I(X;Y|Z) = H(X,Z)+H(Y,Z)-H(Z)-H(X,Y,Z)
                if hasattr(est, "Conditional_Mutual_Information"):
                    return float(est.Conditional_Mutual_Information(For=[var_names[0], var_names[1]], Known=known_names))
                # entropy-based fallback:
                X, Y = var_names[0], var_names[1]
                Z = known_names
                Hxz = float(est.Entropy(For=[X] + Z))
                Hyz = float(est.Entropy(For=[Y] + Z))
                Hz  = float(est.Entropy(For=Z))
                Hxyz = float(est.Entropy(For=[X, Y] + Z))
                return Hxz + Hyz - Hz - Hxyz
            raise ValueError(f"Unknown measure: {measure}")
        return f

    raise ValueError(f"Unknown estimator spec: {spec}")


# ----------------------------
# Main CLI
# ----------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--estimator", choices=["ksg", "binning"], default="ksg")
    ap.add_argument("--measure", choices=["h", "mi", "cmi"], default="mi")

    # Data input
    ap.add_argument("--data", type=str, default="")
    ap.add_argument("--vars", nargs="+", default=["X", "Y"], help="Variable names in column order (>=2 for MI)")
    ap.add_argument("--known", nargs="*", default=[], help="Known variable names (must be included in --vars/columns)")

    # Estimator params
    ap.add_argument("--k", type=int, default=10, help="KSG k")
    ap.add_argument("--Q", type=int, default=2, help="Binning alphabet size")

    # Diagnostics params
    ap.add_argument("--bootstrap", type=int, default=200)
    ap.add_argument("--perm", type=int, default=200)
    ap.add_argument("--stability_R", type=int, default=30)
    ap.add_argument("--seed", type=int, default=0)

    # Synthetic
    ap.add_argument("--synthetic", choices=["", "gaussian_mi", "gaussian_cmi", "binary_channel"], default="")
    ap.add_argument("--N", type=int, default=5000)
    ap.add_argument("--rho", type=float, default=0.6)
    ap.add_argument("--rho_xy", type=float, default=0.5)
    ap.add_argument("--rho_xz", type=float, default=0.4)
    ap.add_argument("--rho_yz", type=float, default=0.3)
    ap.add_argument("--p", type=float, default=0.5)
    ap.add_argument("--q", type=float, default=0.1)

    ap.add_argument("--k_sweep", nargs="*", type=int, default=[3, 5, 8, 10, 15, 20])

    args = ap.parse_args()

    # Load/generate data
    truth = {}
    if args.synthetic:
        if args.synthetic == "gaussian_mi":
            data, truth = synth_gaussian_mi(args.N, args.rho, seed=args.seed)
            args.vars = ["X", "Y"]
            args.known = []
        elif args.synthetic == "gaussian_cmi":
            data, truth = synth_gaussian_cmi(args.N, args.rho_xy, args.rho_xz, args.rho_yz, seed=args.seed)
            args.vars = ["X", "Y", "Z"]
            args.known = ["Z"]
            args.measure = "cmi"
        elif args.synthetic == "binary_channel":
            data, truth = synth_binary_channel(args.N, args.p, args.q, seed=args.seed)
            args.vars = ["X", "Y"]
            args.known = []
            args.estimator = "binning"
            args.measure = "mi"
        else:
            raise ValueError("Unknown synthetic option")
    else:
        if not args.data:
            print("Provide --data or --synthetic", file=sys.stderr)
            sys.exit(2)
        # Expected: .npy containing (N, d) array in the same order as args.vars
        data = np.load(args.data)

    var_names = list(args.vars)
    known_names = list(args.known)

    # Main estimator function
    f = estimator_fn_from_spec(args.estimator, args.measure, var_names, known_names, args.k, args.Q)

    # Point estimate
    point = f(data)

    # Bootstrap CI
    ci = bootstrap_ci(f, data, B=args.bootstrap, seed=args.seed) if args.bootstrap > 0 else None

    # Permutation test (permute Y column for MI/CMI)
    pval = None
    null_mean = None
    if args.perm > 0 and args.measure in ("mi", "cmi"):
        y_col = 1  # assume second column corresponds to Y in vars
        pval, null_mean = permutation_test(f, data, y_col=y_col, P=args.perm, seed=args.seed)

    # Stability curve
    sizes = []
    N = data.shape[0]
    for n in [200, 500, 1000, 2000, 5000, 10000, 20000]:
        if n < N:
            sizes.append(n)
    sizes.append(N)
    curve = stability_curve(f, data, sizes=sizes, R=args.stability_R, seed=args.seed) if args.stability_R > 0 else None

    # Sensitivity sweep (KSG only)
    sens = None
    if args.estimator == "ksg" and args.k_sweep:
        sens = []
        for kk in args.k_sweep:
            ff = estimator_fn_from_spec("ksg", args.measure, var_names, known_names, kk, args.Q)
            sens.append((f"k={kk}", float(ff(data))))

    # Print report
    print("\n=== Estimator Credibility Report ===")
    print(f"Estimator: {args.estimator}")
    print(f"Measure:   {args.measure}")
    print(f"N:         {data.shape[0]}")
    print(f"Vars:      {var_names}")
    if known_names:
        print(f"Known:     {known_names}")
    if args.estimator == "ksg":
        print(f"k:         {args.k}")
    if args.estimator == "binning":
        print(f"Q:         {args.Q}")

    if truth:
        for k, v in truth.items():
            print(f"Truth {k}: {v:.6g}" if isinstance(v, (int, float)) else f"Truth {k}: {v}")

    print(f"\nPoint estimate: {point:.6g}")
    if ci is not None:
        print(f"Bootstrap {95}% CI: [{ci[0]:.6g}, {ci[1]:.6g}]")
    if pval is not None:
        print(f"Permutation p-value (permute Y): {pval:.6g}")
        print(f"Null mean: {null_mean:.6g}")

    if curve is not None:
        print("\nStability curve (subsample size, mean, std):")
        for n, m, s in curve:
            print(f"  n={n:6d}  mean={m:.6g}  std={s:.6g}")

    if sens is not None:
        print("\nSensitivity (KSG k sweep):")
        for label, val in sens:
            print(f"  {label:>6s}: {val:.6g}")

    print("\nNotes:")
    print("- If the stability curve does not flatten with n, variance is high.")
    print("- If k-sweep changes a lot, KSG result is sensitive (low credibility).")
    print("- If permutation p-value is large, dependence is not clearly detected.")
    print("")


if __name__ == "__main__":
    main()
