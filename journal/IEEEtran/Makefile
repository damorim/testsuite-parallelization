NAME:=bare_jrnl_compsoc

# To update, run: latex-process-inputs -makefilelist main.tex
TEX_FILES = \
bare_jrnl_compsoc.tex

PDFS := $(NAME).pdf
TEMP_TXTS := $(patsubst %.pdf,%.txt,$(PDFS))
OUTPUTS_SPELL := $(TEMP_TXTS)

.DEFAULT_GOAL := pdf

pdf:
#	-rm -f $(NAME).aux
	latexmk -bibtex -pdf $(NAME)

final: pdf
	@echo '******** Did you spell-check the paper? ********'
	pdffonts $(NAME).pdf; fi

read: pdf
	evince main.pdf &
clean:
	-rm -f *aux *bbl *blg *log *.dvi main.pdf *.fls *.fdb_latexmk *~ *.out

check: $(TEMP_TXTS)
	cat $^ | aspell list --extra-dicts=./okwords.en.pws --lang en | sort | uniq

%.txt: main.pdf
	pdftotext $<

%.err: %.txt
	cat $^ | aspell list --extra-dicts=./okwords.en.pws --lang en | sort | uniq

.PHONY: all

tags: TAGS
TAGS: ${TEX_FILES}
	etags ${TEX_FILES}
