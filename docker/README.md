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

### Prepare the image

Switch to `docker` directory here and run `docker build -t excalibur .` (don't forget the final `.`) to build your docker image. That may take some time but is only required once. Or perhaps a few times after you tweak something in a `Dockerfile`.

After the process is finished you have a `excalibur` image, that will be the base for your experiments. You can confirm that looking on results of `docker images` command.

### Run the container

From your project folder, run `docker run -it -p 5000:5000 -v $(pwd):/excalibur/ excalibur /bin/bash`
This will start the container and open up a bash console inside it.

At this point you need to initialize the metadata database using:

<pre>
$ excalibur initdb
</pre>

Once initialized, you need to enable connectivity from outside the container:

Use nano to open the config file ...

<pre>
$ nano /root/excalibur/excalibur.cfg
</pre>

... and modify the [webserver] section as:

<pre>
web_server_host = 0.0.0.0
</pre>

And then start the webserver using:

<pre>
$ excalibur webserver
</pre>

That's it! Now you can go to http://localhost:5000 and start extracting tabular data from your PDFs.
