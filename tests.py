import unittest
import time
import subprocess
from myrm.myrm import *
from myrm.main_logic import *
from myrm.edit_config import *
from myrm.additional_functions import *
from myrm.converter_to_JSON import converter_to_JSON
from myrm.config import Config

log_config(config=config)


class TestConsole(unittest.TestCase):

    def setUp(self):
        f2 = config.path_to_trash
        f3 = '.temp_name_trash'
        os.rename(f2, f3)
        os.mkdir(f2)
        os.mkdir('test_dir')
        files = ['a.txt', 'b.txt', 'c.txt']
        for f in files:
            with open('test_dir/{}'.format(f), 'w'):
                pass

    def tearDown(self):
        f2 = config.path_to_trash
        f3 = '.temp_name_trash'
        if os.path.exists('test_dir'):
            shutil.rmtree('test_dir')
        shutil.rmtree(f2)
        os.rename(f3, f2)

    def test_remove_files(self):
        files1 = ['test_dir/a.txt', 'test_dir/b.txt', 'test_dir/c.txt']
        files2 = ['a.txt', 'b.txt', 'c.txt']

        subprocess.call('myrm delete_files {} {} {}'.format(files1[0], files1[1], files1[2]), shell=True)

        for f in files1:
            self.assertFalse(os.path.exists(f))
        for f in files2:
            self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, f)))

    def test_remove_dir(self):
        d1 = 'test_dir'
        subprocess.call('myrm delete_files {}'.format(d1), shell=True)
        self.assertFalse(os.path.exists(d1))

    def test_remove_not_available_files(self):
        f1 = 'test_dir/a.txt'
        subprocess.call('myrm delete_files {}'.format(f1), shell=True)
        self.assertFalse(os.path.exists(f1))
        subprocess.call('myrm delete_files {}'.format(f1), shell=True)
        self.assertFalse(os.path.exists(f1))

    def test_remove_two_identical_files(self):
        f1 = 'test_dir/a.txt'
        subprocess.call('myrm delete_files {}'.format(f1), shell=True)
        self.assertFalse(os.path.exists(f1))
        with open(f1, 'w'):
            pass
        self.assertTrue(os.path.exists(f1))
        subprocess.call('myrm delete_files {}'.format(f1), shell=True)
        self.assertFalse(os.path.exists(f1))

    def test_remove_and_restore_files(self):
        f1 = ['test_dir/a.txt', 'test_dir/b.txt', 'test_dir/c.txt']
        f2 = ['a.txt', 'b.txt', 'c.txt']
        subprocess.call('myrm delete_files {} {} {}'.format(f1[0], f1[1], f1[2]), shell=True)

        for f in f1:
            self.assertFalse(os.path.exists(f))
        for f in f2:
            self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, f)))

        subprocess.call('myrm restore_files {} {} {}'.format(f2[0], f2[1], f2[2]), shell=True)

        for f in f1:
            self.assertTrue(os.path.exists(f))
        for f in f2:
            self.assertFalse(os.path.exists(os.path.join(config.path_to_trash, f)))

    def test_restore_not_available_files(self):
        f1 = 'test_dir/a.txt'
        subprocess.call('myrm delete_files {}'.format(f1), shell=True)
        self.assertFalse(os.path.exists(f1))
        f4 = 'a.txt'
        subprocess.call('myrm restore_files {}'.format(f4), shell=True)
        self.assertTrue(os.path.exists(f1))
        subprocess.call('myrm restore_files {}'.format(f4), shell=True)
        self.assertTrue(os.path.exists(f1))

    def test_restore_two_identical_files(self):
        f1 = 'test_dir/a.txt'
        subprocess.call('myrm delete_files {}'.format(f1), shell=True)
        self.assertFalse(os.path.exists(f1))
        with open(f1, 'w'):
            pass
        self.assertTrue(os.path.exists(f1))
        subprocess.call('myrm restore_files a.txt', shell=True)
        self.assertFalse(os.path.exists(os.path.join(config.path_to_trash, 'a.txt')))

    def test_delete_by_pattern(self):
        f1 = ['test_dir/a.txt', 'test_dir/b.txt', 'test_dir/c.txt']
        f2 = ['a.txt', 'b.txt', 'c.txt']
        subprocess.call('myrm delete_by_pattern "test_dir/[a-c].txt"', shell=True)

        for f in f1:
            self.assertFalse(os.path.exists(f))
        for f in f2:
            self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, f)))

    def test_delete_by_pattern_more_files(self):
        files = []
        os.mkdir('test_dir2')
        for i in range(1, 500):
            files.append(i)
        for f in files:
            with open('test_dir2/{}'.format(f), 'w'):
                pass
        subprocess.call('myrm delete_by_pattern "test_dir2/[0-9]*"', shell=True)
        self.assertTrue(os.listdir('test_dir2') == [])
        self.assertFalse(os.listdir('test_dir2') != [])
        os.rmdir('test_dir2')

    def test_clear_trash(self):
        subprocess.call('myrm clear_trash', shell=True)
        self.assertTrue(os.listdir(config.path_to_trash) == [])
        self.assertFalse(os.listdir(config.path_to_trash) != [])

    def test_new_trash_path(self):
        f1 = '.trashes'
        f2 = config.path_to_trash
        f3 = '.temp_name'
        subprocess.call('myrm new_trash_path "{}"'.format(f1), shell=True)
        self.assertTrue(os.path.exists(f1))
        shutil.rmtree(f1)
        self.assertFalse(os.path.exists(f1))
        os.rename(f2, f3)
        subprocess.call('myrm new_trash_path "{}"'.format(f2), shell=True)
        shutil.rmtree(f2)
        self.assertFalse(os.path.exists(f2))
        os.rename(f3, f2)

    def test_load_txt_config(self):
        subprocess.call('myrm load_txt_config config.txt', shell=True)
        self.assertTrue(converter_to_JSON(config_JSON_file='config.json', config_txt_file='config.txt') == 0)
        self.assertFalse(converter_to_JSON(config_JSON_file='config.json', config_txt_file='config.txt') == 1)

    def test_new_log_path(self):
        f1 = '.log_itislogfilemyrm_'
        f2 = config.path_to_log
        subprocess.call('myrm new_log_path "{}"'.format(f1), shell=True)
        self.assertTrue(os.path.exists(config.path_to_log))
        subprocess.call('myrm new_log_path "{}"'.format(f2), shell=True)
        os.remove(f1)
        self.assertFalse(os.path.exists(f1))

    def test_settings(self):
        shutil.copyfile(r'config.json', r'temp.json')
        subprocess.call('myrm settings -d', shell=True)
        subprocess.call('myrm delete_files test_dir/a.txt', shell=True)
        self.assertTrue(os.path.exists('test_dir/a.txt'))
        self.assertFalse(os.path.exists(os.path.join(config.path_to_trash, 'a.txt')))
        shutil.copyfile(r'temp.json', r'config.json')
        os.remove('temp.json')

    def test_show_trash(self):
        subprocess.call('myrm show_trash', shell=True)
        self.assertTrue(show_list_of_trash(config=config) == 0)
        self.assertFalse(show_list_of_trash(config=config) != 0)


