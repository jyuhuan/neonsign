import logging
from abc import ABC, abstractmethod

from neonsign.block.canvas import Canvas
from neonsign.core.size import Size


class Renderable(ABC):
    """An object that can be rendered on a two-dimensional canvas."""

    @abstractmethod
    def _render(self, granted_size: Size) -> Canvas:
        """Renders the text block using the size granted.

        When implementing this method, you should always return a canvas of
        the same size as the granted size. If not, it will be cropped or padded
        to the granted size.
        """
        pass

    def render(self, granted_size: Size) -> Canvas:
        """Renders the text block using the size granted.

        The rendered canvas will be of the same size as the granted size.
        """
        canvas: Canvas = self._render(granted_size=granted_size)
        if canvas.size != granted_size:
            logging.warning(
                f'{type(self).__name__} did not provide a render matching the '
                f'granted size. '
                f'Granted size: {granted_size} != rendered size: {canvas.size}.'
            )
            return canvas.crop_or_pad_to(granted_size)
        else:
            return canvas
