# -*- coding: utf-8 -*-
"""
Created by suun on 5/4/2018
"""

import logging


def get_logger(name, _level=logging.DEBUG,
               _format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
               _data_format="%y-%m-%d %H:%M:%S"):
    logger = logging.getLogger(name)
    logger.setLevel(_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(_level)
    formatter = logging.Formatter(fmt=_format,
                                  datefmt=_data_format)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
