# -*- coding: utf-8 -*-

import random

from .maps import Map, Cell, Direction
from .generator import Generator


class RandomDepthFirstSearch(Generator):
    """
    Child Generator class implementing the Random Depth First Search Maze generation algorithm.
    This algorithm is biased towards generating mazes with long corridors.
    """

    def _generate_implementation(self):

        map_rows, map_cols = self.dimention
        directions_deltas = {Direction.UP   : (-1, 0),
                             Direction.DOWN : (+1, 0),
                             Direction.LEFT : (0, -1),
                             Direction.RIGHT: (0, +1)}

        self.map = Map(self.dimention, init_all_walls_up = True)

        stack = [Cell(row = random.randrange(map_rows), col = random.randrange(map_cols))]

        # Initialize array of booleans to determine if each cell was already visited. 
        visited = [[False for _ in range(map_cols)] for _ in range(map_rows)]

        while stack:
            current_cell = stack.pop()
            
            # Get valid, unvisited neighbours.
            neighbours = {}
            for direction, (delta_row, delta_col) in directions_deltas.items():
                neighbour_cell = Cell(current_cell.row + delta_row, current_cell.col + delta_col)

                if self.map.is_cell_in_map(neighbour_cell) and not visited[neighbour_cell.row][neighbour_cell.col]:
                    neighbours[direction] = neighbour_cell

            if neighbours:
                stack.append(current_cell)

                rand_neighbour_direction = random.choice(list(neighbours))
                rand_neighbour = neighbours[rand_neighbour_direction]

                self.map.set_wall_of_cell(current_cell, rand_neighbour_direction, value = False)

                visited[rand_neighbour.row][rand_neighbour.col] = True
                stack.append(rand_neighbour)

        return self