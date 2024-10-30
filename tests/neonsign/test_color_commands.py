from unittest import TestCase

from neonsign.color_commands import (
    command_for_background, command_for_foreground
)
from neonsign.colors import Color
from neonsign.style_command import StyleCommand


class TestColorCommands(TestCase):

    def test_simple_color_commands(self):

        # Foreground colors:
        self.assertEqual(StyleCommand(30), command_for_foreground(Color.BLACK))
        self.assertEqual(StyleCommand(31), command_for_foreground(Color.RED))
        self.assertEqual(StyleCommand(32), command_for_foreground(Color.GREEN))
        self.assertEqual(StyleCommand(33), command_for_foreground(Color.YELLOW))
        self.assertEqual(StyleCommand(34), command_for_foreground(Color.BLUE))
        self.assertEqual(StyleCommand(35), command_for_foreground(Color.MAGENTA))
        self.assertEqual(StyleCommand(36), command_for_foreground(Color.CYAN))
        self.assertEqual(StyleCommand(37), command_for_foreground(Color.WHITE))
        self.assertEqual(StyleCommand(90), command_for_foreground(Color.BRIGHT_BLACK))
        self.assertEqual(StyleCommand(91), command_for_foreground(Color.BRIGHT_RED))
        self.assertEqual(StyleCommand(92), command_for_foreground(Color.BRIGHT_GREEN))
        self.assertEqual(StyleCommand(93), command_for_foreground(Color.BRIGHT_YELLOW))
        self.assertEqual(StyleCommand(94), command_for_foreground(Color.BRIGHT_BLUE))
        self.assertEqual(StyleCommand(95), command_for_foreground(Color.BRIGHT_MAGENTA))
        self.assertEqual(StyleCommand(96), command_for_foreground(Color.BRIGHT_CYAN))
        self.assertEqual(StyleCommand(97), command_for_foreground(Color.BRIGHT_WHITE))

        # Background colors:
        self.assertEqual(StyleCommand(40), command_for_background(Color.BLACK))
        self.assertEqual(StyleCommand(41), command_for_background(Color.RED))
        self.assertEqual(StyleCommand(42), command_for_background(Color.GREEN))
        self.assertEqual(StyleCommand(43), command_for_background(Color.YELLOW))
        self.assertEqual(StyleCommand(44), command_for_background(Color.BLUE))
        self.assertEqual(StyleCommand(45), command_for_background(Color.MAGENTA))
        self.assertEqual(StyleCommand(46), command_for_background(Color.CYAN))
        self.assertEqual(StyleCommand(47), command_for_background(Color.WHITE))
        self.assertEqual(StyleCommand(100), command_for_background(Color.BRIGHT_BLACK))
        self.assertEqual(StyleCommand(101), command_for_background(Color.BRIGHT_RED))
        self.assertEqual(StyleCommand(102), command_for_background(Color.BRIGHT_GREEN))
        self.assertEqual(StyleCommand(103), command_for_background(Color.BRIGHT_YELLOW))
        self.assertEqual(StyleCommand(104), command_for_background(Color.BRIGHT_BLUE))
        self.assertEqual(StyleCommand(105), command_for_background(Color.BRIGHT_MAGENTA))
        self.assertEqual(StyleCommand(106), command_for_background(Color.BRIGHT_CYAN))
        self.assertEqual(StyleCommand(107), command_for_background(Color.BRIGHT_WHITE))

    def test_8_bit_color_commands(self):
        for i in range(0, 256):
            self.assertEqual(
                StyleCommand(command=38, args=(5, i)),
                command_for_foreground(Color.color8(i))
            )
            self.assertEqual(
                StyleCommand(command=48, args=(5, i)),
                command_for_background(Color.color8(i))
            )

    def test_24_bit_color_commands(self):
        step_size = 10
        for r in range(0, 255, step_size):
            for g in range(0, 255, step_size):
                for b in range(0, 255, step_size):
                    self.assertEqual(
                        StyleCommand(command=38, args=(2, r, g, b)),
                        command_for_foreground(Color.rgb(r, g, b))
                    )
                    self.assertEqual(
                        StyleCommand(command=48, args=(2, r, g, b)),
                        command_for_background(Color.rgb(r, g, b))
                    )

    def test_unknown_color_type(self):
        class UnknownColorType(Color):
            pass
        with self.assertRaises(TypeError) as e:
            command_for_foreground(UnknownColorType())
        self.assertTrue('Unknown color type' in str(e.exception))
