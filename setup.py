"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import os

from setuptools import setup, find_packages, Extension

import pynumenc_meta

# pylint: disable=redefined-builtin

here = os.path.abspath(os.path.dirname(__file__))  # pylint: disable=invalid-name

NUMENC = Extension('numenc', sources=['numenc-cpp/encoder_decoder.cpp'])

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()  # pylint: disable=invalid-name

setup(
    name=pynumenc_meta.__title__,
    version=pynumenc_meta.__version__,
    description=pynumenc_meta.__description__,
    long_description=long_description,
    url=pynumenc_meta.__url__,
    author=pynumenc_meta.__author__,
    author_email=pynumenc_meta.__author_email__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    license='License :: OSI Approved :: MIT License',
    keywords='C encode decode bytes encoding decoding sorted',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[],
    extras_require={
        'dev':
        ['mypy==0.560', 'hypothesis==3.74.3', 'pylint==1.8.2', 'yapf==0.20.2']
    },
    ext_modules=[NUMENC],
    py_modules=['pynumenc', 'pynumenc_meta'],
    package_data={
        'pynumenc': ['py.typed'],
        '': ['LICENSE.txt', 'README.rst'],
    })
