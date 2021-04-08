from setuptools import setup
import pypandoc


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
      long_description=pypandoc.convert('README.md', 'rst'),
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
