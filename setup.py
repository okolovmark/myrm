from setuptools import setup
from os.path import join, dirname


setup(
    name='myrm',
    version='1.0',
    py_modules=[
        'myrm.myrm',
        'myrm.main_logic',
        'myrm.edit_config',
        'myrm.converter_to_JSON',
        'myrm.config',
        'myrm.additional_functions'],
    install_requires=[
        'Click',
        'Enum',
    ],
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_points='''
        [console_scripts]
        myrm=myrm.myrm:main
    ''',
)
