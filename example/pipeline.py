# -*- coding: utf-8 -*-
"""
Created by suun on 5/7/2018
"""
from cadre import pipeline
import codecs
import json


class NjuPipeline(pipeline.PipeLine):
    def process_item(self, item):
        fh = codecs.open("res.json", "a")
        fh.write(json.dumps(dict(item), ensure_ascii=False) + '\n')
        fh.close()
