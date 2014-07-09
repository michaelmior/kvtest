# GNU Make automatic variables
# $< is the first prerequisite
# $* is the stem of target with which rule match (e.g., foo of foo.c) - what matches with % in a rulek
# $@ is the name of the target

targets = paper

built_figtargets =  

base_figtargets = 

all: ${targets:%=%.pdf}

paper.pdf: paper.tex paper.bib ${built_figtargets:%=%.pdf} ${base_figtargets}
	pdflatex paper.tex
	bibtex paper
	pdflatex paper.tex
	pdflatex paper.tex

clean:
	/bin/rm -f ${targets:%=%.aux}
	/bin/rm -f ${targets:%=%.blg}
	/bin/rm -f ${targets:%=%.bbl}
	/bin/rm -f ${targets:%=%.log}
	/bin/rm -f ${targets:%=%.dvi}
	/bin/rm -f ${targets:%=%.nav}
	/bin/rm -f ${targets:%=%.out}
	/bin/rm -f ${targets:%=%.snm}
	/bin/rm -f ${targets:%=%.toc}
	/bin/rm -f ${built_figtargets:%=%.eps}

distclean: clean
	/bin/rm -f ${targets:%=%.pdf}
	/bin/rm -f ${built_figtargets:%=%.pdf}

fullclean: distclean
