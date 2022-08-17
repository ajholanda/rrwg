repo := https://github.com/ascherer/cweb.git

cweb/ctangle: cweb/ctangle.c
	cd cweb && make

cweb/cweave: cweb/cweave.c
	cd cweb && make

cweb:
	if [ ! -d cweb ]; then mkdir cweb; fi
trash += cweb

cweb/ctangle.c cweb/cweave.c:
	git clone $(repo)
