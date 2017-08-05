from setuptools import setup


setup(
    name='lab2',
    version='1.0',
    py_modules=['myrm'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        myrm=myrm:main
    ''',
)
