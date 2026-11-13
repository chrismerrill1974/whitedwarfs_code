# WhiteDwarfs V5 — White dwarf signatures of Radial Dimensionality Theory

Code for **Radial Dimensionality Theory II: White Dwarf Structure under
Solar-Constrained Density-Dependent Dimensionality**
(C. K. Merrill and Claude, 2026).

This package applies the RDT opening law and exact modified Lane–Emden
equation of Paper I (see the companion `solarcore_code` repository) to
non-relativistic n = 3/2 white dwarfs with the physical degenerate-electron
polytropic constant (μ_e = 2), and computes the maximum structural
signatures allowed by Paper I's solar bound. Headline result: a radius
**deficit** at fixed mass of |ΔR/R| ≤ 9.5×10⁻³ across M ≈ 0.16–0.86 M_⊙,
nearly mass-independent — at the precision frontier of eclipsing-binary
mass–radius measurements.

## Requirements

Python ≥ 3.10 with `numpy`, `scipy`, `matplotlib`.

## Files

| File | Purpose |
|---|---|
| `model.py` | Physics: RDT opening law, exact modified Lane–Emden ODE (n = 3/2), physical polytropic constant, white dwarf builder `build_wd(params, rho_c)` → (M, R), and `mr_pair` for standard/modified comparisons at fixed central density. |
| `validate.py` | Validation gates. **Run this first.** A=0 regression (ξ₁ = 3.653754, ω = 2.71406), analytic scalings (R ∝ ρ_c^(−1/6), M ∝ ρ_c^(1/2)), physical sanity (ρ_c = 10⁶ g/cm³ → R = 1.12×10⁹ cm, M = 0.50 M_⊙), start-inside-the-star check, cgs/SI unit invariance, fiducial sanity. Gates 2–4 regress directly against the failure modes of the superseded V4 code. |
| `predict.py` | Computes fixed-mass radius shifts for parameters on Paper I's combined 95% CL exclusion boundary A₉₅(α) — the largest solar-allowed signatures. Writes `results_predictions.csv` and `figures/fig_dR_bands.pdf`, and prints the paper-numbers block. ~1 min. |
| `results_predictions.csv` | Prediction output behind the published numbers (included for reproducibility). |

## Usage

Run single-threaded (numpy/BLAS gains nothing at these sizes and will
otherwise occupy every core):

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
       VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1

# 1. Validation gates — all must PASS before trusting any physics output
python3 validate.py

# 2. Predictions along the solar exclusion boundary (~1 min)
python3 predict.py
```

`predict.py` prints every number quoted in the paper and regenerates the
paper figure.

## Notes

- Validity range: ρ_c ∈ [10⁵, 3×10⁶] g/cm³ (non-relativistic electrons;
  M ≈ 0.16–0.86 M_⊙). The n = 3/2 polytrope has no maximum mass, so this
  code makes **no** Chandrasekhar-mass statements (see Paper III for the
  relativistic regime).
- The observable convention is radius at fixed mass:
  Δln R|_M = Δln R|_ρc + (1/3)·Δln M|_ρc.
- The A₉₅(α) boundary values are hard-coded in `predict.py` from the
  Paper I analysis (solarcore_code/analyze.py output, 2026-06-10).
- All results are unit-invariant (gate 5 verifies cgs ↔ SI).

## License

MIT — see [LICENSE](LICENSE).
