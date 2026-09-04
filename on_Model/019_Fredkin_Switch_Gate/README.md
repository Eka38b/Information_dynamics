# Fredkin Switch-Gate Model

## Overview

This directory implements a finite-state, reversible model for studying the
competition between a pre-existing circulating information flow and a newly
activated external information flow. The interaction at the merging node is a
Fredkin controlled-swap operation.

The numerical experiment compares

$$
T_{A_3\to p}(t_0)
\quad\text{and}\quad
T_{\mathrm{Ext}\to p}(t_1),
$$

where $t_0$ is the last update before the external interaction and $t_1$
is the first update after it is activated.

The script is intended to be used with the `Information_dynamics` repository
and its `Core` package.

## Network

For the default setting `N = 3`, the directed network is

```text
p -> A1 -> A2 -> A3 -> p
                      ^
                      |
                     Ext
```

The nodes `p`, `A1`, `A2`, `A3`, and `Ext` all use the same four-state
alphabet. In the notation of the theoretical merging problem,

| Theoretical variable | Simulation node |
| --- | --- |
| $A$, the circulating input | `A3` |
| $P$, the merging node | `p` |
| $Q$, the delayed copy of $P$ | `A1` |
| $B=(B_1,B_2)$, the external input | `Ext` |

The remaining node `A2` supplies an additional delay along the cycle.

## State encoding

Every node has state space

$$
\{00,01,10,11\},
$$

encoded in the program as

```text
0 -> 00
1 -> 01
2 -> 10
3 -> 11
```

The first bit of `Ext` is the Fredkin control bit. Its second bit is an
independent auxiliary coordinate and does not enter the controlled swap.

## Parameterized cycle ensemble

The script denotes the distribution parameter by `theta`. It corresponds to
the parameter $x$ in the analytical description:

$$
x\equiv\theta,
\qquad 0\le x<\frac14.
$$

Each cycle node is independently initialized from

$$
p_x(00)=\frac14,\qquad
p_x(01)=\frac14+x,\qquad
p_x(10)=\frac14-x,\qquad
p_x(11)=\frac14.
$$

Thus, the initial joint distribution of the cycle nodes is a product of
identical marginals. The isolated cycle update only permutes the node states,
so this product distribution is stationary even though information is
transferred around a directed cycle.

The external node is initialized independently and uniformly over its four
states. Consequently, its first bit is a fair control bit.

## State dynamics

### Before the interaction

For `t < Start_of_Interaction`, the cycle is updated by deterministic copies:

$$
\begin{aligned}
A_1(t+1)&=p(t),\\
A_2(t+1)&=A_1(t),\\
A_3(t+1)&=A_2(t),\\
p(t+1)&=A_3(t),\\
\mathrm{Ext}(t+1)&=\mathrm{Ext}(t).
\end{aligned}
$$

### After the interaction

At and after `Start_of_Interaction`, the first bit of `Ext` controls whether
the two bits of `A3` are exchanged before being written to `p`. Define

$$
\pi_0(a_1,a_2)=(a_1,a_2),
\qquad
\pi_1(a_1,a_2)=(a_2,a_1).
$$

Then

$$
p(t+1)=\pi_{B_1(t)}\bigl(A_3(t)\bigr).
$$

In the integer encoding, this operation exchanges states `1` and `2` and
leaves states `0` and `3` unchanged. The second external bit is carried
unchanged and has no effect on the update of `p`.

Because the cycle update is a permutation, the control state is retained, and
the controlled swap is self-inverse, the complete state update is bijective.

## Exact information-theoretic prediction

Let

$$
H(p_x)=-\sum_{z\in\{00,01,10,11\}}p_x(z)\ln p_x(z).
$$

Before the interaction, neighboring cycle nodes are simultaneously
independent under the stationary product ensemble, while the next state of
`p` is a deterministic copy of `A3`. Therefore,

$$
T_{A_3\to p}(t_0)=H(p_x).
$$

The Fredkin swap maps $p_x$ to $p_{-x}$. Since the first bit of `Ext` is
fair,

$$
\frac12p_x+\frac12p_{-x}
=\operatorname{Uniform}(\{00,01,10,11\}).
$$

It follows that

$$
T_{\mathrm{Ext}\to p}(t_1)=\ln4-H(p_x).
$$

Hence this model attains the conditional-entropy bound:

$$
T_{A_3\to p}(t_0)+T_{\mathrm{Ext}\to p}(t_1)=\ln4.
$$

