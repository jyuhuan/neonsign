from typing import Callable
from unittest import TestCase

from neonsign.colors import Color, Color24, Color8, SimpleColor


class TestColors(TestCase):

    def test_uniqueness_of_simple_colors(self):
        simple_colors = [
            getattr(Color, var_name)
            for var_name in dir(Color)
            if isinstance(getattr(Color, var_name), SimpleColor)
        ]
        self.assertEqual(16, len(simple_colors))
        self.assertEqual(
            len(simple_colors),
            len(set(c.name for c in simple_colors))
        )

    def test_24_bit_colors_rgb_initializer(self):
        color_instance: Color = Color.rgb(1, 2, 3)
        self.assertIsInstance(color_instance, Color24)
        self.assertEqual(1, color_instance.red)
        self.assertEqual(2, color_instance.green)
        self.assertEqual(3, color_instance.blue)

    def test_24_bit_colors_hex_string_initializer(self):
        color_instance: Color = Color.hex('#70A7C2')
        self.assertIsInstance(color_instance, Color24)
        self.assertEqual(112, color_instance.red)
        self.assertEqual(167, color_instance.green)
        self.assertEqual(194, color_instance.blue)

        # 3-character hex code should be expanded correctly:
        self.assertEqual(Color.hex('#8899AA'), Color.hex('#89A'))

    def test_24_bit_colors_hsl_initializer(self):
        color_instance: Color = Color.hsl(200, 40, 60)
        self.assertIsInstance(color_instance, Color24)
        self.assertEqual(112, color_instance.red)
        self.assertEqual(167, color_instance.green)
        self.assertEqual(194, color_instance.blue)

    def test_24_bit_colors_hsv_initializer(self):
        color_instance: Color = Color.hsv(200, 40, 60)
        self.assertIsInstance(color_instance, Color24)
        self.assertEqual(92, color_instance.red)
        self.assertEqual(133, color_instance.green)
        self.assertEqual(153, color_instance.blue)

    def test_8_bit_colors(self):
        color_instance: Color = Color.color8(1)
        self.assertIsInstance(color_instance, Color8)
        self.assertEqual(1, color_instance.index)

    def test_simple_color_validation(self):
        with self.assertRaises(ValueError) as e:
            SimpleColor('rainbow')
        self.assertEqual(
            'Cannot create color with name "rainbow"!',
            str(e.exception)
        )

    def test_8_bit_color_validation(self):
        # Valid cases:
        Color8(index=0)
        Color8(index=255)

        # Invalid cases:
        with self.assertRaises(ValueError) as e:
            Color8(index=-1)
        self.assertEqual(
            'Index for an 8-bit color must be within 0 and 255, not -1!',
            str(e.exception)
        )
        with self.assertRaises(ValueError) as e:
            Color8(index=256)
        self.assertEqual(
            'Index for an 8-bit color must be within 0 and 255, not 256!',
            str(e.exception)
        )

    def test_24_bit_color_validation_in_rgb_initializer(self):

        # Valid cases:

        Color24(red=0, green=0, blue=255)
        Color24(red=0, green=255, blue=0)
        Color24(red=255, green=0, blue=0)

        # Invalid cases:

        def check(
                f: Callable[[], Color24],
                expected_error_summary: str
        ):
            with self.assertRaises(ValueError) as e:
                f()
            self.assertEqual(
                f'Value of a 24-bit color component must be between 0 and 255, '
                f'but the following are found to be outside of these bounds: '
                f'{expected_error_summary}!',
                str(e.exception)
            )

        self._check(
            lambda: Color24(0, 0, -1),
            ' - blue = -1 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(0, -1, 0),
            ' - green = -1 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(0, -1, -1),
            ' - blue = -1 (required to be within (0, 255))',
            ' - green = -1 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(-1, 0, 0),
            ' - red = -1 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(-1, 0, -1),
            ' - blue = -1 (required to be within (0, 255))',
            ' - red = -1 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(-1, -1, 0),
            ' - green = -1 (required to be within (0, 255))',
            ' - red = -1 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(-1, -1, -1),
            ' - blue = -1 (required to be within (0, 255))',
            ' - green = -1 (required to be within (0, 255))',
            ' - red = -1 (required to be within (0, 255))'
        )

        self._check(
            lambda: Color24(0, 0, 256),
            ' - blue = 256 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(0, 256, 0),
            ' - green = 256 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(0, 256, 256),
            ' - blue = 256 (required to be within (0, 255))',
            ' - green = 256 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(256, 0, 0),
            ' - red = 256 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(256, 0, 256),
            ' - blue = 256 (required to be within (0, 255))',
            ' - red = 256 (required to be within (0, 255))'
        )
        self._check(
            lambda: Color24(256, 256, 0),
            ' - green = 256 (required to be within (0, 255))',
            ' - red = 256 (required to be within (0, 255))'

        )
        self._check(
            lambda: Color24(256, 256, 256),
            ' - blue = 256 (required to be within (0, 255))',
            ' - green = 256 (required to be within (0, 255))',
            ' - red = 256 (required to be within (0, 255))'
        )

    def test_24_bit_color_validation_in_hex_initializer(self):

        with self.assertRaises(ValueError) as e:
            Color24.from_hex('')
        self.assertEqual(
            "A color in hexadecimal format should start with the # sign, "
            "but '' does not!",
            str(e.exception)
        )

        with self.assertRaises(ValueError) as e:
            Color24.from_hex('#')
        self.assertEqual(
            "A hex code for 24-bit color must be 3-character or "
            "6-character long, excluding the # sign at the beginning, "
            "but '' is 0-character long!",
            str(e.exception)
        )

        with self.assertRaises(ValueError) as e:
            Color24.from_hex('#1A')
        self.assertEqual(
            "A hex code for 24-bit color must be 3-character or "
            "6-character long, excluding the # sign at the beginning, "
            "but '1A' is 2-character long!",
            str(e.exception)
        )

        with self.assertRaises(ValueError) as e:
            Color24.from_hex('1A2B3C')
        self.assertEqual(
            "A color in hexadecimal format should start with the # sign, "
            "but '1A2B3C' does not!",
            str(e.exception)
        )

    def test_24_bit_color_validation_in_hsl_initializer(self):
        self._check(
            lambda: Color24.from_hsl(0, 0, -1),
            ' - lightness = -1 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsl(0, -1, 0),
            ' - saturation = -1 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsl(0, -1, -1),
            ' - lightness = -1 (required to be within (0, 100))',
            ' - saturation = -1 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsl(-1, 0, 0),
            ' - hue = -1 (required to be within (0, 360))'
        )
        self._check(
            lambda: Color24.from_hsl(-1, 0, -1),
            ' - hue = -1 (required to be within (0, 360))',
            ' - lightness = -1 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsl(-1, -1, 0),
            ' - hue = -1 (required to be within (0, 360))',
            ' - saturation = -1 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsl(-1, -1, -1),
            ' - hue = -1 (required to be within (0, 360))',
            ' - lightness = -1 (required to be within (0, 100))',
            ' - saturation = -1 (required to be within (0, 100))'
        )

        self._check(
            lambda: Color24.from_hsl(0, 0, 101),
            ' - lightness = 101 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsl(0, 101, 0),
            ' - saturation = 101 (required to be within (0, 100))',
        )
        self._check(
            lambda: Color24.from_hsl(0, 101, 101),
            ' - lightness = 101 (required to be within (0, 100))',
            ' - saturation = 101 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsl(361, 0, 0),
            ' - hue = 361 (required to be within (0, 360))'
        )
        self._check(
            lambda: Color24.from_hsl(361, 0, 101),
            ' - hue = 361 (required to be within (0, 360))',
            ' - lightness = 101 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsl(361, 101, 0),
            ' - hue = 361 (required to be within (0, 360))',
            ' - saturation = 101 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsl(361, 101, 101),
            ' - hue = 361 (required to be within (0, 360))',
            ' - lightness = 101 (required to be within (0, 100))',
            ' - saturation = 101 (required to be within (0, 100))'
        )

    def test_24_bit_color_validation_in_hsv_initializer(self):
        self._check(
            lambda: Color24.from_hsv(0, 0, -1),
            ' - value = -1 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsv(0, -1, 0),
            ' - saturation = -1 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsv(0, -1, -1),
            ' - saturation = -1 (required to be within (0, 100))',
            ' - value = -1 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsv(-1, 0, 0),
            ' - hue = -1 (required to be within (0, 360))'
        )
        self._check(
            lambda: Color24.from_hsv(-1, 0, -1),
            ' - hue = -1 (required to be within (0, 360))',
            ' - value = -1 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsv(-1, -1, 0),
            ' - hue = -1 (required to be within (0, 360))',
            ' - saturation = -1 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsv(-1, -1, -1),
            ' - hue = -1 (required to be within (0, 360))',
            ' - saturation = -1 (required to be within (0, 100))',
            ' - value = -1 (required to be within (0, 100))'
        )

        self._check(
            lambda: Color24.from_hsv(0, 0, 101),
            ' - value = 101 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsv(0, 101, 0),
            ' - saturation = 101 (required to be within (0, 100))',
        )
        self._check(
            lambda: Color24.from_hsv(0, 101, 101),
            ' - saturation = 101 (required to be within (0, 100))',
            ' - value = 101 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsv(361, 0, 0),
            ' - hue = 361 (required to be within (0, 360))'
        )
        self._check(
            lambda: Color24.from_hsv(361, 0, 101),
            ' - hue = 361 (required to be within (0, 360))',
            ' - value = 101 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsv(361, 101, 0),
            ' - hue = 361 (required to be within (0, 360))',
            ' - saturation = 101 (required to be within (0, 100))'
        )
        self._check(
            lambda: Color24.from_hsv(361, 101, 101),
            ' - hue = 361 (required to be within (0, 360))',
            ' - saturation = 101 (required to be within (0, 100))',
            ' - value = 101 (required to be within (0, 100))'
        )

    def _check(
            self,
            f: Callable[[], Color24],
            *expected_error_messages: str
    ):
        with self.assertRaises(ValueError) as e:
            f()

        all_messages = '\n'.join(expected_error_messages)
        self.assertEqual(
            f'The following values are out of their required ranges:\n'
            f'{all_messages}',
            str(e.exception)
        )
