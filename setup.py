"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import os

from setuptools import setup, find_packages, Extension

# pylint: disable=redefined-builtin

here = os.path.abspath(os.path.dirname(__file__))  # pylint: disable=invalid-name

NUMENC_MODULE = Extension('numenc_module', sources=['numenc/encoder_decoder.c'])

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()  # pylint: disable=invalid-name

setup(
    name='pynumenc',
    version='1.0.0',
    description='Translates integer and flaoting-point numbers to/from sortable bytes',
    long_description=long_description,
    url='https://github.com/Parquery/pynumenc',
    author='Teodoro Filippini',
    author_email='teodoro.filippini@parquery.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    license="License :: OSI Approved :: MIT License",
    keywords='C encode decode bytes encoding decoding sorted',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['pyyaml>=3.12'],
    extras_require={'dev': ['mypy==0.560', 'hypothesis==3.74.3', 'pylint==1.8.2', 'yapf==0.20.2']},
    ext_modules=[NUMENC_MODULE],
    package_data={"pynumenc": ["py.typed"]})
