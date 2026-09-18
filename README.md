# How Do We Know? — A Problem-Driven Epistemology

[English](README.md) | [中文](README.zh-CN.md)

This is a Chinese-language epistemology learning textbook organized and continuously revised by Chong Liu. It grows primarily out of selecting, integrating, comparing, and problematizing materials encountered in the course of studying epistemology; it does not require the construction of an original philosophical system as its main goal. Authorial judgment is concentrated in problem framing, source selection, interpretation, comparison, and pedagogical organization. Quarto remains the sole formal manuscript system.

## Current stage: Web Edition Development

The web edition is currently the primary development and publication target. The normal workflow is:

`QMD → validation → HTML → GitHub Pages`

Whenever changes enter `main` through a Pull Request, GitHub Actions revalidates the canonical QMD sources, renders the complete HTML site, and deploys the validated `_book/` output to the public website. Therefore, changes to the manuscript, structure, and web styling should ultimately appear in the actual readable site.

Read online: <https://chongliuphil.github.io/epistemology-textbook/>

Open access and support: <https://chongliuphil.github.io/epistemology-textbook/manuscript/00-open-access-and-support.html>

EPUB, PDF, and DOCX are not part of the day-to-day Pages CI. A separate manual publication-format workflow may generate them from the same canonical QMD sources for layout testing and editorial review; a successful build is not itself a formal release approval.

## Source of truth

The formal manuscript has only the following sources:

- Homepage and textbook entry point: `index.qmd`
- Main text and front/back matter: `manuscript/*.qmd`
- Bibliography database: `references.bib`

The book structure and HTML configuration live in `_quarto.yml`, and the website styling lives in `book.css`.

`textbook/` preserves the pre-migration historical LaTeX version for auditing and version tracing only. It is not a formal manuscript source and does not participate in editing, validation, or builds. TeX/LaTeX-style syntax inside mathematical formulas is Quarto/Pandoc math syntax and does not imply a return to a LaTeX document workflow.

## Online reading experience

The current Web Edition treats the website itself as the primary development deliverable rather than a by-product of the build process. The site provides:

- a left-side “Book contents” navigation for moving across chapters and a right-side “On this page” navigation for locating material within the current chapter;
- full-site search, previous/next chapter navigation, and back-to-top controls;
- reader mode for focused reading of long chapters;
- hover previews for citations and footnotes;
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
make check    # validate QMD, bibliography metadata, project structure, reading/feedback configuration, and HTML-only workflow
make preview  # launch local Quarto HTML preview
make html     # generate the HTML reading edition
make all      # currently equivalent to a full HTML development build
make clean    # remove _book/ and .quarto/
```

Quarto HTML output is written to `_book/`. `make check` blocks deterministic bibliographic errors such as missing citation keys, duplicate or malformed DOIs, and invalid URLs. Bibliography entries that are not currently cited are reported as audit information rather than deleted automatically.

External website availability depends on publishers, rate limits, authentication, and network state, so it is not part of the blocking gate for Pages deployment. The repository has a separate `External Link Audit`: it runs automatically when relevant manuscript, bibliography, web configuration, or audit-script changes enter `main`, and it also supports weekly and manual runs. It renders the complete site and checks the external links in the final HTML, treating only explicit HTTP 404/410 responses as broken-link failures; other network problems remain warnings.

## On-demand publication formats

The current day-to-day Pages workflow does not generate:

- EPUB
- PDF
- DOCX

A separate manual publication-format workflow can generate these formats for layout checks and future publication preparation. They still derive from `index.qmd`, `manuscript/*.qmd`, and `references.bib`, so they do not create a second manuscript source; formal release remains subject to separate author review.

## CI and deployment

At the Pull Request stage:

- check canonical QMD sources;
- validate bibliography citation keys, DOI/URL metadata, and project structure;
- verify open-reading configuration, feedback entry points, and the left/right navigation labels visible to readers;
- install Quarto;
- render the complete HTML site;
- validate site-wide internal links, static assets, page anchors, and duplicate HTML IDs;
- verify that key HTML pages and important reading-interface elements exist;
- verify that EPUB/PDF/DOCX files were not generated unexpectedly.

After merging into `main`, and only after all of the above validation passes, the workflow deploys the `_book/` produced by that same build as a GitHub Pages artifact. Deployment does not use a script to force-push a `gh-pages` branch. External HTTP reachability is handled by the separate audit: it runs immediately when relevant content enters `main`, and also on weekly and manual schedules, so temporary failures of third-party sites do not become part of the Pages publication gate.

## Editing principles

Edit `index.qmd`, `manuscript/*.qmd`, and `references.bib` directly. Use Quarto/Pandoc citation syntax for references; use Markdown/Pandoc syntax supported directly by Quarto for formulas, footnotes, tables, and callouts. Run at least `make check` before committing, and use `make preview` or `make html` when checking the final web presentation.

See `CONTRIBUTING.md` for detailed conventions.


## Collaboration governance: HARC-lite

This repository uses a project-specific HARC-lite collaboration layer so that a new human collaborator or AI agent can reconstruct the current project state without relying on prior chat history.

For zero-context onboarding, start with `START_HERE.zh-CN.md`. Stable content and form principles live in `core/CONTENT_CORE.zh-CN.md` and `core/FORM_CORE.zh-CN.md`; durable decisions are recorded in `core/DECISION_LOG.zh-CN.md`; current objectives, tasks, and pending human decisions live under `docs/working-memory/`.

The adopted upstream HARC revision is pinned in `HARC_MANIFEST.yaml` and does not automatically follow upstream changes. Internal governance is Chinese-canonical and does not require a full English mirror for every internal file; the public README remains bilingual.

`make check` now also validates repository-backed collaboration state so stale publishing instructions, legacy-source confusion, and unresolved licensing status cannot silently become current project truth.