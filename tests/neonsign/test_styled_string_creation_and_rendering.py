from unittest import TestCase

from neonsign.colors import Color
from neonsign.styled_string import (
    BackgroundColoredString, BlinkingString, BoldString, CrossedOutString,
    DoublyUnderlinedString, ForegroundColoredString, FramedString, HiddenString,
    ItalicString, LightString, OverlinedString, PaddedString, PlainString,
    ConcatenatedString, UnderlinedString
)
from neonsign.syntax import s
from tests.neonsign.utils import validate_styled_string


class TestStyledStringCreationAndRendering(TestCase):

    def test_plain_string(self):
        validate_styled_string(
            test_case=self,
            expression=s('test'),
            expected_structure=PlainString('test'),
            expected_rendering='test',
            expected_content='test',
            expected_layout_size=4,
        )

    def test_individual_styles(self):
        validate_styled_string(
            test_case=self,
            expression=s('test').bold(),
            expected_structure=BoldString(PlainString('test')),
            expected_rendering='\033[1mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').light(),
            expected_structure=LightString(PlainString('test')),
            expected_rendering='\033[2mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').italic(),
            expected_structure=ItalicString(PlainString('test')),
            expected_rendering='\033[3mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').underlined(),
            expected_structure=UnderlinedString(PlainString('test')),
            expected_rendering='\033[4mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').blinking(),
            expected_structure=BlinkingString(PlainString('test')),
            expected_rendering='\033[5mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').hidden(),
            expected_structure=HiddenString(PlainString('test')),
            expected_rendering='\033[8mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').crossed_out(),
            expected_structure=CrossedOutString(PlainString('test')),
            expected_rendering='\033[9mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').doubly_underlined(),
            expected_structure=DoublyUnderlinedString(PlainString('test')),
            expected_rendering='\033[21mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').framed(),
            expected_structure=FramedString(PlainString('test')),
            expected_rendering='\033[51mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').overlined(),
            expected_structure=OverlinedString(PlainString('test')),
            expected_rendering='\033[53mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').foreground(Color.BLUE),
            expected_structure=ForegroundColoredString(
                Color.BLUE,
                PlainString('test')
            ),
            expected_rendering='\033[34mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').foreground(Color.rgb(10, 20, 30)),
            expected_structure=ForegroundColoredString(
                Color.rgb(10, 20, 30),
                PlainString('test')
            ),
            expected_rendering='\033[38;2;10;20;30mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').foreground(Color.color8(100)),
            expected_structure=ForegroundColoredString(
                Color.color8(100),
                PlainString('test')
            ),
            expected_rendering='\033[38;5;100mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').background(Color.BLUE),
            expected_structure=BackgroundColoredString(
                Color.BLUE,
                PlainString('test')
            ),
            expected_rendering='\033[44mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').background(Color.rgb(10, 20, 30)),
            expected_structure=BackgroundColoredString(
                Color.rgb(10, 20, 30),
                PlainString('test')
            ),
            expected_rendering='\033[48;2;10;20;30mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').background(Color.color8(100)),
            expected_structure=BackgroundColoredString(
                Color.color8(100),
                PlainString('test')
            ),
            expected_rendering='\033[48;5;100mtest\033[m',
            expected_content='test',
            expected_layout_size=4,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').padded(),
            expected_structure=PaddedString(
                PlainString('test'),
                padding_left=1,
                padding_right=1,
            ),
            expected_rendering=' test ',
            expected_content='test',
            expected_layout_size=6,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').padded(2),
            expected_structure=PaddedString(
                PlainString('test'),
                padding_left=2,
                padding_right=2,
            ),
            expected_rendering='  test  ',
            expected_content='test',
            expected_layout_size=8,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').padded_left(),
            expected_structure=PaddedString(
                PlainString('test'),
                padding_left=1,
                padding_right=0,
            ),
            expected_rendering=' test',
            expected_content='test',
            expected_layout_size=5,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').padded_left(3),
            expected_structure=PaddedString(
                PlainString('test'),
                padding_left=3,
                padding_right=0,
            ),
            expected_rendering='   test',
            expected_content='test',
            expected_layout_size=7,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').padded_right(),
            expected_structure=PaddedString(
                PlainString('test'),
                padding_left=0,
                padding_right=1,
            ),
            expected_rendering='test ',
            expected_content='test',
            expected_layout_size=5,
        )
        validate_styled_string(
            test_case=self,
            expression=s('test').padded_right(4),
            expected_structure=PaddedString(
                PlainString('test'),
                padding_left=0,
                padding_right=4,
            ),
            expected_rendering='test    ',
            expected_content='test',
            expected_layout_size=8,
        )

    def test_style_chaining(self):
        validate_styled_string(
            test_case=self,
            expression=(
                s('test')
                .padded()
                .italic()
                .foreground(Color.rgb(10, 20, 30))
                .bold()
            ),
            expected_structure=(
                BoldString(
                    ForegroundColoredString(
                        Color.rgb(red=10, green=20, blue=30),
                        ItalicString(
                            PaddedString(
                                PlainString('test'),
                                padding_left=1,
                                padding_right=1
                            )
                        )
                    )
                )
            ),
            expected_rendering=(
                '\033[1;38;2;10;20;30;3m \033[m'
                '\033[1;38;2;10;20;30;3mtest\033[m'
                '\033[1;38;2;10;20;30;3m \033[m'
            ),
            expected_content='test',
            expected_layout_size=6,
        )

    def test_applying_style_to_concatenated_string(self):
        validate_styled_string(
            test_case=self,
            expression=(
                s(
                    s('test0').bold(),
                    s('test1'),
                    s('test2').italic(),
                    'test3'
                ).underlined()
            ),
            expected_structure=(
                UnderlinedString(
                    ConcatenatedString(
                        (
                            BoldString(
                                PlainString('test0')
                            ),
                            PlainString('test1'),
                            ItalicString(
                                PlainString('test2')
                            ),
                            PlainString('test3')
                        )
                    )
                )
            ),
            # Expectation:
            #  - 'test0' should have bold (1) and underline (4).
            #  - 'test1' should have underline (4) only.
            #  - 'test2' should have both italic (3) and underline (4).
            expected_rendering=(
                '\033[4;1mtest0\033[m'
                '\033[4mtest1\033[m'
                '\033[4;3mtest2\033[m'
                '\033[4mtest3\033[m'
            ),
            expected_content='test0test1test2test3',
            expected_layout_size=20,
        )

    def test_complex_composition(self):
        validate_styled_string(
            test_case=self,
            expression=(
                s(
                    s('test0'),
                    s(
                        s('test1.0').padded_right(),
                        s('test1.1').foreground(Color.GREEN),
                        s('test1.2').padded_left()
                                    .bold()
                                    .foreground(Color.BLUE),
                        'test1.3'
                    ).background(Color.YELLOW),
                    s('test2').italic()
                ).underlined()
            ),
            expected_structure=(
                UnderlinedString(
                    ConcatenatedString(
                        (
                            PlainString('test0'),
                            BackgroundColoredString(
                                Color.YELLOW,
                                ConcatenatedString(
                                    (
                                        PaddedString(
                                            PlainString('test1.0'),
                                            padding_left=0,
                                            padding_right=1
                                        ),
                                        ForegroundColoredString(
                                            Color.GREEN,
                                            PlainString('test1.1')
                                        ),
                                        ForegroundColoredString(
                                            Color.BLUE,
                                            BoldString(
                                                PaddedString(
                                                    PlainString('test1.2'),
                                                    padding_left=1,
                                                    padding_right=0,
                                                )
                                            ),
                                        ),
                                        PlainString('test1.3')
                                    )
                                )
                            ),
                            ItalicString(
                                PlainString('test2')
                            )
                        )
                    )
                )
            ),
            expected_rendering=(
                '\033[4mtest0\033[m'
                '\033[4;43mtest1.0\033[m'
                '\033[4;43m \033[m'
                '\033[4;43;32mtest1.1\033[m'
                '\033[4;43;34;1m \033[m'
                '\033[4;43;34;1mtest1.2\033[m'
                '\033[4;43mtest1.3\033[m'
                '\033[4;3mtest2\033[m'
            ),
            expected_content='test0test1.0test1.1test1.2test1.3test2',
            expected_layout_size=40,
        )
