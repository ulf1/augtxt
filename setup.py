from setuptools import setup
import os


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        s = fp.read()
    return s


def get_version(path):
    with open(path, "r") as fp:
        lines = fp.read()
    for line in lines.split("\n"):
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(name='augtxt',
      version=get_version("augtxt/__init__.py"),
      description='Text augmentation.',
      long_description=read('README.rst'),
      url='http://github.com/ulf1/augtxt',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['augtxt'],
      install_requires=[
          'numpy>=1.19.0,<2',
          'scipy>=1.5.4,<2',
          'kshingle>=0.6.1,<1'
      ],
      python_requires='>=3.6',
      zip_safe=True)
