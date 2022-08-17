CFLAGS := -Wall -g
TEX := xetex

rrwg: rrwg.c
	$(CC) $(CFLAGS) $<

rrwg.c: rrwg.w
	$(CTANGLE) $<

rrwg.pdf: rrwg.tex
	$(TEX) $<

rrwg.tex: rrwg.w
	$(CWEAVE) $<

include cweb.mk
CTANGLE := cweb/ctangle
CWEAVE := cweb/cweave
