# Repository URL update

Configured `tvu25/Score-based-Metropolis--Hastings-with-stable-proposals` consistently in the README, citation metadata, settings plan,
setup instructions, and manuscript/supplement availability sections. No live
GitHub write was performed. The numerical material remains R4-frozen-1, the
scientific manuscript remains R5, and Truong Vu remains the only manuscript author.

Only the URL was supplied. Public access, a release tag/commit, an archival DOI,
and optional asset uploads were not verified; no such status was invented.
The svjour3 preview format is unchanged. The alternate sn-jnl branch remains
uncompiled. The scientific code, tables, proofs and figures are not revised.

Follow the existing-repository procedure in GITHUB_SETUP.md. After receiving a
real version identifier and confirming its public contents, update the final
availability wording, rebuild the PDFs, and refresh the outer manifest.

The setup-test fixture now initializes its own pre-deposit state instead of
assuming the distributed metadata is always unconfigured. A new test verifies
that local configuration preserves an unverified state without promoting it to
public. This changes only the setup-layer tests, not numerical code.
