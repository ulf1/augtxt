from setuptools import setup
import m2r


setup(name='augtxt',
      version='0.2.0',
      description='Text augmentation.',
      long_description=m2r.parse_from_file('README.md'),
      long_description_content_type='text/x-rst',
      url='http://github.com/ulf1/augtxt',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['augtxt'],
      install_requires=[
          'setuptools>=40.0.0',
          'm2r>=0.2.1',
          'numpy>=1.19.0',
          'scipy>=1.5.4',
          'fasttext>=0.9.2',
          'kshingle>=0.6.0'
      ],
      scripts=[
          'scripts/nlptasks_downloader.py'
      ],
      python_requires='>=3.6',
      zip_safe=True)
