Pynumenc
========

Pynumenc is a Python3 library to translate numbers to and from sortable bytes.

This library was born to avoid the slowness and awkwardness of dealing with bytes directly in Python.

The library contains conversion functions from/to the following types:

=========   ========  ====  =====  ==================================  =====================================
Specifier   Signing   Bits  Bytes  Minimum Value                       Maximum Value
=========   ========  ====  =====  ==================================  =====================================
int8        Signed    8     1      -2^7 (-128)                         2^7 - 1  (127)
uint8       Unsigned  8     1      0                                   2^8 - 1  (255)
int16       Signed    16    2      -2^15 (-32,768)                      2^15 - 1 (32,767)
uint16      Unsigned  16    2      0                                   2^16 - 1 (65,535)
int32       Signed    32    4      -2^31 (-2,147,483,648)              2^31 - 1 (2,147,483,647)
uint32      Unsigned  32    4      0                                   2^32 - 1 (4,294,967,295)
int64       Signed    64    8      -2^63 (-9,223,372,036,854,775,808)  2^63 - 1 (9,223,372,036,854,775,807)
uint64      Unsigned  64    8      0                                   2^64 - 1 (18,446,744,073,709,551,615)
float32     Signed    32    8      -3.402823466385288598117041834e+38  3.4028234663852885981170418348451e+38
float64     Signed    64    8      -1.79769313486231570814527423e+308  1.797693134862315708145274237317e+308
=========   ========  ====  =====  ==================================  =====================================

The encoding and decoding computations are written in C to maximize their speed. Furthermore, unlike the default bit
representation of integers and floats, the above functions use clever bit-manipulation techniques to guarantee that not
only mappings are injective, but that the resulting bytes preserve the order of the numbers, that is:
  * encoding(a) < encoding(b) <=> a < b
  * encoding(a) = encoding(b) <=> a = b

The rules above imply that we do not follow IEEE-754's standard of treating negative zero as smaller than positive
zero: we treat them as the same number.

Installation
============

* Create a virtual environment:

.. code-block:: bash

    python3 -m venv venv3

* Activate it:

.. code-block:: bash

    source venv3/bin/activate

* Install pynumenc with pip:

.. code-block:: bash

    pip3 install pynumenc

Usage
=====
To use the encoding and decoding functions, you need to invoke one of the ``numenc_module.from_TYPE()`` and
``numenc_module.to_TYPE()`` functions, replacing TYPE with any one of the types listed above. For example:

.. code-block:: python

    import numenc_module

    encoded = numenc_module.from_int32(1200) # encoded = b'\x80\x00\x04\xb0'

    decoded = numenc_module.to_int32(b'\x80\x00\x00\x00') # decoded = 0


Development
===========

* Check out the repository.

* In the repository root, create the virtual environment:

.. code-block:: bash

    python3 -m venv venv3

* Activate the virtual environment:

.. code-block:: bash

    source venv3/bin/activate

* Install the development dependencies:

.. code-block:: bash

    pip3 install -e .[dev]

* Run `precommit.py` to execute pre-commit checks locally.

Versioning
==========
We follow `Semantic Versioning <http://semver.org/spec/v1.0.0.html>`_. The version X.Y.Z indicates:

* X is the major version (backward-incompatible),
* Y is the minor version (backward-compatible), and
* Z is the patch version (backward-compatible bug fix).