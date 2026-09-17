.PHONY: check preview html all clean help

help:
	@echo "Available targets:"
	@echo "  make check   - validate canonical Quarto sources, bibliography, and project structure"
	@echo "  make preview - start the local Quarto HTML preview"
	@echo "  make html    - render the HTML reading edition"
	@echo "  make all     - run the complete HTML development build"
	@echo "  make clean   - remove Quarto build output"

check:
	python3 scripts/check_quarto.py
	python3 scripts/check_references.py

preview: check
	quarto preview --to html

html: check
	quarto render --to html

all: html

clean:
	rm -rf _book .quarto
