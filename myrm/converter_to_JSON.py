#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""contain function that convert txt file to JSON file"""


def converter_to_JSON(config_txt_file, config_JSON_file):
    """converts txt file to JSON file"""
    with open(config_txt_file, 'r') as txt_config:
        content_of_file = txt_config.readlines()
        copy_of_content = content_of_file
        i = 0
        content_of_file = [x.strip() for x in content_of_file]
        with open(config_JSON_file, 'w') as json_config:
            count_space = 4
            for x in content_of_file:
                if x == ')':
                    copy_of_content[i - 1] = copy_of_content[i - 1][:copy_of_content[i - 1].__len__() - 3] + '\n'
                    count_space -= 4
                    copy_of_content[i] = count_space * ' ' + '},' + '\n'
                else:
                    line = (x.split("="))
                    if line[1] == '(':
                        copy_of_content[i] = count_space * ' ' + '"' + line[0] + '"' + ':' + ' ' + '{' + '\n'
                        count_space += 4
                    else:
                        copy_of_content[i] = count_space * ' ' + '"' + line[0] + '"' + ':' + ' ' + line[1] + ', ' + '\n'
                i += 1
            copy_of_content[i - 1] = copy_of_content[i - 1][:copy_of_content[i - 1].__len__() - 3] + '\n'
            json_config.write('{\n')
            json_config.writelines(copy_of_content)
            json_config.write('}')
