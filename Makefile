# Repository-level convenience targets.
# The canonical PDF build logic remains in textbook/Makefile.

.PHONY: check pdf web-source web clean help

help:
	@echo "Available targets:"
	@echo "  make check       - run source consistency checks"
	@echo "  make pdf         - build the complete textbook PDF"
	@echo "  make web-source  - generate and validate Quarto pages from LaTeX"
	@echo "  make web         - render the HTML reading site with Quarto"
	@echo "  make clean       - remove temporary PDF and web build output"

check:
	$(MAKE) -C textbook check
	python3 scripts/build_web.py --check

pdf:
	$(MAKE) -C textbook pdf

web-source:
	python3 scripts/build_web.py --check

web: web-source
	quarto render --to html

clean:
	$(MAKE) -C textbook clean
	rm -rf _book website/generated .quarto