class TestMainLogic(unittest.TestCase):

    def setUp(self):
        f2 = config.path_to_trash
        f3 = '.temp_name_trash'
        os.rename(f2, f3)
        os.mkdir(f2)
        os.mkdir('test_dir')
        files = ['a.txt', 'b.txt', 'c.txt']
        for f in files:
            with open('test_dir/{}'.format(f), 'w'):
                pass

    def tearDown(self):
        f2 = config.path_to_trash
        f3 = '.temp_name_trash'
        if os.path.exists('test_dir'):
            shutil.rmtree('test_dir')
        shutil.rmtree(f2)
        os.rename(f3, f2)

    def test_create_new_trash_path(self):
        f1 = '.trashes2'
        f2 = config.path_to_trash
        f3 = '.temp_name'
        self.assertTrue(create_new_trash_path(config=config, path=f1) == 0)
        shutil.rmtree(f1)
        os.rename(f2, f3)
        self.assertTrue(create_new_trash_path(config=config, path=f2) == 0)
        shutil.rmtree(f2)
        os.rename(f3, f2)

    def test_create_fail_new_trash_path(self):
        f1 = '.trashes2'
        os.mkdir(f1)
        self.assertFalse(create_new_trash_path(config=config, path=f1) == 0)
        os.rmdir(f1)

    def test_create_new_log_path(self):
        f1 = '.log'
        f2 = config.path_to_log
        self.assertTrue(create_new_log_path(config=config, path=f1) == 0)
        os.remove(config.path_to_log)
        self.assertTrue(create_new_log_path(config=config, path=f2) == 0)

    def test_fail_create_new_log_path(self):
        f1 = 'D:\.log\.\.\.\.\.\..,\/\\\////.,,,'
        self.assertFalse(create_new_log_path(config=config, path=f1) == 0)

    def test_show_list_of_trash(self):
        self.assertTrue(show_list_of_trash(config=config, verbose=True) == 0)

    def test_clearing_trash(self):
        self.assertTrue(clearing_trash(config) == 0)

    def test_deleting_file(self):
        f = 'test_dir/a.txt'
        self.assertTrue(deleting_file(f, config=config) == 0)

    def test_conflict_name_for_deleting_file(self):
        f = 'test_dir/a.txt'
        self.assertTrue(deleting_file(f, config=config) == 0)
        with open(f, 'w'):
            pass
        self.assertTrue(deleting_file(f, config=config) == 0)

    def test_deleting_files(self):
        f = ['test_dir/a.txt', 'test_dir/b.txt', 'test_dir/c.txt']
        self.assertTrue(deleting_files(f, config) == 0)

    def test_fail_deleting_file(self):
        self.assertFalse(deleting_file('a.txt', config=config) == 0)

    def test_fail_delete_trash(self):
        self.assertFalse(deleting_file(config.path_to_trash, config=config) == 0)

    def test_deleting_by_pattern(self):
        self.assertTrue(deleting_by_pattern('test_dir/?.txt', config) == 0)

    def test_restoring_file(self):
        deleting_file('test_dir/a.txt', config)
        self.assertTrue(restoring_file('a.txt', config) == 0)

    def test_fail_not_available_restoring_file(self):
        self.assertTrue(restoring_file('a.txt', config) == 3)

    def test_fail_incorrect_restoring_file(self):
        with open(os.path.join(config.path_to_trash, 'm.txt'), 'w'):
            pass
        self.assertTrue(restoring_file('m.txt', config) == 2)

    def test_restoring_files(self):
        f1 = ['test_dir/a.txt', 'test_dir/b.txt', 'test_dir/c.txt']
        f2 = ['a.txt', 'b.txt', 'c.txt']
        for f in f1:
            deleting_file(f, config)
        self.assertTrue(restoring_files(f2, config) == 0)
        time.sleep(1)
        for f in f1:
            self.assertTrue(os.path.exists(f))
        for f in f2:
            self.assertFalse(os.path.exists(os.path.join(config.path_to_trash, f)))

    def test_edit_settings(self):
        self.assertTrue(edit_settings(dry=True, silent=True, with_confirmation=False, policy=1,
                                      auto_cleaning=False, show_bar_status=True, time=None, size=None,
                                      resolve_conflict=False, level_log=sys.maxint, config=config) == 0)
        self.assertTrue(deleting_file('test_dir', config) == 0)
        self.assertTrue(os.path.exists('test_dir'))
        self.assertTrue(edit_settings(dry=False, silent=False, with_confirmation=False, policy=0,
                                      auto_cleaning=False, show_bar_status=False, time=None, size=None,
                                      resolve_conflict=False, level_log=sys.maxint, config=config) == 0)


