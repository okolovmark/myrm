#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""its contain all main functions for work with trash"""
import os
import glob
import shutil
import inspect
import datetime
import logging
import sys
import multiprocessing
from edit_config import write_config
from config import Config
from additional_functions import (Codes, log_config, message, confirmation,
                                  print_progress_bar, get_size_trash, auto_clear_trash)


def create_new_trash_path(config=Config(), path='.trash'):
    """Specify the path to the trash."""
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')
    code = Codes.GOOD

    if not confirmation(config):
        code = Codes.NOT_CONFIRMATION
        return code

    try:
        if os.path.basename(path)[0] == '.':
            hidden_trash = os.path.abspath(path)
        else:
            hidden_trash = os.path.abspath(path)[:-os.path.basename(path).__len__()] + '.' + os.path.basename(path)

        if not config.dry:
            os.makedirs(hidden_trash)
            config.path_to_trash = hidden_trash
            write_config(config)

        message(config, 'New trash path: {path}'.format(path=hidden_trash))
        logging.info('New trash path: {path}'.format(path=hidden_trash))
    except OSError:
        message(config, 'Such folder already exists')
        message(config, 'Remains the trash path: {path}'.format(path=config.path_to_trash))
        logging.error('Such folder already exists')
        logging.error('Remains the trash path: {path}'.format(path=config.path_to_trash))
        code = Codes.CONFLICT
    return code


def create_new_log_path(config=Config(), path='.log_myrm'):
    """Specify the path to the log."""
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')
    code = Codes.GOOD
    marker = '_itislogfilemyrm_'
    if not confirmation(config):
        code = Codes.NOT_CONFIRMATION
        return code

    try:
        if (os.path.basename(path)[0] == '.'
            and os.path.basename(path)[os.path.basename(path).__len__() - marker.__len__():] != marker):
            hidden_log = os.path.abspath(path) + marker
        elif (os.path.basename(path)[0] == '.'
              and os.path.basename(path)[os.path.basename(path).__len__() - marker.__len__():] == marker):
            hidden_log = os.path.abspath(path)
        elif (os.path.basename(path)[0] != '.'
              and os.path.basename(path)[os.path.basename(path).__len__() - marker.__len__():] != marker):
            hidden_log = (os.path.abspath(path)[:-os.path.basename(path).__len__()] + '.'
                          + os.path.basename(path) + marker)
        else:
            hidden_log = (os.path.abspath(path)[:-os.path.basename(path).__len__()] + '.'
                          + os.path.basename(path))

        if not config.dry:
            with open(hidden_log, 'w'):
                pass
            config.path_to_log = hidden_log
            write_config(config)

        message(config, 'New log path: {path}'.format(path=hidden_log))
        logging.info('New log path: {path}'.format(path=hidden_log))
    except IOError:
        message(config, 'incorrect path')
        message(config, 'Remains the log path: {path}'.format(path=config.path_to_log))
        logging.error('incorrect path')
        logging.error('Remains the log path: {path}'.format(path=config.path_to_log))
        code = Codes.BAD
    except OSError:
        code = Codes.BAD
    return code


def show_list_of_trash(config=Config(), verbose=False, number=100):
    """Show the contents of the basket in quantity 'number'."""
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')
    code = Codes.GOOD

    if not confirmation(config):
        code = Codes.NOT_CONFIRMATION
        return code

    if verbose:
        i = 0
        message(config, 'Objects in the basket occupy {} bytes'.format(get_size_trash(config.path_to_trash)))
        logging.info('Objects in the basket occupy {} bytes'.format(get_size_trash(config.path_to_trash)))
        for dirpath, dirs, files in os.walk(config.path_to_trash):
            for file in files:
                if os.path.basename(file)[0] == '.':
                    message(config, os.path.join(dirpath, file) + "   info_file")
                    logging.info(os.path.join(dirpath, file) + "   info_file")
                else:
                    message(config, os.path.join(dirpath, file) + "   file")
                    logging.info(os.path.join(dirpath, file) + "   file")
                i = i + 1

                if i == number:
                    break

            if i == number:
                break

            for dir in dirs:
                message(config, os.path.join(dirpath, dir) + "   dir")
                logging.info(os.path.join(dirpath, dir) + "   dir")
                i = i + 1

                if i == number:
                    break
    else:
        message(config, os.listdir(config.path_to_trash)[-number:])
        logging.info(os.listdir(config.path_to_trash)[-number:])
    return code


def clearing_trash(config=Config()):
    """Clear the contents of the trash."""
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')
    code = Codes.GOOD

    if not confirmation(config):
        code = Codes.NOT_CONFIRMATION
        return code

    try:
        if not config.dry:
            shutil.rmtree(config.path_to_trash)

        message(config, "Trash cleared")
        logging.info("Trash cleared")
    except OSError:
        message(config, "Trash already cleared")
        logging.info("Trash already cleared")
        code = Codes.BAD
    finally:
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
            os.makedirs(config.path_to_trash)
    return code


