from setuptools import setup

setup(name='musicrepair',
      version='0.2',
      description='Lets you repair your music files by adding ID3 tags and album art',
      url='https://github.com/lakshaykalbhor/musicrepair',
      author='Lakshay Kalbhor',
      author_email='lakshaykalbhor@gmail.com',
      license='MIT',
      packages =['musicrepair'],
      install_requires=[
          'bs4',
          'mutagen',
          'requests'
      ],
      entry_points={
        'console_scripts': ['musicrepair=musicrepair.command_line:main'],
      }
      )