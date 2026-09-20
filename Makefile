QUARTO ?= quarto

.PHONY: check governance-check stack-check preview html web-publish-check cloudflare-build all clean help

help:
	@echo "Available targets:"
	@echo "  make governance-check   - validate repository-backed collaboration and stack state"\n	@echo "  make stack-check        - validate AHICP/PPF/Vault-interface cross-contract consistency"\n	@echo "  make check              - validate governance, Quarto sources, math layout, bibliography, PPF, and Cloudflare contract"
	@echo "  make preview            - start the local Quarto Web preview"
	@echo "  make html               - render the Web reading edition"
	@echo "  make web-publish-check  - canonical source -> Web render -> rendered artifact validation"
	@echo "  make cloudflare-build   - install pinned Quarto if needed, then run web-publish-check"
	@echo "  make all                - run the complete Web publication check"
	@echo "  make clean              - remove generated output"

governance-check:
	python3 scripts/check_repository_state.py
	python3 scripts/check_stack_consistency.py

stack-check:
	python3 scripts/check_stack_consistency.py

check: governance-check
	python3 scripts/check_quarto.py
	python3 scripts/check_math_layout.py
	python3 scripts/check_references.py
	python3 scripts/check_cloudflare_readiness.py

preview: check
	$(QUARTO) preview --profile web

html: check
	$(QUARTO) render --profile web

web-publish-check: check
	$(QUARTO) render --profile web
	python3 scripts/check_rendered_html.py

cloudflare-build:
	bash scripts/cloudflare_build.sh

all: web-publish-check

clean:
	rm -rf _book _publication .quarto
