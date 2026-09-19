.PHONY: check governance-check preview html all clean help

help:
	@echo "Available targets:"
	@echo "  make governance-check - validate repository-backed collaboration state"
	@echo "  make check            - validate governance, canonical Quarto sources, bibliography, and project structure"
	@echo "  make preview          - start the local Quarto HTML preview"
	@echo "  make html             - render the HTML reading edition"
	@echo "  make all              - run the complete HTML development build"
	@echo "  make clean            - remove Quarto build output"

governance-check:
	python3 scripts/check_repository_state.py

check: governance-check
	python3 scripts/check_quarto.py
	python3 scripts/check_references.py

preview: check
	quarto preview --profile web

html: check
	quarto render --profile web

all: html

clean:
	rm -rf _book _publication .quarto
