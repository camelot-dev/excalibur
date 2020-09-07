import multiprocessing

from excalibur.cli import webserver

if __name__ == "__main__":
    multiprocessing.freeze_support()
    webserver()
