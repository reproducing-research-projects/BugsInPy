FROM continuumio/miniconda3
MAINTAINER faustinoaq <faustino.aguilar@up.ac.pa>

RUN apt-get update
RUN apt-get -y install git nano build-essential
RUN git clone https://github.com/faustinoaq/BugsInPy ~/BugsInPy
RUN echo "export PATH=$PATH:~/BugsInPy/framework/bin" >> ~/.bashrc

CMD ["/bin/bash"]
