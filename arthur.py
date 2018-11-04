# -*- coding: utf-8 -*-

import multiprocessing

from excalibur.cli import webserver, initdb


if __name__ == '__main__':
    multiprocessing.freeze_support()
    initdb()
    webserver()
