# PPF Adoption — epistemology-textbook

**Status:** PPF adopted / workers.dev canonical cutover VERIFIED / Pages retirement PENDING  
**Framework:** Personal Publishing Framework v0.1.0-draft  
**Adopted framework commit:** `21a5360727167bad6f399477ded073431645fa1d`  
**Previous adopted framework commit:** `9326920e1920d18f0a71eac26d4068da9d6bdffe` — superseded by explicit human adoption on 2026-09-19

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

## 2026-09-19 semantic adoption update

The project owner explicitly adopted PPF `v0.1.0-draft @ 21a5360727167bad6f399477ded073431645fa1d`.

This revision adds provider-neutral semantics for:

- source / repository visibility;
- publication authorization;
- publication visibility;
- access policy;
- canonical publication identity distinct from provider endpoint.

The current project state is recorded as:

~~~text
source visibility = public
Web publication authorization = authorized
Web publication visibility = public
Web access mode = none
current canonical identity = workers.dev
provider endpoint = workers.dev
legacy GitHub Pages policy = retire
post-cutover verification = passed
legacy unpublish = pending
~~~

This adoption records current reality; it does not prevent a future project from using a private source repository, restricted/private Web publication, or an authenticated access policy.

The repository cutover now activates the already selected workers.dev URL as the canonical identity. GitHub Pages is no longer the intended canonical publication endpoint; its selected legacy policy is `retire`, with actual unpublish tracked separately from canonical activation.

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

Cutover decisions and repository migration are now resolved:

- production security profile = Profile A / Workers Builds Native;
- canonical URL = `https://epistemology-textbook.philosophy-research.workers.dev/`;
- Custom Domain = not applicable;
- legacy GitHub Pages policy = `retire`;
- Quarto canonical configuration = workers.dev;
- GitHub Pages deployment workflow = retired.

Post-cutover evidence is now verified:

- merge commit `63510364ed40a97faf190c484dd80afc91971ecb`;
- GitHub runtime run `35453967021`: PASS;
- Cloudflare provider check `105926103705`: PASS;
- Cloudflare build `42aa93fe-d9b6-49e4-80be-a849951a6b9d`: PASS;
- workers.dev canonical marker + 5 representative pages + 30 local assets: PASS.

Remaining cleanup:

1. actual GitHub Pages deployment unpublish.

The second item is provider-side cleanup and is not silently treated as complete merely because the repository stopped deploying Pages.

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

Phase 2 staging/runtime verification and post-cutover main verification are complete. Cloudflare workers.dev is the verified canonical production provider; GitHub Pages is legacy-retirement pending.

## Current Cloudflare security-profile evidence

- **Profile A — Workers Builds Native:** operationally verified; managed user-token scope is broader than a pure static Worker needs and is not per-Worker least privilege.
- **Profile B — Hardened External CI:** candidate / validate-only PASS; no deployment credential is configured and preview/production deployment steps have not run, so it is not production-tested.
- **Profile C — Future Native Granular:** currently unavailable because the required account-owned-token combination is not supported by the recorded Workers Builds product path.

The production security profile is human-governed and has been selected as **Profile A — Workers Builds Native**. The target canonical URL has also been selected as the verified workers.dev endpoint. Neither decision alone completes canonical production cutover.

## Upstream adoption rule

This repository does **not** silently follow PPF `main`.

The durable adopted framework state is the version/commit recorded above: `21a5360727167bad6f399477ded073431645fa1d`.

The earlier adoption `9326920e1920d18f0a71eac26d4068da9d6bdffe` has been superseded only because the human project owner explicitly approved this downstream adoption and the project migrated its publication contract accordingly.

Any later upstream PPF changes remain informative until another explicit downstream adoption decision updates `publishing.yaml` and this file after applicable validation.
