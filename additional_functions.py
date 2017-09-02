#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import click
import os
import inspect
import logging
import datetime
from mainlogic import auto_clear_trash
from config import Config


def log_config(config=Config()):
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                        level=config.level_log, filename=config.path_to_log)


def message(config=Config(), *args, **kwargs):
    if not config.silent:
        click.echo(*args, **kwargs)


def confirmation(config=Config()):
    log_config(config=config)
    if config.with_confirmation:
        message(config, 'Are you sure you want to run function {}?'.format(inspect.stack()[1][3]))
        message(config, 'If not sure write no')
        logging.info('Are you sure you want to run function {}?'.format(inspect.stack()[1][3]))
        logging.info('If not sure write no')
        answer = raw_input()
        if answer.lower() == 'no':
            message(config, 'Function {} canceled'.format(inspect.stack()[1][3]))
            logging.info('Function {} canceled'.format(inspect.stack()[1][3]))
            return False
    return True


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', config=Config()):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    message(config, '\r  %s |%s| %s%% %s' % (prefix, bar, percent, suffix) + '\r', nl=False)
    if not config.silent:
        if iteration == total:
            print


def get_size_trash(path):
    total_size = 0
    for dirpath, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def auto_clear_trash_date(config):
    last_cleaning_date = datetime.datetime(config.last_cleaning_date['year'],
                                           config.last_cleaning_date['month'],
                                           config.last_cleaning_date['day'],
                                           config.last_cleaning_date['hour'],
                                           config.last_cleaning_date['minute'],
                                           config.last_cleaning_date['second'],
                                           config.last_cleaning_date['microsecond'])
    min_date_for_start_cleaning = datetime.timedelta(config.min_day_for_start_cleaning)
    if datetime.datetime.now() - last_cleaning_date > min_date_for_start_cleaning:
        auto_clear_trash(config=config)
