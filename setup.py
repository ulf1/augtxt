from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='augtxt',
      version='0.2.1',
      description='Text augmentation.',
      # long_description=read('README.md'),
      # long_description_content_type='text/markdown',
      url='http://github.com/ulf1/augtxt',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['augtxt'],
      install_requires=[
          'setuptools>=40.0.0',
          'numpy>=1.19.0',
          'scipy>=1.5.4',
          'fasttext>=0.9.2',
          'kshingle>=0.6.1'
      ],
      scripts=[
          'scripts/augtxt_downloader.py'
      ],
      python_requires='>=3.6',
      zip_safe=True)
