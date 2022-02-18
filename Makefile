PREFIX := /usr/local

CMD := ansible-playbook \
	--connection=local \
	--extra-vars "basedir=$(PREFIX)" \
	main.yml 

INSTALL := sudo apt install

install: ansible
	$(CMD) --tags install

uninstall: ansible
	$(CMD) --tags uninstall

ansible:
ifeq (, $(shell which ansible))
	$(INSTALL) ansible
endif

clean:
	$(RM) *.dat *.log __pycache__

.PHONY: clean
