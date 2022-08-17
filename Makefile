PREFIX 	:= /usr/local/bin
BINPATH := $(PREFIX)/rrwg
CFLAGS 	:= -Wall -g
TEX 	:= xetex

rrwg: rrwg.c
	$(CC) $(CFLAGS) $< -o $@

rrwg.c: rrwg.w cweb/ctangle
	$(CTANGLE) $<

rrwg.pdf: rrwg.tex
	$(TEX) $<

rrwg.tex: rrwg.w cweb/cweave
	$(CWEAVE) $<

install: rrwg
	-install $< $(BINPATH)
	@echo "Successfully installed!"
phony += install

uninstall:
	-$(RM) -v $(BINPATH)
	@echo "Successfully Uninstalled!"

clean:
	$(RM) -r $(trash) *.c *.idx *.log *.scn *.tex
phony += clean

include cweb.mk
CTANGLE := cweb/ctangle
CWEAVE := cweb/cweave

help:
	@echo "---------------------------------------------------------------------"
	@echo "* RRWG - possible targets:"
	@echo "make doc"
	@echo " \t=> Generate CWEB documentation of the program. Depends on TeX."
	@echo "make clean"
	@echo " \t=> Clean up all generated files."
	@echo "make install"
	@echo "\t=> Install the program and its manual using as prefix $(PREFIX)."
	@echo "\t   If you intend to install them in a different directory,"
	@echo "\t   change the variable PREFIX inside 'Makefile' file."
	@echo "make uninstall"
	@echo "\t=> Remove the program from prefix $(PREFIX)."
	@echo "---------------------------------------------------------------------"
phony += help

.PHONY: $(phony)
