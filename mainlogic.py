import click
import os
import glob
import shutil
import inspect
import datetime
import logging
from edit_config import write_config, config
from progress_bar import print_progress_bar


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, filename=config.path_to_log)


def message(*args, **kwargs):
    global config
    if not config.silent:
        click.echo(*args, **kwargs)


def confirmation():
    global config
    if config.with_confirmation:
        message('Are you sure you want to run function {}?'.format(inspect.stack()[1][3]))
        message('If not sure write no')
        logging.info('Are you sure you want to run function {}?'.format(inspect.stack()[1][3]))
        logging.info('If not sure write no')
        answer = raw_input()
        if answer.lower() == 'no':
            message('Function {} canceled'.format(inspect.stack()[1][3]))
            logging.info('Function {} canceled'.format(inspect.stack()[1][3]))
            return False
    return True


def get_size_trash(path):
    total_size = 0
    for dirpath, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def create_new_trash_path(path='.trash'):
    """Specify the path to the trash."""
    global config
    logging.info(inspect.stack()[0][3])
    if not confirmation():
        return
    try:
        if os.path.basename(path)[0] == '.':
            hidden_trash = os.path.abspath(path)
        else:
            hidden_trash = os.path.abspath(path)[:-os.path.basename(path).__len__()] + '.' + os.path.basename(path)
        if not config.dry:
            os.makedirs(hidden_trash)
            config.path_to_trash = hidden_trash
            write_config(config)
        message('New trash path: {path}'.format(path=hidden_trash))
        logging.info('New trash path: {path}'.format(path=hidden_trash))
    except OSError:
        message('Such folder already exists')
        message('Remains the trash path: {path}'.format(path=config.path_to_trash))
        logging.error('Such folder already exists')
        logging.error('Remains the trash path: {path}'.format(path=config.path_to_trash))


def create_new_log_path(path='.log_myrm'):
    """Specify the path to the log."""
    global config
    logging.info(inspect.stack()[0][3])
    if not confirmation():
        return
    try:
        if os.path.basename(path)[0] == '.':
            hidden_log = os.path.abspath(path) + '_itislogfilemyrm_'
        else:
            hidden_log = os.path.abspath(path)[:-os.path.basename(path).__len__()] + '.' \
                         + os.path.basename(path) + '_itislogfilemyrm_ '
        if not config.dry:
            with open(hidden_log, 'w'):
                pass
            config.path_to_log = hidden_log
            write_config(config)
        message('New log path: {path}'.format(path=hidden_log))
        logging.info('New log path: {path}'.format(path=hidden_log))
    except IOError:
        message('incorrect path')
        message('Remains the trash path: {path}'.format(path=config.path_to_log))
        logging.error('incorrect path')
        logging.error('Remains the trash path: {path}'.format(path=config.path_to_log))
    except OSError:
        pass


def show_list_of_trash(verbose=False, number=100):
    """Show the contents of the basket in quantity 'number'."""
    global config
    logging.info(inspect.stack()[0][3])
    if not confirmation():
        return
    if verbose:
        i = 0
        message('Objects in the basket occupy {} bytes'.format(get_size_trash(config.path_to_trash)))
        logging.info('Objects in the basket occupy {} bytes'.format(get_size_trash(config.path_to_trash)))
        for dirpath, dirs, files in os.walk(config.path_to_trash):
            for file in files:
                if os.path.basename(file)[0] == '.':
                    message(os.path.join(dirpath, file) + "   info_file")
                    logging.info(os.path.join(dirpath, file) + "   info_file")
                else:
                    message(os.path.join(dirpath, file) + "   file")
                    logging.info(os.path.join(dirpath, file) + "   file")
                i = i + 1
                if i == number:
                    break
            if i == number:
                break
            for dir in dirs:
                message(os.path.join(dirpath, dir) + "   dir")
                logging.info(os.path.join(dirpath, dir) + "   dir")
                i = i + 1
                if i == number:
                    break
    else:
        message(os.listdir(config.path_to_trash)[-number:])
        logging.info(os.listdir(config.path_to_trash)[-number:])


def clearing_trash():
    """Clear the contents of the trash."""
    global config
    logging.info(inspect.stack()[0][3])
    if not confirmation():
        return
    try:
        if not config.dry:
            shutil.rmtree(config.path_to_trash)
        message("Trash cleared")
        logging.info("Trash cleared")
    except OSError:
        message("Trash already cleared")
        logging.info("Trash already cleared")
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


