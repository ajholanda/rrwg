PROJ := rrwg
PREFIX := /usr/local
BINPATH := $(PREFIX)/bin/$(PROJ)
MANPATH := $(PREFIX)/man/man1/$(PROJ).1

INSTALL := apt install
PIP_PKG := python3-pip

default: help

install: $(PROJ).py $(PROJ).1 setup
	@install -v rrwg.py $(BINPATH)
	@install -v rrwg.1 $(MANPATH)
	@echo "Successfully installed!"
	@echo "See man rrwg"

setup: pip
	pip install -r requirements.txt

pip:
ifeq (, $(shell which pip))
	$(INSTALL) $(PIP_PKG)
endif

uninstall:
	@rm -vf $(BINPATH)
	@rm -vf $(MANPATH)
	@echo "Successfully Uninstalled!"


rrwg.1: rrwg.md pandoc
	pandoc -s -t man $< -o $@

man: rrwg.1

pandoc:
ifeq (, $(shell which pandoc))
	$(INSTALL) pandoc
endif

clean:
	$(RM) *.dat *.log *.pdf $(PROJ).1

tidy: clean
	$(RM) -r __pycache__ *.pyc

help:
	@echo "---------------------------------------------------------------------"
	@echo "* RRWG - possible targets:"
	@echo "make rrwg.1 | man"
	@echo " \t=> Generate man page of the program. Depends on Pandoc."
	@echo "make clean"
	@echo " \t=> Clean up all generated files."
	@echo "make tidy"
	@echo " \t=> Clean up all generated files, including Python-generated."
	@echo "make install"
	@echo "\t=> Install the program and its manual using as prefix $(PREFIX)."
	@echo "\t   If you intend to install them in a different directory,"
	@echo "\t   change the variable PREFIX inside 'Makefile' file."
	@echo "make uninstall"
	@echo "\t=> Remove the program from prefix $(PREFIX)."
	@echo "---------------------------------------------------------------------"

.PHONY: clean default help install man pandoc setup uninstall