The conditional-entropy margin is

$$
\epsilon(x)
=\ln4-H(P'\mid P)
=\ln4-H(p_x),
$$

and the realized external transfer satisfies

$$
T_{\mathrm{Ext}\to p}(t_1)=\epsilon(x).
$$

At $x=0$, the cycle-node distribution is uniform, so

$$
H(P'\mid P)=\ln4,
\qquad
T_{\mathrm{Ext}\to p}(t_1)=0.
$$

For $0<x<1/4$,

$$
\frac{dT_{\mathrm{Ext}\to p}}
     {dT_{A_3\to p}}=-1.
$$

At $x=0$, both derivatives with respect to $x$ vanish. The corresponding
boundary statement is therefore understood as the one-sided limit as
$x\downarrow0$, rather than as a direct quotient at $x=0$.

## Relation to the sufficient hypotheses

The six hypotheses used in the accompanying theoretical analysis are checked
analytically rather than inferred from the numerical trend. In particular,
the deterministic delay and Fredkin updates give

$$
\alpha_{1,\mathrm{pre}}=\alpha_{1,\mathrm{post}}=0,
$$

while

$$
H(P'\mid P)=T_{A_3\to p}(t_0)=H(p_x)
$$

and

$$
0\le T_{\mathrm{Ext}\to p}(t_1)
=\epsilon(x)
=\ln4-H(P'\mid P).
$$

The simulation estimates the transfer entropies; it is not used as a
substitute for the analytical verification of the hypotheses.

## Default simulation settings

| Parameter | Value | Meaning |
| --- | ---: | --- |
| `Q` | 4 | Number of states per node |
| `N` | 3 | Number of internal nodes `A1`, ..., `AN` |
| `Simulation_Time_Limit` | 40 | Number of simulated updates |
| `Start_of_Interaction` | 25 | First update using the Fredkin interaction |
| `Size_of_Ensemble` | 10,000 | Ensemble size for each estimate |
| `N_Trials` | 5 | Independent numerical trials |
| `N_Param` | 10 | Number of parameter cases |
| Estimator | Simple binning | Plug-in estimator supplied by `Core` |

The current parameter scan is

$$
x=0.24,0.22,0.20,\ldots,0.06.
$$

## Installation and placement

Place the script at

```text
on_Model/019_Fredkin_Switch_Gate/main.py
```

inside the `Information_dynamics` repository. Install the repository
requirements, for example:

```bash
python -m pip install -r requirements.txt
```

Before the first run, create the base output directory:

```bash
mkdir -p on_Model/019_Fredkin_Switch_Gate/Temporal_Results
```

The script creates the individual trial and case directories. These directories
must not already exist when the current script is run, because it uses
`os.mkdir` without `exist_ok=True`.

## Running the simulation

Run from the repository root so that the `Core` imports and relative output
paths resolve correctly:

```bash
python on_Model/019_Fredkin_Switch_Gate/main.py
```

The complete default scan can be computationally intensive because a separate
ensemble is generated for every selected link, selected node, time point,
parameter case, and trial.

## Outputs

The generated directory structure is

```text
on_Model/019_Fredkin_Switch_Gate/Temporal_Results/
  Figure3.png
  Paper_001/
    Case000/
      Link_A3_p.txt
      Link_Ext_p.txt
      Link_p_A1.txt
      Node_p.txt
      Node_p_E_values.txt
      Simulation_Properties.txt
    Case001/
    ...
  Paper_002/
  ...
```

The summary figure uses

- `Link_A3_p.txt`: `TE2[24]` for $T_{A_3\to p}(t_0)$, and
- `Link_Ext_p.txt`: `TE2[25]` for $T_{\mathrm{Ext}\to p}(t_1)$.

These indices select the last pre-interaction transition and the first
post-interaction transition, respectively.

## Reproducibility and numerical interpretation

The current script seeds NumPy from the system time. Consequently, repeated
runs do not reproduce exactly the same Monte Carlo estimates. For archival or
publication use, replace the time-dependent seed with a fixed recorded seed.

The simple-binning estimator is a finite-sample plug-in estimator. Its estimates
need not satisfy the exact identity

$$
T_{A_3\to p}+T_{\mathrm{Ext}\to p}=\ln4
$$

at finite ensemble size. In particular, it may return a small positive external
transfer entropy at the exact $x=0$ boundary. Numerical points should
therefore be compared with the analytical reference curve, and uncertainty
across trials should be reported.

