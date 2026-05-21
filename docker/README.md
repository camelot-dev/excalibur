<p align="center">
   <img src="https://raw.githubusercontent.com/camelot-dev/excalibur/master/docs/_static/excalibur-logo.png" width="200">
</p>

# Excalibur: Docker
This is the Docker configuration which allows you to run Excalibur without installing any dependencies on your machine!<br/>
OK, any except `docker`.

## Prerequisites

As stated, the thing you need is `docker`.

Follow the instructions on [Install Docker](https://docs.docker.com/engine/installation/) for your environment if you haven't got `docker` already.

## Usage

### With compose

Switch to `docker` directory and run `docker-compose up --build`

Open your browser to http://localhost and start extracting tabular data from your PDFs.

### Running the container youself

### Prepare the image

Switch to `docker` directory and run `docker build -t excalibur ./excalibur` to build your docker image. That may take some time but is only required once. Or perhaps a few times after you tweak something in a `Dockerfile`.

After the process is finished you have a `excalibur` image, that will be the base for your experiments. You can confirm that looking on results of `docker images` command.

### Run the container

From your project folder, run `docker run -it -p 5000:5000 excalibur`

That's it! Now you can go to http://localhost:5000 and start extracting tabular data from your PDFs.
