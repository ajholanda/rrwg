PROJ := rrwg
PREFIX := /usr/local

CMD := ansible-playbook \
	--connection=local \
	--extra-vars "basedir=$(PREFIX)" \
	main.yml 

INSTALL := sudo apt install

default: help

install: ansible rrwg.1
	$(CMD) --tags install

uninstall: ansible
	$(CMD) --tags uninstall

ansible:
ifeq (, $(shell which ansible))
	$(INSTALL) ansible
endif

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

.PHONY: ansible clean default help install pandoc uninstall
