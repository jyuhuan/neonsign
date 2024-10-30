from unittest import TestCase

from neonsign.style_command import StyleCommand


class TestStyleCommand(TestCase):

    def test(self):

        command_without_args = StyleCommand(command=30)
        command_with_args = StyleCommand(command=38, args=(2, 10, 20, 30))

        self.assertEqual((), command_without_args.args)

        self.assertEqual((30,), command_without_args.terminal_code)
        self.assertEqual(
            (38, 2, 10, 20, 30),
            command_with_args.terminal_code
        )
