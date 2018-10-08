#!/usr/bin/env python3
# pylint: disable=missing-docstring
import unittest

import hypothesis
import hypothesis.strategies

import numenc_module

MIN_SIGNED_INT16 = -32768
MAX_SIGNED_INT16 = 32767
MAX_UNSIGNED_INT16 = 65535


class TestEncodingInt16(unittest.TestCase):
    @hypothesis.given(hypothesis.strategies.integers(min_value=MIN_SIGNED_INT16, max_value=MAX_SIGNED_INT16))
    def test_encode_decode_automatic(self, value: int):
        hypothesis.assume(value)
        self.assertEqual(value, numenc_module.to_int16(numenc_module.from_int16(value)))

    @hypothesis.given(
        value1=hypothesis.strategies.integers(min_value=MIN_SIGNED_INT16, max_value=MAX_SIGNED_INT16),
        value2=hypothesis.strategies.integers(min_value=MIN_SIGNED_INT16, max_value=MAX_SIGNED_INT16))
    def test_encode_order(self, value1: int, value2: int):
        encoded1 = numenc_module.from_int16(value1)
        encoded2 = numenc_module.from_int16(value2)
        if value1 < value2:
            self.assertLess(encoded1, encoded2)
        elif value1 == value2:
            self.assertEqual(encoded1, encoded2)
        else:
            self.assertGreater(encoded1, encoded2)

    def test_encode_decode(self):
        #yapf: disable
        nums = [
            MIN_SIGNED_INT16,
            -3332,
            0,
            2289,
            MAX_SIGNED_INT16
        ]

        expected = [
            b'\x00\x00',
            b'\x72\xfc',
            b'\x80\x00',
            b'\x88\xf1',
            b'\xff\xff'
        ]
        #yapf: enable

        for i, num in enumerate(nums):
            key = numenc_module.from_int16(num)
            self.assertEqual(expected[i], key)

            num_decoded = numenc_module.to_int16(key)
            self.assertEqual(num, num_decoded)

        for i, _ in enumerate(expected):
            if i > 0:
                self.assertLess(expected[i - 1], expected[i])

    def test_encode_exceptions(self):
        tajp_err_triggers = [
            "some string", 2.344, ('1', '2'), [], {}, b'\x01\x02', MIN_SIGNED_INT16 - 1, MAX_SIGNED_INT16 + 1
        ]

        for weird_val in tajp_err_triggers:
            tajp_err = False
            try:
                _ = numenc_module.from_int16(weird_val)
            except TypeError:
                tajp_err = True

            self.assertTrue(tajp_err, msg="excepted error thrown for input {!r}, but got no error.".format(weird_val))

    def test_decode_exceptions(self):
        tajp_err_triggers = ["some string", 2.344, ('1', '2'), [], {}, 232, -1.23]
        val_err_triggers = [b'\x01', b'', b'\x01\x02\x02\x02']

        for weird_val in tajp_err_triggers:
            tajp_err = False
            try:
                _ = numenc_module.to_int16(weird_val)
            except TypeError:
                tajp_err = True

            self.assertTrue(tajp_err, msg="excepted error thrown for input {!r}, but got no error.".format(weird_val))

        for weird_val in val_err_triggers:
            val_err = False
            try:
                _ = numenc_module.to_int16(weird_val)
            except ValueError:
                val_err = True

            self.assertTrue(val_err, msg="excepted error thrown for input {!r}, but got no error.".format(weird_val))


class TestEncodingUInt16(unittest.TestCase):
    @hypothesis.given(hypothesis.strategies.integers(min_value=0, max_value=MAX_UNSIGNED_INT16))
    def test_encode_decode_automatic(self, value: int):
        hypothesis.assume(value)
        self.assertEqual(value, numenc_module.to_uint16(numenc_module.from_uint16(value)))

    @hypothesis.given(
        value1=hypothesis.strategies.integers(min_value=0, max_value=MAX_UNSIGNED_INT16),
        value2=hypothesis.strategies.integers(min_value=0, max_value=MAX_UNSIGNED_INT16))
    def test_encode_order(self, value1: int, value2: int):
        encoded1 = numenc_module.from_uint16(value1)
        encoded2 = numenc_module.from_uint16(value2)
        if value1 < value2:
            self.assertLess(encoded1, encoded2)
        elif value1 == value2:
            self.assertEqual(encoded1, encoded2)
        else:
            self.assertGreater(encoded1, encoded2)

    def test_encode_decode(self):
        #yapf: disable
        nums = [
            0,
            29436,
            32768,
            35057,
            MAX_UNSIGNED_INT16
        ]

        expected = [
            b'\x00\x00',
            b'\x72\xfc',
            b'\x80\x00',
            b'\x88\xf1',
            b'\xff\xff'
        ]
        #yapf: enable

        for i, num in enumerate(nums):
            key = numenc_module.from_uint16(num)
            self.assertEqual(expected[i], key)

            num_decoded = numenc_module.to_uint16(key)
            self.assertEqual(num, num_decoded)

        for i, _ in enumerate(expected):
            if i > 0:
                self.assertLess(expected[i - 1], expected[i])

    def test_encode_exceptions(self):
        tajp_err_triggers = ["some string", 2.344, ('1', '2'), [], {}, b'\x01\x02']
        val_err_triggers = [-2222222, -1, MAX_UNSIGNED_INT16 + 1]

        for weird_val in tajp_err_triggers:
            tajp_err = False
            try:
                _ = numenc_module.from_uint16(weird_val)
            except TypeError:
                tajp_err = True

            self.assertTrue(tajp_err, msg="excepted error thrown for input {!r}, but got no error.".format(weird_val))

        for weird_val in val_err_triggers:
            val_err = False
            try:
                _ = numenc_module.from_uint16(weird_val)
            except ValueError:
                val_err = True

            self.assertTrue(val_err, msg="excepted error thrown for input {!r}, but got no error.".format(weird_val))

    def test_decode_exceptions(self):
        tajp_err_triggers = ["some string", ('1', '2'), [], {}, 232, -1.23]
        val_err_triggers = [b'\x01', b'', b'\x01\x02\x02\x02']

        for weird_val in tajp_err_triggers:
            tajp_err = False
            try:
                _ = numenc_module.to_uint16(weird_val)
            except TypeError:
                tajp_err = True

            self.assertTrue(tajp_err, msg="excepted error thrown for input {!r}, but got no error.".format(weird_val))

        for weird_val in val_err_triggers:
            val_err = False
            try:
                _ = numenc_module.to_uint16(weird_val)
            except ValueError:
                val_err = True

            self.assertTrue(val_err, msg="excepted error thrown for input {!r}, but got no error.".format(weird_val))


if __name__ == '__main__':
    unittest.main()
