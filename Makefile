LATEX ?= tectonic

.PHONY: all article example dist clean

all: article example

article:
	python tools/check_article.py
	mkdir -p build
	$(LATEX) -o build article.tex

example:
	mkdir -p example/build
	cd example && $(LATEX) -o build example.tex

# Zip for Overleaf: article, class, included figures and generated table.
dist: 
	rm -rf dist
	mkdir -p dist/misis-article
	cp misisarticle.cls article.tex README.md LICENSE dist/misis-article/
	cp -R figures dist/misis-article/
	cp -R results dist/misis-article/
	cd dist && zip -r misis-article.zip misis-article
	rm -rf dist/misis-article

clean:
	rm -rf build example/build dist
	rm -f *.aux *.log *.out *.toc *.bbl *.blg *.bcf *.run.xml *.xdv *.synctex.gz *.fls *.fdb_latexmk
	rm -f article.pdf example/example.pdf
