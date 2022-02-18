PROJ := rrwg
PREFIX := /usr/local
BINPATH := $(PREFIX)/bin/$(PROJ)

CMD := ansible-playbook \
	--connection=local \
	--extra-vars "basedir=$(PREFIX)" \
	main.yml 

INSTALL := apt install

default: help

install: rrwg.py rrwg.1
	@install -v rrwg.py $(BINPATH)
	@install -v rrwg.1 $(MANPATH)
	@echo "Successfully installed!"

uninstall:
	@rm -vf $(BINPATH)
	@rm -vf rrwg.1 $(MANPATH)
	@echo "Successfully Uninstalled!"


rrwg.1: rrwg.md pandoc
	pandoc -s -t man $< -o $@

pandoc:
ifeq (, $(shell which pandoc))
	$(INSTALL) pandoc
endif

clean:
	$(RM) *.dat *.log *.pdf *.pyc $(PROJ).1

tidy: clean
	$(RM) -r __pycache__

help:
	@echo "---------------------------------------------------------------------"
	@echo "* RRWG - possible targets:"
	@echo "make rrwg.1"
	@echo " \t=> Generate man page of the program. Depends on Pandoc."
	@echo "make clean"
	@echo " \t=> Clean up all generated files."
	@echo "make tidy"
	@echo " \t=> Clean up all generated files, including Python-generated."
	@echo "make install"
	@echo "\t=> Install the program using as prefix $(PREFIX)."
	@echo "\t   If you intend to install in a different directory,"
	@echo "\t   change the variable PREFIX inside 'Makefile' file."
	@echo "make uninstall"
	@echo "\t=> Remove the program from prefix $(PREFIX)."
	@echo "---------------------------------------------------------------------"

.PHONY: clean default help install pandoc uninstall
