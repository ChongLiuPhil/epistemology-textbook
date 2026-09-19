# PPF Adoption — epistemology-textbook

**Status:** PPF pilot / Phase 1 runtime validation PASS — final normal CI verification  
**Framework:** Personal Publishing Framework v0.1.0-draft  
**Adopted framework commit:** `9326920e1920d18f0a71eac26d4068da9d6bdffe`

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

## Phase 2 — Cloudflare cutover

Cloudflare activation is a separate change.

It requires, at minimum:

1. a confirmed Worker / Static Assets deployment target;
2. GitHub deployment credentials or another authorized deployment mechanism;
3. a confirmed canonical production URL;
4. a successful preview/staging deployment;
5. production verification;
6. an explicit decision about redirect/canonical handling for the existing GitHub Pages URL.

Only after those conditions are satisfied should the main Web workflow change from GitHub Pages deployment to automatic Cloudflare deployment.

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
