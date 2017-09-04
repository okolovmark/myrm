#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""It contains functions that simplify the code."""
import click
import os
import inspect
import logging
import datetime
from edit_config import write_config
from config import Config
from enum import Enum


class Codes(Enum):
    GOOD = 0
    CONFLICT = 1
    BAD = 2
    NO_FILE = 3
    NOT_CONFIRMATION = 4


def log_config(config=Config()):
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                        level=config.level_log, filename=config.path_to_log)


def message(config=Config(), *args, **kwargs):
    code = Codes.GOOD
    try:
        if not config.silent:
            click.echo(*args, **kwargs)
    except:
        code = Codes.BAD
        return code
    else:
        return code


def input_string(string=None):  # for auto input for tests
    if string is None:
        return raw_input()
    else:
        return string


def confirmation(config=Config(), string=None):
    """function requesting confirmation for an operation"""
    log_config(config=config)
    if config.with_confirmation:
        message(config, 'Are you sure you want to run function {}?'.format(inspect.stack()[1][3]))
        message(config, 'If not sure write no')
        logging.info('Are you sure you want to run function {}?'.format(inspect.stack()[1][3]))
        logging.info('If not sure write no')
        answer = input_string(string=string)
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


def check_date_for_auto_clear_trash(config):
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


def auto_clear_trash(config=Config()):
    """Clear automatically the contents of the trash."""

    def sort_by_count_slash(string):
        count_slash = 0
        for char in string:
            if char == '/':
                count_slash = count_slash + 1
        return count_slash

    code = Codes.GOOD
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')

    if not confirmation(config):
        code = Codes.NOT_CONFIRMATION
        return code

    if not config.dry:
        list_of_files = []
        list_of_dirs = []

        for dirpath, dirs, files in os.walk(config.path_to_trash):
            iteration_files = 0
            iteration_dirs = 0
            total_files = len(files)
            total_dirs = len(dirs)

            for file in files:
                if config.show_bar_status:
                    iteration_files += 1
                    print_progress_bar(iteration_files, total_files, config=config,
                                       prefix='Progress counting files:', suffix='Complete', length=50)
                list_of_files.append(os.path.abspath(os.path.join(dirpath, file)))
            for dir in dirs:
                if config.show_bar_status:
                    iteration_dirs += 1
                    print_progress_bar(iteration_dirs, total_dirs,  config=config,
                                       prefix='Progress counting dirs:', suffix='Complete', length=50)
                list_of_dirs.append(os.path.abspath(os.path.join(dirpath, dir)))

        list_of_dirs.sort(key=sort_by_count_slash, reverse=True)
        iteration_files = 0
        iteration_dirs = 0
        total_files = len(list_of_files)
        total_dirs = len(list_of_dirs)

        for file in list_of_files:
            if config.show_bar_status:
                iteration_files += 1
                print_progress_bar(iteration_files, total_files, config=config,
                                   prefix='Progress remove files:', suffix='Complete', length=50)
            os.remove(file)

        for dir in list_of_dirs:
            if config.show_bar_status:
                iteration_dirs += 1
                print_progress_bar(iteration_dirs, total_dirs, config=config,
                                   prefix='Progress remove dirs:', suffix='Complete', length=50)
            os.rmdir(dir)

    message(config, 'Automatic cleaning of the trash occurred')
    logging.info('Automatic cleaning of the trash occurred')

    if not config.dry:
        last_cleaning_date = datetime.datetime.now()
        config.last_cleaning_date['year'] = last_cleaning_date.year
        config.last_cleaning_date['month'] = last_cleaning_date.month
        config.last_cleaning_date['day'] = last_cleaning_date.day
        config.last_cleaning_date['hour'] = last_cleaning_date.hour
        config.last_cleaning_date['minute'] = last_cleaning_date.minute
        config.last_cleaning_date['second'] = last_cleaning_date.second
        config.last_cleaning_date['microsecond'] = last_cleaning_date.microsecond
        write_config(config)
    return code
