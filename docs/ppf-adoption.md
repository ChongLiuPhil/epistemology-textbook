# PPF Adoption — epistemology-textbook

**Status:** PPF Phase 1 COMPLETE / Cloudflare staging+runtime VERIFIED / canonical cutover PENDING  
**Framework:** Personal Publishing Framework v0.1.0-draft  
**Adopted framework commit:** `9326920e1920d18f0a71eac26d4068da9d6bdffe`  
**Observed upstream PPF main during 2026-09-19 reconciliation:** `b9140e1abb116ba27e73c0c7873955078be9593b` — **NOT ADOPTED**

## Purpose

This project is the first real downstream pilot of the Personal Publishing Framework (PPF).

The pilot tests whether one durable Quarto source can support:

```text
accepted source
      |
      +--> continuous Web edition
      |
      +--> explicit on-demand publication formats
```

without allowing generated formats to become competing manuscript sources.

## Phase 1 — profile and runtime validation

Phase 1 keeps the existing public GitHub Pages site online.

It introduces:

- `publishing.yaml` as the declarative publication contract;
- `web` as the default Quarto profile;
- separate EPUB / PDF / DOCX / LaTeX profiles;
- `_book/` for the continuous Web artifact;
- `_publication/<format>/` for on-demand artifacts;
- one-format-per-request publication builds;
- `wrangler.jsonc` as a staged Cloudflare Workers Static Assets configuration.

GitHub Pages remains the production provider during this phase so runtime validation can occur without changing the public canonical URL.

## Phase 2 — Cloudflare staging and cutover

Cloudflare staging is now real and verified, while canonical cutover remains a separate change.

Completed:

- Cloudflare account / GitHub App / repository connection: VERIFIED;
- Worker target: VERIFIED;
- main Workers Build: PASS;
- non-production preview: PASS;
- main workers.dev runtime: PASS;
- preview workers.dev runtime: PASS;
- build-token permission scope review: COMPLETE;
- Hardened External CI candidate: candidate / validate-only PASS.

Still required before canonical production cutover:

1. explicit human production-security-profile selection;
2. a confirmed canonical production URL;
3. Cloudflare zone / Custom Domain eligibility and binding;
4. post-cutover production verification;
5. an explicit legacy / redirect / canonical policy for the existing GitHub Pages URL.

GitHub Pages remains the current canonical production until those gates are completed. A successful provider production-branch build or workers.dev runtime does not itself change canonical production.

## Source boundary

Canonical manuscript source remains:

- `index.qmd`
- `manuscript/*.qmd`
- `references.bib`
- shared Quarto metadata/configuration

Generated output is always derived:

- `_book/`
- `_publication/`

No generated artifact may silently become the manuscript source.

## Publication semantics

- **Web / HTML** — continuous publication.
- **EPUB / PDF / DOCX / LaTeX** — on-demand build artifacts.
- **BUILD** does not imply **RELEASE**.
- **RELEASE** does not imply external platform publication.
- Existing project Release Approval rules remain in force.

## Governance boundary

This pilot changes the publishing lifecycle only.

The repository's current HARC-lite collaboration-governance files are intentionally left unchanged in this PR. Migration from HARC-lite to an AHICP-based project profile should be handled in a separate governance change so publishing-runtime defects and governance defects remain distinguishable.


## Runtime validation result

Phase 1 has now been validated in real GitHub Actions on PR #20.

Passed:

- repository governance;
- canonical-source validation;
- full Web-profile render and rendered-HTML checks;
- EPUB profile;
- DOCX profile;
- LaTeX profile;
- PDF profile with Noto CJK fonts and TinyTeX.

The temporary PR-only matrix workflow used to validate all four on-demand formats was removed after validation. It is not part of the final architecture.

Detailed evidence is recorded in `docs/ppf-pilot-audit.zh-CN.md`.

This completes **profile/runtime validation**, not Cloudflare production validation. GitHub Pages remains the current production provider until Phase 2.


## Phase 1 completion record

Phase 1 was merged through PR #20.

- merge commit: `96b91691bd776136e156c384eee619d52ff2e3a4`
- main Governance CI: PASS
- main Web-profile build and rendered-HTML validation: PASS
- GitHub Pages artifact upload: PASS
- GitHub Pages deployment: PASS
- External Link Audit: PASS

The general-purpose web reader available in this ChatGPT session could not directly fetch the GitHub Pages URL, so this record does **not** claim an independent external HTTP content fetch. Production deployment is verified from GitHub's Pages deployment job, and repository-side external-link validation also passed.

Phase 2 staging/runtime verification is now complete. Cloudflare remains a verified staging/runtime target, not the canonical production provider.

## Current Cloudflare security-profile evidence

- **Profile A — Workers Builds Native:** operationally verified; managed user-token scope is broader than a pure static Worker needs and is not per-Worker least privilege.
- **Profile B — Hardened External CI:** candidate / validate-only PASS; no deployment credential is configured and preview/production deployment steps have not run, so it is not production-tested.
- **Profile C — Future Native Granular:** currently unavailable because the required account-owned-token combination is not supported by the recorded Workers Builds product path.

The production security profile is a human-governed decision and has not been selected in this adoption record.

## Upstream adoption rule

This repository does **not** silently follow PPF `main`.

The durable adopted framework state remains the version/commit recorded above. Later upstream PPF changes, including provider-integration semantic work completed after the original pilot adoption, are informative until a separate downstream adoption decision updates `publishing.yaml` and this file after applicable validation.