def deleting_file(file, config=Config(), iteration=0, total_files=1):
    code = Codes.GOOD
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')

    if config.show_bar_status:
        iteration += 1
        print_progress_bar(iteration, total_files, prefix='Progress:', suffix='Complete', length=50, config=config)

    if not os.path.exists(os.path.abspath(file)):
        message(config, 'The file "{}" does not exist'.format(os.path.abspath(file).encode('utf8')))
        logging.error('The file "{}" does not exist'.format(os.path.abspath(file).encode('utf8')))
        code = Codes.NO_FILE
        logging.info('return code: {}'.format(code))
        return code

    if os.path.abspath(file) == config.path_to_trash:
        message(config, 'You can not delete a trash')
        logging.error('You can not delete a trash')
        code = Codes.BAD
        logging.info('return code: {}'.format(code))
        return code

    # Name conflict solution
    path_this_file_in_trash = os.path.join(config.path_to_trash,
                                           os.path.basename(os.path.abspath(file)))
    info = ''

    if os.path.exists(path_this_file_in_trash):
        count = 1
        while True:
            if os.path.exists("{}_copy_{}".format(path_this_file_in_trash, count)):
                count += 1
            else:
                break

        path_this_file_in_trash += "_copy_{}".format(count)
        info += "_copy_{}".format(count)

    try:
        if not config.dry:
            if not os.path.exists(config.path_to_trash):
                os.makedirs(config.path_to_trash)
            os.rename(os.path.abspath(file), path_this_file_in_trash)
    except OSError:
        message(config, 'No such file or directory')
        logging.error('No such file or directory')
        code = Codes.NO_FILE
    except MemoryError:
        message(config, 'memory is full')
        logging.error('memory is full')
        code = Codes.BAD

        if config.call_auto_cleaning_if_memory_error:
            message(config, 'Auto cleaning is called')
            logging.error('Auto cleaning is called')
            auto_clear_trash(config=config)
        else:
            message(config, 'Free up memory')
            logging.error('Free up memory')
    else:
        if not config.dry:
            with open(os.path.join(config.path_to_trash,
                                   '.info_' +
                                           os.path.basename(os.path.abspath(file)) +
                                           info),
                      'w'
                      ) as info_file:
                info_file.write(os.path.abspath(file).encode('utf8'))

        message(config, 'The file {} was successfully deleted'.format(os.path.abspath(file).encode('utf8')))
        logging.info('The file {} was successfully deleted'.format(os.path.abspath(file).encode('utf8')))

    if config.policy >= 0:  # if >0 than policy = size, if 0 than policy = both
        if config.max_size_for_start_cleaning < get_size_trash(config.path_to_trash):
            auto_clear_trash(config=config)
    logging.info('return code: {}'.format(code))
    return code


def deleting_files(files, config=Config()):
    """delete files in the trash."""
    code = Codes.GOOD
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')
    iteration = 0
    total_files = len(files)

    if not confirmation(config):
        code = Codes.NOT_CONFIRMATION
        return code

    for file in files:
        p = multiprocessing.Process(target=deleting_file, args=(file, config, iteration, total_files))
        p.start()
    return code


def deleting_by_pattern(pattern, config=Config()):
    """delete files by pattern in the trash."""
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')
    code = Codes.GOOD

    if not confirmation(config):
        code = Codes.NOT_CONFIRMATION
        return code
    files = glob.glob(pattern)

    if files:
        deleting_files(files, config=config)
    else:
        message(config, 'Files not found')
        logging.error('Files not found')
        code = Codes.NO_FILE
    return code


