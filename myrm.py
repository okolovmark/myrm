#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import click
import json
import inspect
import logging
from edit_config import read_config
from converter_to_JSON import converter_to_JSON
from config import Config
from additional_functions import message, log_config, auto_clear_trash_date
from mainlogic import create_new_trash_path, create_new_log_path, show_list_of_trash, clearing_trash,\
                      deleting_files, deleting_by_pattern, restoring_files, edit_settings


config = Config()


@click.group()
@click.option('-f', '--file_of_settings', type=str, required=False,
              help='One-time settings from JSON file, if it is specified then one_time_settings is ignored')
@click.option('-o', '--one_time_settings', is_flag=True,
              help='One-time settings, if false, then the other lower options is ignored.')
@click.option('-d', '--dry', is_flag=True, help='Imitation of program.')
@click.option('-s', '--silent', is_flag=True, help='Program operation without reports.')
@click.option('-w', '--with_confirmation', is_flag=True, help='All actions require confirmation.')
@click.option('-p', '--policy', is_flag=True, help='Select the trash cleaning policy: True=size, False=time.')
@click.option('-a', '--auto_cleaning', is_flag=True, help='Call function auto_clear_trash if memory is full.')
@click.option('-b', '--show_bar_status', is_flag=True, help='Show bar status.')
@click.option('-t', '--time', type=int, required=False,
              help='Change the time at which the trash will be cleaned(recommended: --time=10).')
@click.option('-z', '--size', type=int, required=False,
              help='Change the size(byte) at which the trash will be cleaned(recommended: --size=2000000000).')
@click.option('-l', '--level_log', type=int, required=False,
              help='Change the level of the logging or omit the parameter to disable logging.')
@click.option('-r', '--resolve_conflict', is_flag=True, help='Resolve a conflict of files.')
def main(file_of_settings, one_time_settings, dry, silent, with_confirmation, policy,
         auto_cleaning, show_bar_status, time, size, level_log, resolve_conflict):
    """Here you can specify one-time settings, if you want and call the program functions."""
    global config
    config = read_config()
    log_config(config=config)
    logging.info(inspect.stack()[0][3])
    if file_of_settings is not None:
        try:
            file_config = open(file_of_settings, 'r')
        except IOError:
            message(config, 'Could not open file')
            message(config, 'Open a normal config')
            logging.error('Could not open file')
            logging.error('Open a normal config')
        else:
            with file_config:
                try:
                    config.__dict__ = json.loads(file_config.read())
                except BaseException:
                    message(config, 'Could not read file')
                    message(config, 'Open a normal config')
                    logging.error('Could not read file')
                    logging.error('Open a normal config')
    elif one_time_settings:
        config.dry = dry
        config.silent = silent
        config.with_confirmation = with_confirmation
        config.policy = policy
        config.call_auto_cleaning_if_memory_error = auto_cleaning
        config.show_bar_status = show_bar_status
        config.resolve_conflict = resolve_conflict
        config.level_log = level_log
        if time is not None:
            config.min_day_for_start_cleaning = time
        if size is not None:
            config.max_size_for_start_cleaning = size
    if config.policy <= 0:  # if <0 than policy = time, if 0 than policy = both,
        auto_clear_trash_date(config)


@main.command()
@click.argument('path', default='.trash', type=str)
def new_trash_path(path):
    """Specify the path to the trash."""
    create_new_trash_path(config=config, path=path)


@main.command()
@click.argument('path', default='.log_myrm', type=str)
def new_log_path(path):
    """Specify the path to the log."""
    create_new_log_path(config=config, path=path)


@main.command()
@click.argument('path_txt_file', default='config.txt', type=str)
def load_txt_config(path_txt_file):
    """Loads the txt configuration file."""
    converter_to_JSON(config_JSON_file='config.json', config_txt_file=path_txt_file)


@main.command()
@click.option('-v', '--verbose', is_flag=True)
@click.argument('number', type=int, default=100, required=False)
def show_trash(verbose, number):
    """Show the contents of the basket in quantity 'number'."""
    show_list_of_trash(config=config, verbose=verbose, number=number)


@main.command()
def clear_trash():
    """Clear the contents of the trash."""
    clearing_trash(config=config)


@main.command()
@click.argument('files', nargs=-1, type=str)
def delete_files(files):
    """delete files in the trash."""
    deleting_files(config=config, files=files)


@main.command()
@click.argument('pattern', type=str)
def delete_by_pattern(pattern):
    """delete files by pattern in the trash."""
    deleting_by_pattern(config=config, pattern=pattern)


@main.command()
@click.argument('files', nargs=-1, type=str)
def restore_files(files):
    """restore files from the trash."""
    restoring_files(config=config, files=files)


@main.command()
@click.option('-d', '--dry', is_flag=True, help='Imitation of program.')
@click.option('-s', '--silent', is_flag=True, help='Program operation without reports.')
@click.option('-w', '--with_confirmation', is_flag=True, help='All actions require confirmation.')
@click.option('-p', '--policy', type=int, required=False, default=0,
              help='Select the trash cleaning policy: >0=size, <0=time, 0=both')
@click.option('-a', '--auto_cleaning', is_flag=True, help='Call function auto_clear_trash if memory is full.')
@click.option('-b', '--show_bar_status', is_flag=True, help='Show bar status.')
@click.option('-r', '--resolve_conflict', is_flag=True, help='Resolve a conflict of files.')
@click.option('-t', '--time', type=int, required=False,
              help='Change the time at which the trash will be cleaned(recommended: --time=10).')
@click.option('-z', '--size', type=int, required=False,
              help='Change the size(byte) at which the trash will be cleaned(recommended: --size=2000000000).')
@click.option('-l', '--level_log', type=int, required=False,
              help='Change the level of the logging or omit the parameter to disable logging.')
def settings(dry, silent, with_confirmation, policy, auto_cleaning, show_bar_status, resolve_conflict, time, size, level_log):
    """Editing program settings."""
    edit_settings(dry=dry, silent=silent, with_confirmation=with_confirmation, policy=policy,
                  config=config, auto_cleaning=auto_cleaning, show_bar_status=show_bar_status,
                  time=time, size=size, level_log=level_log, resolve_conflict=resolve_conflict)


if __name__ == '__main__':
    main()
