PDFLATEX="pdflatex"
BIBTEX="bibtex"
CAPITULOS=gpl.tex introduccion.tex procesado.tex aplicaciones.tex resultados.tex
BIBLIO=biblio
DIAGRAMAS=diagramas/*.tex
#IMAGENES=imagenes/*.jpg
FILES_AUX=*.log *.aux *.out *.lof *.toc *.blg *.pdf

all: memoria.pdf 

memoria.pdf: memoria.tex ${CAPITULOS} ${DIAGRAMAS} 
	${PDFLATEX} memoria.tex

biblio.bbl: biblio.bib
	${BIBTEX} ${BIBLIO}
clean:
	rm $(FILES_AUX)
