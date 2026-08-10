all: main.pdf

LATEXCMD=lualatex

main.pdf: main.tex
	TEXINPUTS=.:theme//:latex-inria-fonts//: \
	${LATEXCMD} -file-line-error -halt-on-error main.tex
	bibtex main || true
	TEXINPUTS=.:theme//:latex-inria-fonts//: \
	${LATEXCMD} -file-line-error -halt-on-error main.tex
	TEXINPUTS=.:theme//:latex-inria-fonts//: \
	${LATEXCMD} -file-line-error -halt-on-error main.tex

clean:
	@rm -f main.aux main.log main.nav main.out main.snm main.toc main.pdf main.fls main.fdb_latexmk main.blg main.bbl
