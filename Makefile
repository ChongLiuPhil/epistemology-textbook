# Repository-level convenience targets.
# The canonical build logic remains in textbook/Makefile.

.PHONY: check pdf clean help

help:
	@echo "Available targets:"
	@echo "  make check  - run source consistency checks"
	@echo "  make pdf    - build the complete textbook PDF"
	@echo "  make clean  - remove the temporary build directory"

check:
	$(MAKE) -C textbook check

pdf:
	$(MAKE) -C textbook pdf

clean:
	$(MAKE) -C textbook clean
