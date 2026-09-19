PDFNAME = PhD_Defense_2026-09-08_LouisHauseux.pdf
JOBNAME = PhD_Defense_2026-09-08_LouisHauseux

all: $(PDFNAME)

$(PDFNAME): main.tex
	latexmk -jobname=$(JOBNAME) main.tex

clean:
	latexmk -jobname=$(JOBNAME) -C
	@rm -f $(JOBNAME).nav $(JOBNAME).snm
