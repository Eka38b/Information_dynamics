"""
KSG estimators for:
- Mutual information (MI): I(X;Y)
- Conditional mutual information (CMI): I(X;Y|Z)
- Transfer entropy (TE) from ensemble of (x, y, x', y'):
    TE_{Y→X} = I(Y_t ; X_{t+1} | X_t)
    TE_{X→Y} = I(X_t ; Y_{t+1} | Y_t)

Assumes you have an ensemble of i.i.d. samples across replicates at a fixed time t
(or a pooled stationary regime), i.e. rows are independent.

Dependencies:
  pip install numpy scipy scikit-learn
"""

from __future__ import annotations
import numpy as np
from scipy.special import digamma
from sklearn.neighbors import NearestNeighbors


def _as_2d(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a)
    if a.ndim == 1:
        return a.reshape(-1, 1)
    if a.ndim != 2:
        raise ValueError(f"Expected 1D or 2D array, got shape {a.shape}")
    return a


def _zscore(a: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    mu = np.mean(a, axis=0, keepdims=True)
    sd = np.std(a, axis=0, ddof=0, keepdims=True)
    return (a - mu) / (sd + eps)


def _add_jitter(a: np.ndarray, jitter: float, rng: np.random.Generator) -> np.ndarray:
    if jitter <= 0:
        return a
    scale = jitter * (np.std(a, axis=0, ddof=0, keepdims=True) + 1e-12)
    return a + rng.normal(0.0, 1.0, size=a.shape) * scale


def _knn_eps_chebyshev(data: np.ndarray, k: int) -> np.ndarray:
    """
    For each point i, return epsilon_i = distance to its k-th nearest neighbor
    under Chebyshev (L_infty) metric.

    Note: NearestNeighbors includes the point itself at distance 0, so we query k+1.
    """
    n = data.shape[0]
    if k < 1 or k >= n:
        raise ValueError(f"k must satisfy 1 <= k < N; got k={k}, N={n}")

    nn = NearestNeighbors(metric="chebyshev", algorithm="auto")
    nn.fit(data)
    dists, _ = nn.kneighbors(data, n_neighbors=k + 1)
    eps = dists[:, -1]
    return eps


def _count_within_eps(data: np.ndarray, eps: np.ndarray) -> np.ndarray:
    """
    Count neighbors strictly within eps (Chebyshev balls), excluding self.
    Uses radius_neighbors_graph for speed.

    Important: we use radius = nextafter(eps, -inf) to implement "strictly < eps"
    to match KSG convention and avoid tie issues.
    """
    nn = NearestNeighbors(metric="chebyshev", algorithm="auto")
    nn.fit(data)

    # strictly less than eps (per-point). sklearn only supports a scalar radius,
    # so we do a fast workaround: compute counts for a single radius per point by batching.
    # For simplicity/robustness, we do a loop. (Works well up to ~1e5 points if dims are small.)
    counts = np.empty(data.shape[0], dtype=int)
    for i, e in enumerate(eps):
        r = np.nextafter(e, -np.inf)  # strictly less than epsilon
        idx = nn.radius_neighbors(data[i:i+1], radius=r, return_distance=False)[0]
        # exclude self (always included when r>0)
        counts[i] = max(len(idx) - 1, 0)
    return counts


def mi_ksg(x: np.ndarray,
           y: np.ndarray,
           k: int = 5,
           standardize: bool = True,
           jitter: float = 1e-10,
           seed: int | None = 0) -> float:
    """
    KSG (kNN) mutual information estimator I(X;Y) in nats.
    X and Y can be 1D or 2D arrays with same first dimension.

    Returns MI in nats (divide by log(2) for bits).
    """
    rng = np.random.default_rng(seed)

    X = _as_2d(x)
    Y = _as_2d(y)
    if X.shape[0] != Y.shape[0]:
        raise ValueError("X and Y must have same number of samples")

    if standardize:
        X = _zscore(X)
        Y = _zscore(Y)

    X = _add_jitter(X, jitter, rng)
    Y = _add_jitter(Y, jitter, rng)

    XY = np.concatenate([X, Y], axis=1)

    eps = _knn_eps_chebyshev(XY, k=k)
    nx = _count_within_eps(X, eps)
    ny = _count_within_eps(Y, eps)

    n = X.shape[0]
    # KSG MI estimator (variant 1) with strict counts
    mi = digamma(k) + digamma(n) - np.mean(digamma(nx + 1) + digamma(ny + 1))
    return float(mi)


def cmi_ksg(x: np.ndarray,
            y: np.ndarray,
            z: np.ndarray,
            k: int = 5,
            standardize: bool = True,
            jitter: float = 1e-10,
            seed: int | None = 0) -> float:
    """
    KSG-style conditional mutual information estimator I(X;Y|Z) in nats.
    Uses the common kNN CMI formulation (Frenzel-Pompe / KSG-CMI).

    X, Y, Z can be 1D or 2D arrays with same first dimension.

    Returns CMI in nats.
    """
    rng = np.random.default_rng(seed)

    X = _as_2d(x)
    Y = _as_2d(y)
    Z = _as_2d(z)
    n = X.shape[0]
    if Y.shape[0] != n or Z.shape[0] != n:
        raise ValueError("X, Y, Z must have same number of samples")

    if standardize:
        X = _zscore(X)
        Y = _zscore(Y)
        Z = _zscore(Z)

    X = _add_jitter(X, jitter, rng)
    Y = _add_jitter(Y, jitter, rng)
    Z = _add_jitter(Z, jitter, rng)

    XYZ = np.concatenate([X, Y, Z], axis=1)
    XZ = np.concatenate([X, Z], axis=1)
    YZ = np.concatenate([Y, Z], axis=1)

    eps = _knn_eps_chebyshev(XYZ, k=k)

    nxz = _count_within_eps(XZ, eps)
    nyz = _count_within_eps(YZ, eps)
    nz = _count_within_eps(Z, eps)

    cmi = digamma(k) - np.mean(digamma(nxz + 1) + digamma(nyz + 1) - digamma(nz + 1))
    return float(cmi)


def mi_te_from_xyxpy(ensemble: np.ndarray,
                     k: int = 5,
                     standardize: bool = True,
                     jitter: float = 1e-10,
                     seed: int | None = 0) -> dict[str, float]:
    """
    Convenience wrapper for ensemble of (x, y, x', y'):

    Input:
      ensemble: array of shape (N,4) where columns are [x_t, y_t, x_{t+1}, y_{t+1}]

    Outputs (nats):
      - MI_t: I(X_t; Y_t)
      - MI_tp1: I(X_{t+1}; Y_{t+1})
      - TE_Y_to_X: I(Y_t; X_{t+1} | X_t)
      - TE_X_to_Y: I(X_t; Y_{t+1} | Y_t)
      - I_present_future: I((X_t,Y_t); (X_{t+1},Y_{t+1}))
    """
    E = np.asarray(ensemble)
    if E.ndim != 2 or E.shape[1] != 4:
        raise ValueError("ensemble must have shape (N,4) as [x, y, x', y']")
    x, y, xp, yp = E[:, 0], E[:, 1], E[:, 2], E[:, 3]

    out = {}
    out["MI_t"] = mi_ksg(x, y, k=k, standardize=standardize, jitter=jitter, seed=seed)
    out["MI_tp1"] = mi_ksg(xp, yp, k=k, standardize=standardize, jitter=jitter, seed=seed)

    # TE_{Y→X} = I(Y_t ; X_{t+1} | X_t)
    out["TE_Y_to_X"] = cmi_ksg(y, xp, x, k=k, standardize=standardize, jitter=jitter, seed=seed)

    # TE_{X→Y} = I(X_t ; Y_{t+1} | Y_t)
    out["TE_X_to_Y"] = cmi_ksg(x, yp, y, k=k, standardize=standardize, jitter=jitter, seed=seed)

    # I( (X_t,Y_t) ; (X_{t+1},Y_{t+1}) )
    out["I_present_future"] = mi_ksg(
        np.column_stack([x, y]),
        np.column_stack([xp, yp]),
        k=k, standardize=standardize, jitter=jitter, seed=seed
    )
    return out


# ------------------ Example usage ------------------
if __name__ == "__main__":
    # Example: synthetic ensemble (replace with your simulation output)
    rng = np.random.default_rng(0)
    N = 2000
    x = rng.normal(size=N)
    y = 0.7 * x + 0.3 * rng.normal(size=N)
    xp = 0.9 * x + 0.2 * y + 0.3 * rng.normal(size=N)
    yp = 0.9 * y + 0.2 * x + 0.3 * rng.normal(size=N)

    ensemble = np.column_stack([x, y, xp, yp])
    stats = mi_te_from_xyxpy(ensemble, k=10)

    # Convert nats -> bits if you want:
    # stats_bits = {k: v / np.log(2) for k, v in stats.items()}

    for k, v in stats.items():
        print(f"{k:>16s} = {v:.6f} nats")
