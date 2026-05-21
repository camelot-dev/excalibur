FROM ubuntu

RUN apt-get update

RUN apt-get install -y \
    apt-utils \
    curl \
    wget \
    libsm6 \
    libxrender1 \
    libxext6 \
    nano \
    ghostscript \
    python3-minimal \
    python3-setuptools \
    python3-pip \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip

EXPOSE 5000

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /excalibur/
COPY . ./

RUN pip3 install .

RUN excalibur initdb

RUN cat /root/excalibur/excalibur.cfg | sed 's/127.0.0.1/0.0.0.0/g' > /root/excalibur/excalibur.cfg2; \
    mv /root/excalibur/excalibur.cfg2 /root/excalibur/excalibur.cfg
