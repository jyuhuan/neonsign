from unittest import TestCase


class TestTopLevelAPI(TestCase):

    def test(self):

        # This test verifies that the functions and classes exported by the
        # __init__.py file at the root of the library can be imported with no
        # errors.

        from neonsign import s, StyledString, Color

        green: Color = Color.GREEN
        styled_string: StyledString = (
            s('test').bold()
                     .foreground(green)
        )

        self.assertEqual('\033[32;1mtest\033[m', str(styled_string))
