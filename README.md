# How Do We Know? — A Problem-Driven Epistemology

[English](README.md) | [中文](README.zh-CN.md)

This is a Chinese-language, problem-driven epistemology textbook and learning project maintained by Chong Liu. It grows primarily out of the author's ongoing study and integration of concepts, arguments, debates, and literature. Its main goal is not to construct a new proprietary epistemological theory, although the selection of problems, organization of material, comparative framing, and evaluative judgments remain author-reviewed.

## Current stage: Web Edition Development

The Web edition is the verified canonical continuous publication. The normal delivery path is:

`canonical QMD → make web-publish-check → Cloudflare Workers Builds → workers.dev`

Read online: <https://epistemology-textbook.philosophy-research.workers.dev/>

Open access and support: <https://epistemology-textbook.philosophy-research.workers.dev/manuscript/00-open-access-and-support.html>

PDF, DOCX, EPUB, and LaTeX are explicit on-demand build artifacts. The manual `Build Publication Format` workflow builds one selected profile per run; a successful build is for review, offline reading, or publication preparation and does not by itself constitute formal release approval.

## Project orientation

The project uses a **learning-and-synthesis + problem-driven** approach. Its organization reflects a pedagogical view that doing philosophy is not identical to studying what earlier thinkers said. Intellectual history and the history of philosophy are important, but philosophical training also involves confronting problems directly, distinguishing concepts, comparing reasons, constructing counterexamples, and testing positions.

Accordingly, the book uses historical and contemporary material in the service of philosophical problems rather than organizing itself mainly as a catalogue of thinkers or schools. This orientation is expressed primarily through chapter structure, exercises, the research studio, and reading routes rather than through a long methodological manifesto.

## Source of truth

The formal manuscript has only the following sources:

- Homepage and textbook entry point: `index.qmd`
- Main text and front/back matter: `manuscript/*.qmd`
- Bibliography database: `references.bib`

Shared book structure lives in `_quarto.yml`; Web configuration lives in `_quarto-web.yml`; PDF, DOCX, EPUB, and LaTeX use separate profiles. Publication intent is declared in `publishing.yaml`, and website styling lives in `book.css`.

`textbook/` preserves the pre-migration historical LaTeX version for auditing and version tracing only. It is not a formal manuscript source and does not participate in editing, validation, or builds. TeX/LaTeX-style syntax inside mathematical formulas is Quarto/Pandoc math syntax and does not imply a return to a LaTeX document workflow.

## Online reading experience

The current Web Edition treats the website itself as the primary development deliverable rather than a by-product of the build process. The site provides:

- a left-side “Book contents” navigation for moving across chapters, a desktop right-side “On this page” navigation, and a collapsible chapter table of contents near the title on narrow screens;
- full-site search, previous/next chapter navigation, and back-to-top controls;
- reader mode for focused reading of long chapters;
- hover previews for citations and footnotes, plus click-through citation details and return links from chapter bibliography entries;
- right-side “Report an issue” and “View source” entry points;
- footer notices across the book for open access, feedback, and version status;
- structured GitHub feedback forms that distinguish “manuscript corrections/content suggestions” from “web display/reading problems.”

Open reading has no paywall. Financial support is entirely voluntary and does not affect reading access or future public updates; corrections, discussion, teaching feedback, dissemination, and bibliographic suggestions are also treated as forms of support.

## Book structure

### Part I: Knowledge, Skepticism, and Reasons

1. What Is Knowledge, and Why Do We Need It?
2. Skepticism, Luck, and the Boundaries of Knowledge
3. How Do Reasons Support Belief?

### Part II: Sources of Knowledge, Social Systems, and Rational Models

4. How Do Experience, Memory, and the A Priori Become Sources of Knowledge?
5. How Do Other People, Experts, and Institutions Produce Knowledge Together?
6. Probability, Models, and Rational Decision-Making

### Part III: Epistemic Value, Technological Environments, and Comparative Methods

7. Why Are Knowledge, Understanding, and Wisdom Valuable?
8. How Do Digital Environments and Artificial Intelligence Reshape Knowing?
9. How Does Comparative Epistemology Change Our Questions?

The book also includes an open-access and support statement, a preface, a study and writing guide, a research studio, exercise hints, a glossary, and references.

## Feedback and maintenance

Readers can use “Report an issue” directly from the right side of any long chapter, or open GitHub Issues:

<https://github.com/ChongLiuPhil/epistemology-textbook/issues/new/choose>

