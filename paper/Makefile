NAME:=main

# To update, run: latex-process-inputs -makefilelist main.tex
TEX_FILES = \
main.tex 

pdf:
#	-rm -f $(NAME).aux
	latexmk -bibtex -pdf $(NAME)

final: pdf
	@echo '******** Did you spell-check the paper? ********'
	pdffonts $(NAME).pdf; fi

clean:
	-rm -f *aux *bbl *blg *log *.dvi main.pdf

tags: TAGS
TAGS: ${TEX_FILES}
	etags ${TEX_FILES}
