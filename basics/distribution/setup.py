# https://docs.python.org/3.6/distutils/introduction.html#distutils-simple-example

from distutils.core import setup
setup(name='foo',
      version='1.0',
      py_modules=['foo']
      )