# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod
from collections import namedtuple
from enum import IntEnum
from time import time

from PIL import Image, ImageCms


# Define constants for possible cell states represented by each pixel.
CellState = IntEnum('CellState', ['WALL', 'FREE', 'START', 'END', 'SOLUTION'])

# Define namedtuple used to identify cell and access its attributes without indexing.
Cell = namedtuple('Cell', ['row', 'col'])


class Solver(ABC):
    """
    Abstract class implementing a maze solving algorithm. The input maze is read from an image,
    a suitable color is chosen to draw solution, and finally an output image with the solution
    draw on top is saved.
    """

    def __init__(self):
        self.input_image_path = None
        self.dimentions = None
        self.solution = None

    def solve(self, image_path):
        self.input_image_path = image_path

        image = Image.open(self.input_image_path).convert('RGB')

        print('Analysing image...')
        self.colors = self._analyse_image_colors(image)
        array, start, end = self._image_to_array(image, self.colors)

        print(f'Solving {image.height}x{image.width} maze with {type(self).__name__}...')
        start_time = time()
        self._solve_implementation(array, start, end)
        print(f'Solved {image.height}x{image.width} maze with {type(self).__name__} in {time()-start_time:.5f} seconds.')

        return self

    @abstractmethod
    def _solve_implementation(self, array, start, end):
        raise NotImplementedError

    def _choose_different_color(self, colors):
        # Convert colors to CIELAB colorspace.
        profile_rgb = ImageCms.createProfile("sRGB")
        profile_lab = ImageCms.createProfile("LAB")

        rgb_to_lab_transform = ImageCms.buildTransformFromOpenProfiles(profile_rgb, profile_lab, "RGB", "LAB")
    
        convert_rgb_to_lab = lambda rgb_color: ImageCms.applyTransform(Image.new("RGB", (1, 1), color = rgb_color), rgb_to_lab_transform).getpixel((0, 0))

        lab_colors = [convert_rgb_to_lab(color) for color in colors]

        # Compute CIE76 Delta E between each possible RGB color and each existing color.
        # Sum distances for each possible rgb color computed over existing colors. 
        color_distances = {}
        possible_channel_values = list(range(0, 256, 10)) + [255]
        for red in possible_channel_values:
            for green in possible_channel_values:
                for blue in possible_channel_values:
                    l, a, b = convert_rgb_to_lab((red, green, blue))

                    color_distances[(red, green, blue)] = sum(((l - l_e)**2 + (a - a_e)**2 + (b - b_e)**2)**0.5 for l_e, a_e, b_e in lab_colors)

        return max(color_distances, key = color_distances.get)

    def _analyse_image_colors(self, image):
        colors = {}

        # Any cell with both coordinates even is always a wall. 
        colors[CellState.WALL] = image.getpixel((0, 0))

        # Any cell with both coordinates odd is always free.
        colors[CellState.FREE] = image.getpixel((1, 1))

        all_colors_image = set(image.getdata())

        # If more colors than one for each of wall, free, start and end are detected, image is invalid (possibly has been compressed with loss)
        # and cell states can't be determined accurately from image pixels. 
        if len(all_colors_image) != 4:
            raise ValueError('Image is invalid: incorrect number of different colors detected. This may be due to use of a lossy image format.')

        colors[CellState.START], colors[CellState.END] =  list(all_colors_image - set(colors.values()))

        colors[CellState.SOLUTION] = self._choose_different_color(colors.values())

        return colors

    def _image_to_array(self, image, colors):
        colors_to_state_dict = {v: k for k, v in colors.items()}

        array = [[None for _ in range(image.width)] for _ in range(image.height)]
        start = None
        end = None

        for col in range(image.width):
            for row in range(image.height):
                cell_type = colors_to_state_dict[image.getpixel((col, row))]

                array[row][col] = cell_type

                if cell_type == CellState.START:
                    start = Cell(row, col)
                elif cell_type == CellState.END:
                    end = Cell(row, col)

        return array, start, end

    def _is_walkable_cell(self, array, cell):
        return array[cell.row][cell.col] != CellState.WALL

    def _get_neighbours(self, cell):
        """Returns a list of tuples of form (distance, neighbour)."""

        return [(1, Cell(cell.row + 1, cell.col)),
                (1, Cell(cell.row - 1, cell.col)), 
                (1, Cell(cell.row, cell.col + 1)),
                (1, Cell(cell.row, cell.col - 1))]

    def save_solution_as_img(self, image_path):
        
        if self.solution is None:
            raise RuntimeError("save_solution_as_img method called before generate method.")

        image = Image.open(self.input_image_path).convert('RGB')

        for row, col in self.solution:
            image.putpixel((col, row), self.colors[CellState.SOLUTION])

        image.save(image_path)