# Cloudflare access-transition plan — management-only

Status: **planning/reconciliation only**. This file does not change the active Worker, current provider-native URL, public source repository, build pipeline, or current live access state.

## Current-state preservation
- Reuse existing Worker `epistemology-textbook`; do not create a duplicate Worker.
- Preserve the current `workers.dev` URL and active deployment until a separate access transition is explicitly verified.
- Preserve current Workers Builds integration, Wrangler configuration, Quarto build contracts, repository visibility, and public source history.
- No URL retirement, redirect, DNS, or custom-domain change is authorized here.

## Target management state
- Provider remains Cloudflare Workers / Static Assets.
- Desired future Web visibility: restricted while source remains public.
- Reader policy reference: `shared-reader-access`.
- Preview visibility: private; non-production previews remain protected/disabled until Access acceptance.
- Production branch: `main`; commit-triggered only; no scheduled polling.
- Public bypass target: disabled.
- Paid services: not authorized.

## Content/build boundary
This phase does not modify textbook chapters, Quarto configuration, bibliography, assets, output formats, current build commands, `publishing.yaml`, `website.yaml`, `cloudflare-builds.yaml`, or `wrangler.jsonc`. It records only future access-management intent.

## Manual/provider gates
Cloudflare login/MFA, verification of the actual Worker/Builds state, account-wide Access baseline, reader approval, exact hostname policy review, anonymous denial, authorized-reader access, direct asset/feed checks, and explicit access transition remain separate gates.

## Rollback
No provider write is performed here. Before any future access-policy change, record the active verified Worker version and current Access state. Repository rollback is a normal revert; provider rollback restores the previous verified Access/Worker state. No paid upgrade or URL change is authorized.
