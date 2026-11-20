FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential
RUN apt-get install -y --no-install-recommends python3.12
RUN apt-get install -y --no-install-recommends python3-pip python3-venv
RUN apt-get install -y --no-install-recommends g++-15
RUN apt-get install -y --no-install-recommends openjdk-25-jdk
RUN apt-get install -y --no-install-recommends texlive-full
RUN apt-get install -y --no-install-recommends wget
RUN apt-get install -y --no-install-recommends git
RUN apt-get install -y --no-install-recommends vim

RUN wget https://downloads.python.org/pypy/pypy3.12-v8.0.1-linux64.tar.gz
RUN tar -xzvf pypy3.12-v8.0.1-linux64.tar.gz -C /opt/
RUN ln -s /opt/pypy3.12-v8.0.1-linux64/bin/pypy3 /usr/local/bin/pypy3


RUN useradd -ms /bin/bash cpyc-user
WORKDIR /home/cpyc-user

ENV VENV=/opt/venv
ENV PATH=${VENV}/bin:$PATH
RUN mkdir ${VENV}
RUN python3 -m venv ${VENV}
RUN chown -R cpyc-user ${VENV}
RUN echo source ${VENV}/bin/activate >> .bashrc

USER cpyc-user

ARG BUILDTOOLS_REPO=https://github.com/TaylorWong159/cpyc_buildtools.git
ENV BUILDTOOLS=${BUILDTOOLS_REPO}

ARG REBUILD=0
RUN pip install git+${BUILDTOOLS}