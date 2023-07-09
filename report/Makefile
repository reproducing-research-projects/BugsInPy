out/main.pdf: main.tex
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) nopreserveroot/latexmk -outdir=out/ -auxdir=aux/ -pdf main
	docker run --volume $(PWD):$(PWD) --workdir $(PWD) debian:12-slim chown --recursive $(UID):$(GID) aux/ out/

clean:
	rm -rf aux/ out/
