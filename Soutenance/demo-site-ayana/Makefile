PDFNAME = Demo_Ayana_LouisHauseux.pdf
JOBNAME = Demo_Ayana_LouisHauseux

all: $(PDFNAME)

$(PDFNAME): main.tex
	latexmk -jobname=$(JOBNAME) main.tex

clean:
	latexmk -jobname=$(JOBNAME) -C
	@rm -f $(JOBNAME).nav $(JOBNAME).snm