When reporting manuscript content, it is helpful to include the page link, chapter or section, a description of the problem, and any suggested revision or reference source. When reporting website problems, please also include the device and browser environment.

For scholarly citations that require precise version tracking, in addition to author, title, chapter, page link, and access date, you may record the corresponding Git commit so that a specific revision of this continuously updated work can be identified.

## Local development

Python 3, GNU Make, and Quarto are required. The current development workflow does not require LaTeX/XeLaTeX.

```sh
make check    # validate QMD, math-layout risks, bibliography metadata, project structure, reading/feedback, PPF, and publication boundaries
make preview  # launch local Quarto HTML preview
make html     # generate the HTML reading edition
make all      # currently equivalent to a full HTML development build
make clean    # remove _book/ and .quarto/
```

Quarto HTML output is written to `_book/`. `make check` blocks deterministic bibliographic errors such as missing citation keys, duplicate or malformed DOIs, and invalid URLs. Bibliography entries that are not currently cited are reported as audit information rather than deleted automatically.

External website availability depends on publishers, rate limits, authentication, and network state, so it is not part of the blocking canonical Web publication gate. The publication/reading profile is documented in `docs/publication-profile.zh-CN.md`. The repository also has a separate `External Link Audit`: it runs automatically when relevant manuscript, bibliography, web configuration, or audit-script changes enter `main`, and it also supports weekly and manual runs. It renders the complete site and checks the external links in the final HTML, treating only explicit HTTP 404/410 responses as broken-link failures; other network problems remain warnings.

## On-demand publication formats

`_quarto.yml` now contains shared configuration and declares `web` as the default profile. Day-to-day Pull Request and `main` workflows render and publish only the HTML Web profile. When review, offline reading, or publication preparation requires it, the manual `Build Publication Format` workflow explicitly selects one of EPUB, PDF, DOCX, or LaTeX.

These artifacts use the same `index.qmd`, `manuscript/*.qmd`, and `references.bib` sources as the Web edition. Web output is written to `_book/`; on-demand formats are written to `_publication/<format>/`. A successful manual build does not by itself constitute an approved formal release; release state is tracked separately in `docs/release-status.zh-CN.md`.

## PPF and Cloudflare publication status

This project adopts Personal Publishing Framework v0.1.0-draft at pinned commit `21a5360727167bad6f399477ded073431645fa1d`. The declarative contract is `publishing.yaml`; the adoption note is `docs/ppf-adoption.md`.

Cloudflare Workers is the verified current Web provider and the workers.dev URL is the canonical publication identity. GitHub Pages has been retired under the recorded `RETIRE` legacy policy. Source visibility, publication authorization, publication visibility, access policy, and canonical identity remain separate PPF concepts; the current textbook is public with no access restriction.

## CI and deployment

At the Pull Request stage, repository checks validate canonical QMD sources, bibliography metadata, PPF/Cloudflare contracts, reader-facing configuration, complete Web rendering, internal links/assets/anchors, and rendered HTML integrity.

`make web-publish-check` is the single canonical Web publication quality gate. GitHub Actions calls it for verification; Cloudflare Workers Builds calls the same gate before updating the workers.dev production site. Normal CI does not deploy GitHub Pages.

External HTTP links are audited separately so temporary third-party failures do not become part of the canonical publication gate.

## Editing principles

Edit `index.qmd`, `manuscript/*.qmd`, and `references.bib` directly. Use Quarto/Pandoc citation syntax for references; use Markdown/Pandoc syntax supported directly by Quarto for formulas, footnotes, tables, and callouts. Run at least `make check` before committing, and use `make preview` or `make html` when checking the final web presentation.

See `CONTRIBUTING.md` for detailed conventions.


## Collaboration governance: HARC-lite

This repository uses a project-specific HARC-lite collaboration layer so that a new human collaborator or AI agent can reconstruct the current project state without relying on prior chat history.

For zero-context onboarding, start with `START_HERE.zh-CN.md`. Stable content and form principles live in `core/CONTENT_CORE.zh-CN.md` and `core/FORM_CORE.zh-CN.md`; durable decisions are recorded in `core/DECISION_LOG.zh-CN.md`; current objectives, tasks, and pending human decisions live under `docs/working-memory/`.

The adopted upstream HARC revision is pinned in `HARC_MANIFEST.yaml` and does not automatically follow upstream changes. Internal governance is Chinese-canonical and does not require a full English mirror for every internal file; the public README remains bilingual.

`make check` now also validates repository-backed collaboration state so stale publishing instructions, legacy-source confusion, and unresolved licensing status cannot silently become current project truth.