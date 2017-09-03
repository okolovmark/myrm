#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""its contain class of config"""
import json
import sys


class Config(object):
    def __init__(self):
        self.dry = False
        self.silent = False
        self.with_confirmation = False
        self.path_to_trash = '.trash'
        self.path_to_log = '.log_myrm_itislogfilemyrm_'
        self.policy = False
        self.last_cleaning_date = {'year': 2017,
                                   'month': 1,
                                   'day': 1,
                                   'hour': 1,
                                   'minute': 1,
                                   'second': 1,
                                   'microsecond': 1}
        self.min_day_for_start_cleaning = 14
        self.max_size_for_start_cleaning = 2000000000
        self.call_auto_cleaning_if_memory_error = False
        self.show_bar_status = False
        self.level_log = sys.maxint
        self.resolve_conflict = False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
