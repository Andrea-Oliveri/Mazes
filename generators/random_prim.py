# -*- coding: utf-8 -*-

import random

from .maps import Map, Cell
from .generator import Generator



class RandomPrim(Generator):
    """
    Child Generator class implementing the Randomized Prim (edge-based) Maze generation algorithm.
    This algorithm is biased towards generating mazes with many short dead ends.
    """

    def _generate_implementation(self):
        map_rows, map_cols = self.dimention
        
        self.map = Map(self.dimention, init_all_walls_up = True)

        # Initialize array of booleans to determine if each cell was already visited. 
        visited = [[False for _ in range(map_cols)] for _ in range(map_rows)]

        random_cell = Cell(row = random.randrange(map_rows), col = random.randrange(map_cols))
        visited[random_cell.row][random_cell.col] = True
        walls_list = list(self.map.get_walls_around_cell(random_cell))

        while walls_list:
            random_wall_idx = random.randrange(len(walls_list))
            random_wall = walls_list[random_wall_idx]

            cell1, cell2 = self.map.get_cells_around_wall(*random_wall)

            if visited[cell1.row][cell1.col] and not visited[cell2.row][cell2.col]:
                self.map.set_wall_idx(*random_wall, value = False)
                visited[cell2.row][cell2.col] = True
                walls_list.extend(self.map.get_walls_around_cell(cell2))

            elif not visited[cell1.row][cell1.col] and visited[cell2.row][cell2.col]:
                self.map.set_wall_idx(*random_wall, value = False)
                visited[cell1.row][cell1.col] = True
                walls_list.extend(self.map.get_walls_around_cell(cell1))

            # Removes element from unordered list fast.
            walls_list[random_wall_idx], walls_list[-1] = walls_list[-1], walls_list[random_wall_idx]
            walls_list.pop()

        return self

