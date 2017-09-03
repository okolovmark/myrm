import unittest
import os
import shutil
import subprocess
from myrm.myrm import *
from myrm.converter_to_JSON import converter_to_JSON
from myrm.main_logic import show_list_of_trash, deleting_file

log_config(config=config)


class TestMYRM(unittest.TestCase):
    def setUp(self):
        subprocess.call('myrm clear_trash', shell=True)
        os.mkdir('test_dir')
        files = ['a.txt', 'b.txt', 'c.txt']
        for f in files:
            with open('test_dir/{}'.format(f), 'w'):
                pass

    def tearDown(self):
        if os.path.exists('test_dir'):
            shutil.rmtree('test_dir')

    def test_remove_files(self):
        f1 = 'test_dir/a.txt'
        f2 = 'test_dir/b.txt'
        f3 = 'test_dir/c.txt'
        subprocess.call('myrm delete_files {} {} {}'.format(f1, f2, f3), shell=True)
        self.assertFalse(os.path.exists(f1))
        self.assertFalse(os.path.exists(f2))
        self.assertFalse(os.path.exists(f3))
        # self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, 'a.txt')))
        # self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, 'b.txt')))
        # self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, 'c.txt')))

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
        f1 = 'test_dir/a.txt'
        f2 = 'test_dir/b.txt'
        f3 = 'test_dir/c.txt'
        subprocess.call('myrm delete_files {} {} {}'.format(f1, f2, f3), shell=True)
        self.assertFalse(os.path.exists(f1))
        self.assertFalse(os.path.exists(f2))
        self.assertFalse(os.path.exists(f3))
        # self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, 'a.txt')))
        # self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, 'b.txt')))
        # self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, 'c.txt')))
        f4 = 'a.txt'
        f5 = 'b.txt'
        f6 = 'c.txt'
        subprocess.call('myrm restore_files {} {} {}'.format(f4, f5, f6), shell=True)
        self.assertTrue(os.path.exists(f1))
        self.assertTrue(os.path.exists(f2))
        self.assertTrue(os.path.exists(f3))
        # self.assertFalse(os.path.exists(os.path.join(config.path_to_trash, 'a.txt')))
        # self.assertFalse(os.path.exists(os.path.join(config.path_to_trash, 'b.txt')))
        # self.assertFalse(os.path.exists(os.path.join(config.path_to_trash, 'c.txt')))

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
        subprocess.call('myrm restore_files {}'.format(f1), shell=True)
        self.assertFalse(os.path.exists(os.path.join(config.path_to_trash, 'a.txt')))

    def test_delete_by_pattern(self):
        subprocess.call('myrm delete_by_pattern "test_dir/[a-c].txt"', shell=True)
        f1 = 'test_dir/a.txt'
        f2 = 'test_dir/b.txt'
        f3 = 'test_dir/c.txt'
        self.assertFalse(os.path.exists(f1))
        self.assertFalse(os.path.exists(f2))
        self.assertFalse(os.path.exists(f3))
        # self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, 'a.txt')))
        # self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, 'b.txt')))
        # self.assertTrue(os.path.exists(os.path.join(config.path_to_trash, 'c.txt')))

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
        subprocess.call('myrm new_trash_path "{}"'.format(f1), shell=True)
        self.assertTrue(os.path.exists(f1))
        os.rmdir(f1)
        self.assertFalse(os.path.exists(f1))
        subprocess.call('myrm new_trash_path "{}"'.format(f2), shell=True)

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

    def test_fail_deleting_file(self):
        deleting_file('a.txt', config=config)
        self.assertFalse(deleting_file('a.txt', config=config) == 0)

    def test_fail_delete_trash(self):
        deleting_file('a.txt', config=config)
        self.assertFalse(deleting_file(config.path_to_trash, config=config) == 0)


if __name__ == '__main__':
    unittest.main()
