# -*- coding: utf-8 -*-
"""
Created by suun on 5/7/2018
"""
from cadre.engine import Engine
from example.pipeline import NjuPipeline
from example.spider import NjuSpider

engine = Engine(spider_class=NjuSpider, pipeline_class=NjuPipeline)
engine.execute_spider()
