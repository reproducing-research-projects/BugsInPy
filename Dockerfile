FROM continuumio/miniconda3:23.3.1-0
MAINTAINER faustinoaq <faustino.aguilar@up.ac.pa>

RUN apt-get update
RUN apt-get -y install git nano dos2unix build-essential

WORKDIR /home/user

COPY ./framework /home/user/BugsInPy/framework
COPY ./projects /home/user/BugsInPy/projects

ENV PATH /home/user/BugsInPy/framework/bin:$PATH

CMD ["/bin/bash"]
