from unittest import TestCase

from neonsign.string.styled_string import (
    ConcatenatedString, PlainString,
    StyledString
)
from neonsign.string.styled_string_factory import (
    construct_multiple,
    construct_single
)


class TestStyledStringFactory(TestCase):

    def test_constructing_from_single_item(self):
        # Case 1: From a plain Python str:
        result_1: StyledString = construct_single('test')
        self.assertIsInstance(result_1, PlainString)

        # Case 2: From another StyledString:
        result_2: StyledString = construct_single(result_1)
        self.assertIsInstance(result_2, PlainString)
        self.assertEqual(result_1, result_2)

        # Case 3: From an unsupported type:
        with self.assertRaises(TypeError) as e:
            construct_single(1.0)
        self.assertEqual(
            "Contents passed to s() must be either a str or a StyledString, "
            "but 1.0 is a <class 'float'>!",
            str(e.exception)
        )

    def test_constructing_from_multiple_items(self):
        # Case 1.1: From a single str object:
        result_1_1: StyledString = construct_multiple('test')
        self.assertIsInstance(result_1_1, PlainString)

        # Case 1.2: From a single StyledString object:
        result_1_2: StyledString = construct_single(result_1_1)
        self.assertIsInstance(result_1_2, PlainString)
        self.assertEqual(result_1_1, result_1_2)

        # Case 2.1: From multiple str objects:
        result_2_1: StyledString = construct_multiple('test1', 'test2')
        self.assertIsInstance(result_2_1, ConcatenatedString)
        self.assertEqual(2, len(result_2_1.substrings))
        self.assertIsInstance(result_2_1.substrings[0], PlainString)
        self.assertIsInstance(result_2_1.substrings[1], PlainString)

        # Case 2.2: From multiple StyledString objects:
        result_2_2: StyledString = construct_multiple(result_1_1, result_2_1)
        self.assertIsInstance(result_2_2, ConcatenatedString)
        self.assertEqual(2, len(result_2_2.substrings))
        self.assertIsInstance(result_2_2.substrings[0], PlainString)
        self.assertIsInstance(result_2_2.substrings[1], ConcatenatedString)

        # Case 2.3: From multiple str and StyledString objects:
        result_2_3: StyledString = construct_multiple('test', result_2_1)
        self.assertIsInstance(result_2_3, ConcatenatedString)
        self.assertEqual(2, len(result_2_3.substrings))
        self.assertIsInstance(result_2_3.substrings[0], PlainString)
        self.assertIsInstance(result_2_3.substrings[1], ConcatenatedString)

        # Case 2.4: From multiple objects, one of which is of unsupported type:
        with self.assertRaises(TypeError) as e:
            construct_multiple('test', result_2_1, 1.0)
        self.assertEqual(
            "Contents passed to s() must be either a str or a StyledString, "
            "but 1.0 is a <class 'float'>!",
            str(e.exception)
        )
