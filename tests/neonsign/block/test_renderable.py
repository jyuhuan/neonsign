from unittest import TestCase
from unittest.mock import patch

from neonsign.block.canvas import Canvas
from neonsign.block.renderable import Renderable
from neonsign.core.size import Size


class TestRenderable(TestCase):

    @patch('neonsign.block.renderable.logging')
    def test_inconsistency_between_granted_size_and_render_size(
            self,
            logging_mock
    ):
        size = Size(width=2, height=3)

        class ConsistentRenderable(Renderable):
            def _render(self, granted_size: Size) -> Canvas:
                return Canvas.of(granted_size)
        self.assertEqual(
            size,
            ConsistentRenderable().render(granted_size=size).size
        )

        class InconsistentRenderable(Renderable):
            def _render(self, granted_size: Size) -> Canvas:
                return Canvas.of(size=granted_size.increased_by(width_delta=1))
        self.assertEqual(
            size,
            InconsistentRenderable().render(granted_size=size).size
        )
        logging_mock.warning.assert_called_once_with(
            'InconsistentRenderable did not provide a render matching the '
            'granted size. Granted size: 2x3 != rendered size: 3x3.'
        )
