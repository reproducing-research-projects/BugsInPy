FROM continuumio/miniconda3
MAINTAINER faustinoaq <faustino.aguilar@up.ac.pa>
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y install git build-essential
RUN git clone https://github.com/faustinoaq/BugsInPy ~/BugsInPy
RUN echo "export PATH=$PATH:~/BugsInPy/framework/bin" >> ~/.bashrc
RUN bugsinpy-testall
CMD ["/usr/bin/bash"]
