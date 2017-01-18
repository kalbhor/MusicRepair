from setuptools import setup, find_packages

setup(
    name='musicrepair',
    version='6.0.4',
    description='Lets you repair your music files by adding metadata and album art',
    url='https://github.com/lakshaykalbhor/musicrepair',
    author='Lakshay Kalbhor',
    author_email='lakshaykalbhor@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'bs4',
        'colorama',
        'mutagen',
        'spotipy',
        'six',
        'requests',
        'configparser',
    ],
    entry_points={
        'console_scripts': ['musicrepair=musicrepair.command_line:main'],
    },
    package_data={'musicrepair':['config.ini']},
)
