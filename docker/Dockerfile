FROM ubuntu

RUN apt-get update \
    && apt-get install -y \
    apt-utils \
    curl \
    wget \
    nano \
    libsm6 \
    libxrender1 \
    libxext6 \
    ghostscript \
    python3-minimal \
    python3-setuptools \
    python3-pip \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip install excalibur-py[dev]

EXPOSE 5000

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /excalibur/
