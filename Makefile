PROJ := rrwg
PREFIX 	:= /usr/local/bin
BINPATH := $(PREFIX)/$(PROJ)
PIPPKG := python3-pip

default: help
phony += default

install: dist/$(PROJ) setup
	@install -v $< $(BINPATH)
	@install -v $(PROJ).1 $(MANPATH)
	@echo "Successfully installed!"
	@echo "See man rrwg"
phony += install

dist/$(PROJ): $(PROJ)
	pyinstaller --noconfirm --clean --onefile --name $^ __main__.py

setup: pip
	pip install -r requirements.txt
phony += setup

pip:
ifeq (, $(shell which pip))
	$(INSTALL) $(PIPPKG)
endif
phony += pip

uninstall:
	@rm -vf $(BINPATH)
	@echo "Successfully Uninstalled!"
phony += uninstall

clean:
	$(RM) *.dat *.log *.pdf $(PROJ).1
phony += clean

tidy: clean
	@$(RM) -rv __pycache__ *.spec dist build
	@find . -name *.pyc -delete
phony += tidy

help:
	@echo "---------------------------------------------------------------------"
	@echo "* RRWG - possible targets:"
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
phony += help

.PHONY: $(phony)
