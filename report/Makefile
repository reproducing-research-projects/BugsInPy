UID = $(shell id -u)
GID = $(shell id -g)

all: out/main.pdf

meat.tex: meat.md
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) pandoc/core --to=latex --output=meat.tex meat.md
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) debian:12-slim chown --recursive $(UID):$(GID) meat.tex

out/main.pdf: main.tex meat.tex
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) nopreserveroot/latexmk -outdir=out/ -auxdir=aux/ -pdf main
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) debian:12-slim chown --recursive $(UID):$(GID) aux/ out/

out/main.docx: meat.md
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) pandoc/core --to=docx --output=out/meat.docx meat.md
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) debian:12-slim chown --recursive $(UID):$(GID) out/meat.docx

clean:
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) debian:12-slim chown --recursive $(UID):$(GID) *
	rm -rf aux/ out/ meat.tex
