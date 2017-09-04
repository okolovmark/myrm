#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""its contain functions that help edit config"""
import click
import logging
import json
from config import Config


def read_config(config, path='config.json'):
    try:
        file_config = open(path, 'r')
    except IOError:
        if not config.silent:
            click.echo('Could not open file')
            click.echo('Config is installed by default')
            logging.error('Could not open file')
            logging.error('Config is installed by default')
        config = Config()
    else:
        with file_config:
            try:
                config.__dict__ = json.loads(file_config.read())
            except BaseException:
                if not config.silent:
                    click.echo('Could not read file')
                    click.echo('Config is installed by default')
                    logging.error('Could not read file')
                    logging.error('Config is installed by default')
                config = Config()
    return config


def write_config(config, path='config.json'):
    with open(path, 'w') as file_config:
        file_config.write(config.toJSON())
