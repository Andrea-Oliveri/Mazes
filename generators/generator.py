# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from enum import IntEnum
from time import time

from PIL import Image

from .maps import Cell


# Define constants for possible cell states represented by each pixel, as well as the color in output image 
# for each pixel type.
PixelState = IntEnum('PixelState', ['WALL', 'FREE', 'START', 'END'], start = 0)
COLORS_DICT = ((0, 0, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0))


class Generator(ABC):
    """
    Abstract class implementing a maze generating algorithm, and saving it into an output image where each
    pixel is a cell.
    """

    def __init__(self, dimention, start, end):
        self.dimention = dimention
        self.start = Cell(*start)
        self.end = Cell(*end)
        self.map = None

    def generate(self):
        rows, cols = self.dimention

        print(f'Generating {rows}x{cols} maze with {type(self).__name__}...')
        start_time = time()
        self._generate_implementation()
        print(f'Generated {rows}x{cols} maze with {type(self).__name__} in {time()-start_time:.5f} seconds.')

        return self

    @abstractmethod
    def _generate_implementation(self):
        raise NotImplementedError

    def save_map_as_img(self, image_path):

        if self.map is None:
            raise RuntimeError("save_map_as_img method called before generate method.")

        image_rows, image_cols = tuple(2*coord+1 for coord in self.dimention)

        image = Image.new(mode = 'RGB', size = (image_cols, image_rows), color = COLORS_DICT[ PixelState.WALL ])

        for cell, wall_down, wall_right in self.map.iter_cells():
            top_left_px_row = 2 * cell.row + 1
            top_left_px_col = 2 * cell.col + 1

            image.putpixel( (top_left_px_col, top_left_px_row), COLORS_DICT[ PixelState.FREE ] )

            if not wall_down:
                image.putpixel( (top_left_px_col, top_left_px_row + 1), COLORS_DICT[ PixelState.FREE ] )

            if not wall_right:
                image.putpixel( (top_left_px_col + 1, top_left_px_row), COLORS_DICT[ PixelState.FREE ] )

        image.putpixel((2*self.start.col+1, 2*self.start.row+1), COLORS_DICT[ PixelState.START ] )
        image.putpixel((2*self.end.col  +1, 2*self.end.row  +1), COLORS_DICT[ PixelState.END   ] )

        image.save(image_path)