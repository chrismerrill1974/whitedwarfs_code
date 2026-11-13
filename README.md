# White Dwarfs — Paper II v6

Producing scripts, inputs, saved results and numerical controls for
**Radial Dimensionality Theory II: White Dwarf Structure under Solar-Constrained
Density-Dependent Dimensionality**.

Source release: `paper2-v6-zenodo-24184274`.

- [Paper](reproduction/output/pdf/publication/paper2/merrill_white_dwarf_stars_v6_10.5281_zenodo.24184274.pdf)
- [Manuscript](reproduction/paper2_WhiteDwarfs/V5_Paper/main.tex)
- [Current calculation and figure generation](reproduction/paper2_WhiteDwarfs/wd_step12/README.md)

## Reproduce the paper

Requires Python 3.14, NumPy 2.4.2, SciPy 1.17.1, Matplotlib 3.10.8,
TeX Live with revtex4-2, and Poppler. The resource controller uses POSIX
nice/setpriority, SIGPROF and SIGSTOP/SIGCONT.

```sh
git clone https://github.com/chrismerrill1974/whitedwarfs_code.git
cd whitedwarfs_code
git checkout paper2-v6-zenodo-24184274
nice -n 19 python3 reproduce.py --output /tmp/whitedwarfs-reproduction
```

The output directory must not exist. The command verifies every capsule hash,
regenerates the figure and table from saved results, and builds a PDF whose
extracted text matches the included paper. PNG figures and numerical tables
match byte-for-byte; PDF creation metadata may differ. No parameter scan is
launched by this command. `release.json` identifies the paper and
`reproduction/CAPSULE.json` records the scientific file checksums.

Full scans use `reproduction/paper2_WhiteDwarfs/wd_step12/propagate.py` and
its pinned solar inputs. Use one worker, verified nice priority 19, a maximum
of 95% of one CPU, and one native-library thread. Numerical evidence includes
resource measurements and failure records.

## Scientific scope and historical calculations

The results describe sampled polytropic models within the stated equation-of-state
limits; they do not establish general predictions for realistic white dwarfs.
Shared scientific scripts, inputs and results are included so no sibling checkout
is needed. This repository's supported paper build is Paper II.

Top-level `model.py`, `predict.py`, `validate.py` and `results_predictions.csv`
retain the original calculation. The revised calculation uses the audited flux
solver under `reproduction/paper2_WhiteDwarfs/audit_2026_11_11` and the propagation
and figures under `reproduction/paper2_WhiteDwarfs/wd_step12`.
