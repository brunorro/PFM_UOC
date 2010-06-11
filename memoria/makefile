PDFLATEX="pdflatex"
BIBTEX="bibtex"
CAPITULOS=introduccion.tex procesado.tex aplicaciones.tex resultados.tex gpl.tex cc-by-sa.tex resumen-cc.tex resumen-mem.tex
BIBLIO=biblio
DIAGRAMAS=diagramas/*.tex
#IMAGENES=imagenes/*.jpg
FILES_AUX=*.log *.aux *.out *.lof *.lot *.toc *.nav *.snm *.blg 
FILES_GEN=*.log *.aux *.out *.lof *.lot *.toc *.nav *.snm *.blg *.pdf

all: memoria.pdf slides.pdf

memoria.pdf: memoria.tex ${CAPITULOS} ${DIAGRAMAS} 
	${PDFLATEX} memoria.tex

slides.pdf: slides.tex
	${PDFLATEX} slides.tex

biblio.bbl: biblio.bib
	${BIBTEX} ${BIBLIO}

clean:
	rm $(FILES_AUX)

cillitbang:
	rm $(FILES_GEN)
