.PHONY: check html epub web all clean help

help:
	@echo "Available targets:"
	@echo "  make check  - validate canonical Quarto sources and citations"
	@echo "  make html   - render the HTML reading edition"
	@echo "  make epub   - render the EPUB ebook"
	@echo "  make web    - alias for make html"
	@echo "  make all    - render all configured Quarto formats"
	@echo "  make clean  - remove Quarto build output"

check:
	python3 scripts/check_quarto.py

html: check
	quarto render --to html

epub: check
	quarto render --to epub

web: html

all: check
	quarto render

clean:
	rm -rf _book .quarto
