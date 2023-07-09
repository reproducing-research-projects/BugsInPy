FROM continuumio/miniconda3:23.3.1-0
MAINTAINER faustinoaq <faustino.aguilar@up.ac.pa>

RUN useradd -ms /bin/bash user
RUN apt-get update
RUN apt-get -y install git nano build-essential

WORKDIR /home/user

COPY . /home/user/BugsInPy

RUN chown -R user:user /home/user/BugsInPy

USER user

RUN echo "export PATH=$PATH:/home/user/BugsInPy/framework/bin" >> /home/user/.bashrc

CMD ["/bin/bash"]