def auto_clear_trash():
    """Clear automatically the contents of the trash."""
    def sort_by_count_slash(string):
        count_slash = 0
        for char in string:
            if char == '/':
                count_slash = count_slash + 1
        return count_slash
    global config
    logging.info(inspect.stack()[0][3])
    if not confirmation():
        return
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
                    print_progress_bar(iteration_files, total_files,
                                       prefix='Progress counting files:', suffix='Complete', length=50)
                list_of_files.append(os.path.abspath(os.path.join(dirpath, file)))
            for dir in dirs:
                if config.show_bar_status:
                    iteration_dirs += 1
                    print_progress_bar(iteration_dirs, total_dirs,
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
                print_progress_bar(iteration_files, total_files,
                                   prefix='Progress remove files:', suffix='Complete', length=50)
            os.remove(file)
        for dir in list_of_dirs:
            if config.show_bar_status:
                iteration_dirs += 1
                print_progress_bar(iteration_dirs, total_dirs,
                                   prefix='Progress remove dirs:', suffix='Complete', length=50)
            os.rmdir(dir)
    message('Automatic cleaning of the trash occurred')
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


def deleting_files(files):
    """delete files in the trash."""
    global config
    logging.info(inspect.stack()[0][3])
    iteration = 0
    total_files = len(files)
    if not confirmation():
        return
    for file in files:
        if config.show_bar_status:
            iteration += 1
            print_progress_bar(iteration, total_files, prefix='Progress:', suffix='Complete', length=50)
        if not os.path.exists(os.path.abspath(file)):
            message('The file "{}" does not exist'.format(os.path.abspath(file).encode('utf8')))
            logging.error('The file "{}" does not exist'.format(os.path.abspath(file).encode('utf8')))
            continue
        if os.path.abspath(file) == config.path_to_trash:
            message('You can not delete a trash')
            logging.error('You can not delete a trash')
            continue
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
            message('No such file or directory')
            logging.error('No such file or directory')
        except MemoryError:
            message('memory is full')
            logging.error('memory is full')
            if config.call_auto_cleaning_if_memory_error:
                message('Auto cleaning is called')
                logging.error('Auto cleaning is called')
                auto_clear_trash()
            else:
                message('Free up memory')
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
            message('The file {} was successfully deleted'.format(os.path.abspath(file).encode('utf8')))
            logging.error('The file {} was successfully deleted'.format(os.path.abspath(file).encode('utf8')))
        if config.policy:  # if true than policy = size
            if config.max_size_for_start_cleaning < get_size_trash(config.path_to_trash):
                auto_clear_trash()


def deleting_by_pattern(pattern):
    """delete files by pattern in the trash."""
    logging.info(inspect.stack()[0][3])
    if not confirmation():
        return
    files = glob.glob(pattern)
    if files:
        deleting_files(files)
    else:
        message('Files not found')
        logging.error('Files not found')


def restoring_files(files):
    """restore files from the trash."""
    global config
    logging.info(inspect.stack()[0][3])
    iteration = 0
    total_files = len(files)
    if not confirmation():
        return
    for file in files:
        if config.show_bar_status:
            iteration += 1
            print_progress_bar(iteration, total_files, prefix='Progress:', suffix='Complete', length=50)
        if not os.path.exists(os.path.join(config.path_to_trash, file)):
            message('The file "{}" does not exist'.format(file).encode('utf8'))
            logging.error('The file "{}" does not exist'.format(file).encode('utf8'))
            continue
        try:
            with open(os.path.join(config.path_to_trash,
                                   '.info_' +
                                   os.path.basename(os.path.abspath(file))),
                      'r'
                      ) as info_file:
                old_path = info_file.readline().decode('utf8')
                if os.path.exists(old_path):
                    message('file "{}" already exists! rename/move/delete it'.format(file).encode('utf8'))
                    logging.error('file "{}" already exists! rename/move/delete it'.format(file).encode('utf8'))
                    continue
        except IOError:
            message('This file can not be restored')
            logging.error('This file can not be restored')
        else:
            try:
                if not config.dry:
                    os.rename(
                        os.path.abspath(os.path.join(config.path_to_trash, os.path.basename(os.path.abspath(file)))),
                        old_path)
            except OSError:
                message('Such file already exists')
                logging.error('Such file already exists')
            else:
                message('The file was successfully restored')
                logging.info('The file was successfully restored')
                try:
                    if not config.dry:
                        os.remove(os.path.join(config.path_to_trash,
                                               '.info_' +
                                               os.path.basename(os.path.abspath(file))))
                except OSError:
                    pass


def edit_settings(dry=False, silent=False, with_confirmation=False, policy=False,
                  auto_cleaning=False, show_bar_status=False, time=10, size=2000000000):
    """Editing program settings."""
    global config
    logging.info(inspect.stack()[0][3])
    if not confirmation():
        return
    config.dry = dry
    config.silent = silent
    config.with_confirmation = with_confirmation
    config.policy = policy
    config.call_auto_cleaning_if_memory_error = auto_cleaning
    config.show_bar_status = show_bar_status
    if time is not None:
        config.min_day_for_start_cleaning = time
    if size is not None:
        config.max_size_for_start_cleaning = size
    write_config(config)
    if config.dry:
        message('Now imitation of the program is on')
        logging.info('Now imitation of the program is on')
    else:
        message('Now imitation of the program is off')
        logging.info('Now imitation of the program is off')
    if config.silent:
        message('Now program operation without reports')
        logging.info('Now program operation without reports')
    else:
        message('Now program operation with reports')
        logging.info('Now program operation with reports')
    if config.with_confirmation:
        message('Now all actions require confirmation')
        logging.info('Now all actions require confirmation')
    else:
        message('Now all actions don\'t require confirmation')
        logging.info('Now all actions don\'t require confirmation')
    if config.policy:
        message('The size policy has been activated')
        logging.info('The size policy has been activated')
    else:
        message('The time policy has been activated')
        logging.info('The time policy has been activated')
    if config.call_auto_cleaning_if_memory_error:
        message('The auto cleaning if memory error has been activated')
        logging.info('The auto cleaning if memory error has been activated')
    else:
        message('The auto cleaning if memory error has been deactivated')
        logging.info('The auto cleaning if memory error has been deactivated')
    if config.show_bar_status:
        message('The bar status has been activated')
        logging.info('The bar status has been activated')
    else:
        message('The bar status has been deactivated')
        logging.info('The bar status has been deactivated')
