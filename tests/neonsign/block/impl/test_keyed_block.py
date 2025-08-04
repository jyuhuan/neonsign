from unittest import TestCase

from neonsign import Label
from neonsign.block.impl.keyed_block import KeyedBlock


class TestKeyedBlock(TestCase):

    def test(self):
        original = Label('hello')
        keyed = original.keyed('example-key')
        self.assertIsInstance(keyed, KeyedBlock)
        self.assertEqual(original, keyed.original)
        self.assertEqual('example-key', keyed.key)
