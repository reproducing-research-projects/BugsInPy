UID = $(shell id -u)
GID = $(shell id -g)
fix_perms = docker run --volume $(PWD):$(PWD) --workdir $(PWD) debian:12-slim chown --recursive $(UID):$(GID)

all: out/main.pdf

meat.tex: meat.md
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) pandoc/core --to=latex --output=$@ $<
	$(fix_perms) $@

out/main.pdf: main.tex meat.tex
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) nopreserveroot/latexmk -outdir=out/ -auxdir=aux/ -pdf main
	$(fix_perms) aux/ out/

out/meat.docx: meat.md
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) pandoc/core --to=docx --output=$@ $<
	$(fix_perms) $@

clean:
	$(fix_perms) *
	rm -rf aux/ out/ meat.tex