class TestEditConfig(unittest.TestCase):

    def setUp(self):
        f2 = config.path_to_trash
        f3 = '.temp_name_trash'
        os.rename(f2, f3)
        os.mkdir(f2)
        os.mkdir('test_dir')
        files = ['a.txt', 'b.txt', 'c.txt']
        for f in files:
            with open('test_dir/{}'.format(f), 'w'):
                pass

    def tearDown(self):
        f2 = config.path_to_trash
        f3 = '.temp_name_trash'
        if os.path.exists('test_dir'):
            shutil.rmtree('test_dir')
        shutil.rmtree(f2)
        os.rename(f3, f2)

    def test_read_and_write_config(self):
        write_config(config, 'test/test_write_config.json')
        test_config1 = read_config(config, 'test/test_read_config.json')
        test_config2 = read_config(config, 'test/test_write_config.json')
        self.assertTrue(test_config1 is test_config2)


class TestAdditionalFunctions(unittest.TestCase):

    def setUp(self):
        f2 = config.path_to_trash
        f3 = '.temp_name_trash'
        os.rename(f2, f3)
        os.mkdir(f2)
        os.mkdir('test_dir')
        files = ['a.txt', 'b.txt', 'c.txt']
        for f in files:
            with open('test_dir/{}'.format(f), 'w'):
                pass

    def tearDown(self):
        f2 = config.path_to_trash
        f3 = '.temp_name_trash'
        if os.path.exists('test_dir'):
            shutil.rmtree('test_dir')
        shutil.rmtree(f2)
        os.rename(f3, f2)

    def test_message(self):
        test_config = Config()
        test_config.silent = False
        self.assertTrue(message(test_config, 'hello') == 0)

    def test_confirmation(self):
        config_test = Config()
        config_test.with_confirmation = True
        self.assertTrue(confirmation(config=config_test, string='yes'))
        self.assertFalse(confirmation(config=config_test, string='no'))

    def test_get_size_trash(self):
        self.assertTrue(get_size_trash('test_dir') < 4500)

    def test_auto_clear_trash(self):
        f1 = 'test_dir/a.txt'
        deleting_file(f1, config)
        self.assertTrue(auto_clear_trash(config) == 0)

if __name__ == '__main__':
    unittest.main()
