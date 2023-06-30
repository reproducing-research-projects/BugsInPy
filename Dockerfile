FROM continuumio/miniconda3
MAINTAINER faustinoaq <faustino.aguilar@up.ac.pa>
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y install git build-essential
RUN git clone https://github.com/faustinoaq/BugsInPy ~/BugsInPy
CMD ["/usr/bin/bash"]
