# Makefile — build the LaTeX manuscript from the repo root.
#
#   make            # full build (engine -> biber -> engine -> engine), PDF copied to ./main.pdf
#   make quick      # single fast pass (no biber), for quick previews
#   make ENGINE=lualatex   # override the TeX engine (default: pdflatex; needs luatexko)
#   make view       # build then open the PDF
#   make clean      # remove build artifacts, keep the PDF
#   make cleanall   # remove build artifacts and the PDF

ENGINE   ?= pdflatex
SRCDIR   := manuscript
MAIN     := main
PDF      := $(SRCDIR)/$(MAIN).pdf
TEXFLAGS := -interaction=nonstopmode -halt-on-error -file-line-error
SOURCES  := $(wildcard $(SRCDIR)/*.tex) $(wildcard $(SRCDIR)/chapters/*.tex) $(SRCDIR)/references.bib

.PHONY: all pdf quick view clean cleanall

all: pdf

# Full build: run inside manuscript/ so \include and \addbibresource paths resolve,
# then copy the finished PDF up to the repo root for convenience.
pdf: $(PDF)
	@cp -f $(PDF) ./$(MAIN).pdf
	@echo "==> Built ./$(MAIN).pdf (engine: $(ENGINE))"

$(PDF): $(SOURCES)
	cd $(SRCDIR) && $(ENGINE) $(TEXFLAGS) $(MAIN).tex
	cd $(SRCDIR) && biber $(MAIN)
	cd $(SRCDIR) && $(ENGINE) $(TEXFLAGS) $(MAIN).tex
	cd $(SRCDIR) && $(ENGINE) $(TEXFLAGS) $(MAIN).tex

# Single pass — fast preview, skips bibliography resolution.
quick:
	cd $(SRCDIR) && $(ENGINE) $(TEXFLAGS) $(MAIN).tex
	@cp -f $(PDF) ./$(MAIN).pdf
	@echo "==> Quick build ./$(MAIN).pdf (no biber)"

view: pdf
	@xdg-open ./$(MAIN).pdf >/dev/null 2>&1 || open ./$(MAIN).pdf 2>/dev/null || echo "Open ./$(MAIN).pdf manually"

clean:
	cd $(SRCDIR) && rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).bcf $(MAIN).blg \
		$(MAIN).log $(MAIN).out $(MAIN).toc $(MAIN).run.xml \
		$(MAIN).fls $(MAIN).fdb_latexmk $(MAIN).synctex.gz
	cd $(SRCDIR) && rm -f chapters/*.aux

cleanall: clean
	rm -f $(PDF) ./$(MAIN).pdf
