# Score-based Metropolis-Hastings with stable proposals
## Invariance and calibration

**Truong Vu**  
Departments of Mathematics and Computational Medicine  
University of California, Los Angeles (UCLA), Los Angeles, California, USA

Research code, synthetic model inputs, recorded results, and manuscript sources for
*Score-based Metropolis-Hastings with stable proposals: Invariance and calibration*.


[Read the manuscript](manuscript/main.pdf) |
[Online Resource 1](manuscript/supplement.pdf) |
[Install and reproduce](docs/REPRODUCING.md) |
[Set up GitHub](docs/GITHUB_SETUP.md) |
[Table/figure map](ARTIFACT_MAP.md)

<!-- REPOSITORY_IDENTITY_BEGIN -->
**Repository:** [tvu25/Score-based-Metropolis--Hastings-with-stable-proposals](https://github.com/tvu25/Score-based-Metropolis--Hastings-with-stable-proposals)  
**Manuscript author:** Truong Vu.  

<!-- REPOSITORY_IDENTITY_END -->

## What this repository contains

The manuscript distinguishes correct invariant laws, consistency of an
acceptance-learning objective, and computational efficiency. It analyzes a linear
proposal-score proxy for isotropic stable proposals, exact conditional-Gaussian
and finite-mixture corrections, Gaussian-reference alternatives, and conditional
error bounds linking balance residuals to transition and stationary errors.

The implementation material includes eight full-vector posterior samplers:
Gaussian random-walk MH, Gaussian MALA, randomized-length HMC, stable random-walk
MH, auxiliary stable MH, marginal finite-mixture MH, Laplace-reference pCN, and
Laplace-reference stable-clock pCN. A same-node conditional-mixture control is
included separately. Historical scripts cover the scalar and projected tests,
acceptance-network example, graph Gibbs analysis, score regression, and certified
integration-work diagnostics. See the manuscript for the assumptions of each result.

This is **not the original MAFLA implementation** and does not claim to reconstruct
the original authors' complete experimental pipeline. The motivating work is
[Aloui et al., arXiv:2602.00835v1](https://arxiv.org/abs/2602.00835v1).

## Versions and evidence boundaries

| Item | Version or status |
|---|---|
| Scientific manuscript | R5, with subsequent journal-format/availability edits |
| Frozen numerical release | `R4-frozen-1` |
| GitHub packaging | `SAC-github-setup-3-url` |
| Primary numerical records | 128 four-chain replications |
| Component-sensitivity records | 16 four-chain replications |
| Public journal DOI | Not assigned in this package |
| License | Author selection pending; see [LICENSE_STATUS.md](LICENSE_STATUS.md) |

The numerical directories are preserved byte-for-byte. A new packaging version
is not a new simulation, independent accuracy replication, or proof. The paper
retains an unresolved dimension-16 random-walk contrast discrepancy. Passing
finite-run diagnostics does not certify posterior-mean accuracy. Timings are
hardware- and workflow-dependent; a rerun cannot recover historical seconds.

## Quick start

Once these files are uploaded and you have access, clone the author-provided repository:

```bash
git clone https://github.com/tvu25/Score-based-Metropolis--Hastings-with-stable-proposals.git
cd Score-based-Metropolis--Hastings-with-stable-proposals
```


Use **Python 3.13**; the recorded version is **3.13.5**. The numerical requirements
are pinned in `requirements.txt`. There is no package to install with `pip install
-e .`; run the supplied scripts from the repository root.

### Linux, macOS, or Windows with WSL

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/verify_repository.py
python scripts/check_github_setup.py
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/run_checks.py --audit --safety
```

### Windows PowerShell

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe scripts/verify_repository.py
.\.venv\Scripts\python.exe scripts/check_github_setup.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
.\.venv\Scripts\python.exe scripts/run_checks.py --audit --safety
```

Linux is the reference numerical platform and the configured GitHub Actions
runner. Windows/macOS commands are supplied for convenience; bitwise trajectory
agreement and identical runtime are not promised across platforms. If the pinned
wheels are unavailable for your interpreter or platform, use the documented Linux
reference environment rather than silently changing the numerical versions.

For only numerical checks, `requirements.txt` is sufficient. The development file
adds PyYAML for validating GitHub configuration. Historical neural retraining has
an additional Torch dependency in `requirements-historical-neural.txt` and is not
part of the quick start or CI.

### What the checks do

| Command | Work performed | Full posterior benchmark? |
|---|---|---|
| `verify_repository.py` | Hashes, immutable scientific files, authorship, and artifact mapping | No |
| `check_github_setup.py` | Workflow, citation, metadata, link, and setup-file checks | No |
| `unittest discover ...` | Local configuration/release-helper regression tests | No |
| `run_checks.py --audit` | Reaggregate the 144 deposited numerical records | No |
| `run_checks.py --safety` | Run the supplied safety tests and short finite-path controls | No |

`run_checks.py` uses a temporary copy, preserving the deposited result files.
The arithmetic audit does not recalculate ESS from thinned inspection arrays or
resimulate every chain. See [reproduction instructions](docs/REPRODUCING.md) for a
separate full rerun. Running the original driver against populated results can
skip completed computations; that is not a fresh experiment.

## Repository layout

```text
.github/                     GitHub workflows, issue forms, and settings plan
manuscript/                  Article, Online Resource 1, LaTeX, and eight figures
reproducibility/
  stable_score_R4_core/       Guarded code, models, seeds, and numerical records
  stable_score_historical_diagnostics/
                             Preserved historical code and results
docs/                        GitHub setup, releases, reproduction, and limitations
scripts/                     Non-destructive verification and setup helpers
tests/                       Tests for the repository setup layer
validation/                  Packaging validation records
ARTIFACT_MAP.json             Table/figure-to-file map and member hashes
RELEASE_ASSETS.json           Seven optional large trace archives and their hashes
CITATION.cff                  Sole-author manuscript/software citation
MANIFEST_SHA256.json          Current repository file manifest
```

The original primary and component summaries are available as
[summary_R4.csv](reproducibility/stable_score_R4_core/results/summary_R4.csv) and
[replicates_R4.csv](reproducibility/stable_score_R4_core/results/replicates_R4.csv).
The complete table/figure map identifies the individual supporting records.

## GitHub checks and releases

The [CI workflow](.github/workflows/ci.yml) checks repository integrity and the
setup layer, then runs the record audit and safety suite in a temporary copy.
It never launches the full benchmark, overwrites deposited records, or publishes
scientific claims. Its status becomes meaningful only after GitHub executes it;
no passing GitHub badge is fabricated in this README.

The [manual draft-release workflow](.github/workflows/draft-release.yml) packages
an existing tag and creates a **draft** release. It does not make a release public.
Optional large trace ZIPs must be uploaded separately under their original names.
See [GitHub setup](docs/GITHUB_SETUP.md), [recommended settings](docs/GITHUB_SETTINGS.md),
and the [release checklist](docs/RELEASING.md).

## Large optional data

The normal record audit needs no large trace downloads. The seven optional ZIPs
are listed in [RELEASE_ASSETS.json](RELEASE_ASSETS.json), including exact filenames,
byte sizes, and SHA256 hashes. Put those ZIPs in a versioned GitHub **Release**, not
in ordinary Git history. The combined optional files are about 307 MB.

After downloading the original ZIPs to a local folder:

```bash
python scripts/install_optional_assets.py /path/to/downloaded/assets
python scripts/run_checks.py --audit --with-inspections
```

All six inspection archives are needed for the inspection audit. The seventh
archive contains prior validation/contrast traces. Inspect the manifest before
extracting; do not use changed or renamed substitutes. Reconstructed unthinned
paths can be checked against the saved hashes in the original environment.

## Building the manuscript

```bash
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
```

The checked article PDF uses the supplied **`svjour3` preview class**, with
two columns and author-year citations. The source can select the official
`sn-jnl` branch if the class is installed, but that branch has not been validated
in this release. See [template status](docs/TEMPLATE_STATUS.md). No font files are
distributed. Complete visible author-information placeholders before submission.

## Citation and authorship

**Truong Vu is the sole author of the article and supplement.** Authors of cited
work and third-party software retain their respective credits. The manuscript
retains its substantive generative-AI-assistance disclosure.

Use [CITATION.cff](CITATION.cff) for machine-readable citation. There is no assigned
journal DOI or asserted journal acceptance. A plain manuscript citation is:

```bibtex
@unpublished{vu_score_based_stable,
  author = {Truong Vu},
  title = {Score-based Metropolis--Hastings with stable proposals:
           Invariance and calibration},
  year = {2026},
  url = {https://github.com/tvu25/Score-based-Metropolis--Hastings-with-stable-proposals},
  note = {Manuscript scientific version R5; numerical release R4-frozen-1}
}
```

## Contributing, security, and license

Read [CONTRIBUTING.md](CONTRIBUTING.md) before modifying the frozen scientific
records. Report reproducibility questions with the supplied issue form and include
the environment and exact command, not confidential data or credentials.
See [SECURITY.md](SECURITY.md) for sensitive reports.

No new reuse license has been selected. Public hosting alone is not a software,
data, or manuscript license. Review [LICENSE_STATUS.md](LICENSE_STATUS.md) and
preserve the Springer and other third-party notices. Do not describe the package
as accepted by a journal, independently peer-reviewed, or formally certified.