def restoring_file(file, config=Config(), iteration=0, total_files=1):
    code = Codes.GOOD
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')

    if config.show_bar_status:
        iteration += 1
        print_progress_bar(iteration, total_files, prefix='Progress:', suffix='Complete', config=config, length=50)

    if not os.path.exists(os.path.join(config.path_to_trash, file)):
        message(config, 'The file "{}" does not exist'.format(file).encode('utf8'))
        logging.error('The file "{}" does not exist'.format(file).encode('utf8'))
        code = Codes.NO_FILE
        logging.info('return code: {}'.format(code))
        return code

    try:
        with open(os.path.join(config.path_to_trash,
                               '.info_' +
                                       os.path.basename(os.path.abspath(file))),
                  'r'
                  ) as info_file:
            old_path = info_file.readline().decode('utf8')

            if os.path.exists(old_path):
                if not config.resolve_conflict:
                    message(config, 'file "{}" already exists! rename/move/delete it'.format(file).encode('utf8'))
                    logging.error('file "{}" already exists! rename/move/delete it'.format(file).encode('utf8'))
                    code = Codes.CONFLICT
                    logging.info('return code: {}'.format(code))
                    return code
    except IOError:
        message(config, 'This file can not be restored')
        logging.error('This file can not be restored')
        code = Codes.BAD
    else:
        try:
            if not config.dry:
                os.rename(
                    os.path.abspath(os.path.join(config.path_to_trash, os.path.basename(os.path.abspath(file)))),
                    old_path)
        except OSError:
            message(config, 'Such file already exists')
            logging.error('Such file already exists')
            code = Codes.CONFLICT
        else:
            message(config, 'The file was successfully restored')
            logging.info('The file was successfully restored')
            try:
                if not config.dry:
                    os.remove(os.path.join(config.path_to_trash,
                                           '.info_' +
                                           os.path.basename(os.path.abspath(file))))
            except OSError:
                code = Codes.BAD
    logging.info('return code: {}'.format(code))
    return code


def restoring_files(files, config=Config()):
    """restore files from the trash."""
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')
    iteration = 0
    total_files = len(files)
    code = Codes.GOOD

    if not confirmation(config):
        code = Codes.NOT_CONFIRMATION
        return code

    for file in files:
        p = multiprocessing.Process(target=restoring_file, args=(file, config, iteration, total_files))
        p.start()
    return code


def edit_settings(dry=False, silent=False, with_confirmation=False, policy=0,
                  auto_cleaning=False, show_bar_status=False, time=None, size=None,
                  resolve_conflict=False, level_log=sys.maxint, config=Config()):
    """Editing program settings."""
    log_config(config=config)
    logging.info('function: ' + inspect.stack()[0][3])
    logging.info('result: ')
    code = Codes.GOOD

    if not confirmation(config):
        code = Codes.NOT_CONFIRMATION
        return code

    config.dry = dry
    config.silent = silent
    config.with_confirmation = with_confirmation
    config.policy = policy
    config.call_auto_cleaning_if_memory_error = auto_cleaning
    config.show_bar_status = show_bar_status
    config.resolve_conflict = resolve_conflict

    if level_log is sys.maxint or level_log is None:
        config.level_log = sys.maxint
        message(config, 'Logging is disabled')
        logging.info('Logging is disabled')
    else:
        config.level_log = level_log
        message(config, 'The following level of logging is set: {}'.format(level_log))
        logging.info('The following level of logging is set: {}'.format(level_log))

    if time is not None:
        config.min_day_for_start_cleaning = time
        message(config, 'The minimum number of days for auto cleaning is set to {}'.format(time))
        logging.info('The minimum number of days for auto cleaning is set to {}'.format(time))

    if size is not None:
        config.max_size_for_start_cleaning = size
        message(config, 'The maximum basket size for cleaning is set to {}'.format(size))
        logging.info('The maximum basket size for cleaning is set to {}'.format(size))

    write_config(config)

    if config.dry:
        message(config, 'Now imitation of the program is on')
        logging.info('Now imitation of the program is on')
    else:
        message(config, 'Now imitation of the program is off')
        logging.info('Now imitation of the program is off')

    if config.silent:
        message(config, 'Now program operation without reports')
        logging.info('Now program operation without reports')
    else:
        message(config, 'Now program operation with reports')
        logging.info('Now program operation with reports')

    if config.resolve_conflict:
        message(config, 'Now the program will replace files')
        logging.info('Now the program will replace files')
    else:
        message(config, 'Now the program will not replace files')
        logging.info('Now the program will not replace files')

    if config.with_confirmation:
        message(config, 'Now all actions require confirmation')
        logging.info('Now all actions require confirmation')
    else:
        message(config, 'Now all actions don\'t require confirmation')
        logging.info('Now all actions don\'t require confirmation')

    if config.policy > 0:
        message(config, 'The size policy has been activated')
        logging.info('The size policy has been activated')
    elif config.policy == 0:
        message(config, 'The time and size policy has been activated')
        logging.info('The time and size policy has been activated')
    else:
        message(config, 'The time policy has been activated')
        logging.info('The time policy has been activated')

    if config.call_auto_cleaning_if_memory_error:
        message(config, 'The auto cleaning if memory error has been activated')
        logging.info('The auto cleaning if memory error has been activated')
    else:
        message(config, 'The auto cleaning if memory error has been deactivated')
        logging.info('The auto cleaning if memory error has been deactivated')

    if config.show_bar_status:
        message(config, 'The bar status has been activated')
        logging.info('The bar status has been activated')
    else:
        message(config, 'The bar status has been deactivated')
        logging.info('The bar status has been deactivated')
    return code
