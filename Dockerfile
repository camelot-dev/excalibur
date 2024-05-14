FROM python:3.8-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y gcc libc6-dev libffi-dev libgl1-mesa-glx libglib2.0-0 ghostscript

RUN pip install .

EXPOSE 5000

RUN excalibur initdb
CMD ["excalibur", "webserver"]
