from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='txtaug',
      version='0.1.0',
      description='yet another text augmentation python package',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/ulf1/txtaug',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['txtaug'],
      install_requires=[
          'setuptools>=40.0.0'],
      python_requires='>=3.6',
      zip_safe=False)
