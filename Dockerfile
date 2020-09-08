FROM ubuntu:bionic
WORKDIR /home/root
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y git libsm6 libxext6 libxrender1 libfontconfig1 python3 python3-pip python-pip python3-tk ghostscript &&  gs -version
COPY . ./excalibur
#&& perl -pi -e 's/from werkzeug import secure_filename/from werkzeug.utils import secure_filename/' excalibur/www/views.py \
RUN cd excalibur \
  && ls -lah \
  && pip3 install . \
  && cd ../
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
EXPOSE 5000
ENTRYPOINT [ "python3", "./excalibur/arthur.py" ]