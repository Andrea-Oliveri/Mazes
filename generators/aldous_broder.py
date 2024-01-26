# -*- coding: utf-8 -*-

import random

from .maps import Map, Cell
from .generator import Generator



class AldousBroder(Generator):
    """
    Child Generator class implementing the Aldous-Broder Maze generation algorithm.
    This algorithm samples in an unbiased way a random maze from the uniform
    distribution over all mazes. However, on large maze sizes, the generation
    time may be extremely long.
    """

    def _generate_implementation(self):
        map_rows, map_cols = self.dimention
        
        self.map = Map(self.dimention, init_all_walls_up = True)

        unvisited_cells = set(Cell(row, col) for row in range(map_rows) for col in range(map_cols))

        current_cell = Cell(row = random.randrange(map_rows), col = random.randrange(map_cols))
        unvisited_cells.remove(current_cell)

        while unvisited_cells:
            direction, neighbour = random.choice(self.map.get_valid_neighbours(current_cell))
            if neighbour in unvisited_cells:
                self.map.set_wall_of_cell(current_cell, direction, value = False)
                unvisited_cells.remove(neighbour)
            current_cell = neighbour

        return self

