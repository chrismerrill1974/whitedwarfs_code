"""
WD V5 predictions: RDT structural shifts along the Paper 1 (V3) combined
95% CL boundary A_95(alpha) — i.e. the LARGEST shifts still allowed by
solar data. Inside the allowed region shifts scale ~linearly with A.

Outputs results_predictions.csv (checkpoint-free; fast to regenerate) and
figures/fig_dR_bands.pdf. Runs in ~1 minute single-threaded.

Observable convention: white dwarfs are compared at fixed MASS:
    dlnR|_M = dlnR|_rhoc - (dlnR/dlnM)_std * dlnM|_rhoc,
with (dlnR/dlnM)_std = -1/3 for n = 3/2.
"""

import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model import Params, mr_pair, MSUN_CGS

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# Paper 1 V3 combined 95% CL upper limits (headline error model),
# from solarcore_v3/analyze.py output, 2026-06-10.
A95 = [
    (0.020, 0.0042), (0.030, 0.0047), (0.045, 0.0055), (0.067, 0.0068),
    (0.100, 0.0083), (0.150, 0.0083), (0.224, 0.0066), (0.334, 0.0061),
    (0.500, 0.0067),
]

# Validity: non-relativistic degenerate electrons. x_F ~ 1 at
# rho ~ 2e6 g/cm^3 (mu_e = 2), so we quote predictions only for
# rho_c <= 3e6 (M <~ 0.85 Msun) — also where most observed WDs live.
RHO_C = np.geomspace(1e5, 3e6, 12)
FAST = dict(rtol=1e-9, atol=1e-11, max_step=0.05)


def main():
    rows = []
    for alpha, A in A95:
        p = Params(A=A, alpha=alpha)
        for rc in RHO_C:
            std, mod = mr_pair(p, rc, **FAST)
            dlnR = np.log(mod.R / std.R)
            dlnM = np.log(mod.M / std.M)
            dlnR_fixedM = dlnR + dlnM / 3.0   # -(dlnR/dlnM)_std = +1/3
            rows.append(dict(alpha=alpha, A=A, rho_c=rc,
                             M_std=std.M / MSUN_CGS, R_std_km=std.R / 1e5,
                             dlnR=dlnR, dlnM=dlnM, dlnR_fixedM=dlnR_fixedM))
        print(f"alpha={alpha:.3f} (A95={A:.4f}) done")

    out = os.path.join(HERE, "results_predictions.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # Envelope over alpha at each rho_c
    print("\n=== Paper-numbers block (95% CL boundary shifts) ===")
    print(f"{'rho_c':>9} {'M_std':>7} {'max|dlnR|_M|':>13} {'at alpha':>9}")
    env = []
    for rc in RHO_C:
        sub = [r for r in rows if r["rho_c"] == rc]
        worst = max(sub, key=lambda r: abs(r["dlnR_fixedM"]))
        env.append((rc, worst["M_std"], worst["dlnR_fixedM"], worst["alpha"]))
        print(f"{rc:9.1e} {worst['M_std']:7.3f} {worst['dlnR_fixedM']:13.4e} "
              f"{worst['alpha']:9.3f}")
    gmax = max(env, key=lambda e: abs(e[2]))
    print(f"\nGlobal envelope: |dR/R|_M <= {abs(gmax[2]):.3e} "
          f"(at rho_c={gmax[0]:.1e}, M={gmax[1]:.2f} Msun, alpha={gmax[3]})")

    # Figure: dlnR at fixed mass vs mass, one curve per alpha on the boundary
    plt.figure(figsize=(7, 4.8))
    cmap = plt.cm.viridis(np.linspace(0.15, 0.9, len(A95)))
    for (alpha, A), c in zip(A95, cmap):
        sub = sorted((r for r in rows if r["alpha"] == alpha),
                     key=lambda r: r["M_std"])
        plt.plot([r["M_std"] for r in sub],
                 [1e3 * r["dlnR_fixedM"] for r in sub],
                 color=c, lw=1.5, label=fr"$\alpha={alpha:g},\ A=A_{{95}}$")
    plt.axhline(0, color="k", lw=0.6)
    plt.xscale("log")
    plt.xlabel(r"$M$ ($M_\odot$)")
    plt.ylabel(r"$\Delta R/R$ at fixed mass  ($\times 10^{-3}$)")
    plt.title("Maximum solar-allowed RDT radius shifts for white dwarfs")
    plt.legend(fontsize=7, ncol=2)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, "fig_dR_bands.pdf"))
    print(f"\nWrote {out} and figures/fig_dR_bands.pdf")


if __name__ == "__main__":
    main()
