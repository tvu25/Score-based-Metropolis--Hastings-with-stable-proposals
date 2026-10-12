# Update the author-provided GitHub repository

Repository: [tvu25/Score-based-Metropolis--Hastings-with-stable-proposals](https://github.com/tvu25/Score-based-Metropolis--Hastings-with-stable-proposals)

This package is configured for the URL supplied by the author. It has not been
pushed to GitHub, and live repository contents, visibility, releases and Actions
runs could not be verified. **Truong Vu is the sole manuscript author.**

## 1. Preserve the existing repository

If you already have a working checkout, use it after committing or backing up
local edits. Otherwise clone the existing repository:

```bash
git clone https://github.com/tvu25/Score-based-Metropolis--Hastings-with-stable-proposals.git
cd Score-based-Metropolis--Hastings-with-stable-proposals
git status --short
git switch -c repository-metadata-update
```

Do not run `gh repo create` for this URL or overwrite the repository history.
An empty remote without a branch may need its first commit instead of the branch
step; use the setup files in the clone, not an unrelated Git history.

## 2. Review and apply the local update

Copy the prepared files into the checkout, including hidden `.github` files.
The smaller update ZIP includes changed files only. The full ZIP also includes
the unchanged science and data. Inspect every overwritten file and preserve any
newer remote edits. This preparation is not a merge against the live repository.

```bash
git diff --stat
git diff -- README.md CITATION.cff repository_metadata.json manuscript/main.tex manuscript/supplement.tex
```

The URL is already configured. No release tag is invented. A public release
identifier must be added after it is actually chosen and checked.

## 3. Check locally

Install the pinned requirements as described in the README. The local checks are:

```bash
python scripts/verify_repository.py
python scripts/check_github_setup.py
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/run_checks.py --audit --safety
```

These do not run the full scientific benchmark. If merging with your newer local
edits changes tracked metadata, review the differences before refreshing the outer
manifest with `python scripts/verify_repository.py --refresh`. Never change the
immutable scientific hashes to conceal an unintended change.

After reviewing the staged files:

```bash
git add .
git diff --cached --stat
git commit -m "Configure repository URL and availability metadata"
git push -u origin HEAD
```

Review and merge that branch on GitHub. Do not force push over existing work.

## 4. Optional repository settings and versioned release

Preview the prepared settings with `python scripts/apply_github_settings.py`.
Run its `--apply` mode only after confirming the target and reviewing the settings;
it uses your own authenticated GitHub CLI session. No settings were applied here.
See [settings](GITHUB_SETTINGS.md) and [releases](RELEASING.md).

Check the actual Actions run after pushing; a valid workflow file is not evidence
of a passing hosted run. Upload the seven optional archives as release assets under
the names in `RELEASE_ASSETS.json`, not as oversized ordinary Git files.

The article's repository URL is filled in. Its release/commit, email, funding,
conflict and license choices remain factual author tasks. See
[availability wording](DATA_AND_CODE_AVAILABILITY.md) and
[verification status](REPOSITORY_STATUS.md).
