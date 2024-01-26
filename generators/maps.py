# -*- coding: utf-8 -*-

from collections import namedtuple
from enum import IntEnum


# Define namedtuple used to identify cell and access its attributes without indexing.
Cell = namedtuple('Cell', ['row', 'col'])

# Define constants for possible grid directions and wall orientations.
Direction = IntEnum('Direction', ['UP', 'DOWN', 'LEFT', 'RIGHT'])
WallOrient = IntEnum('WallOrient', ['H', 'V'], start = 0)


class Map:
    """
    Class representing the whole maze. It keeps track of state of all walls in maze and provides utilitary
    functions to change maze state, move across cells and more.
    """

    def __init__(self, dimentions, init_all_walls_up = True):
        self.map_rows, self.map_cols = dimentions

        self.num_h_walls = self.map_rows + 1
        self.num_v_walls = self.map_cols + 1

        # Indices are (orient, row, col). Border walls are always up (unremovable).
        # Walls are identified as follows:
        #
        #                wall H,r,c    
        #            ------------------
        #            |                |
        #            |                |
        # wall V,r,c |    cell r,c    | wall V,r,c+1
        #            |                |
        #            |                |
        #            ------------------
        #               wall H,r+1,c
        #
        self._walls = [[[init_all_walls_up if self.wall_is_removable(orient, row, col) else True for col in range(self.num_v_walls)] for row in range(self.num_h_walls)] for orient in WallOrient]

    def iter_cells(self):
        for row in range(self.map_rows):
            for col in range(self.map_cols):
                cell = Cell(row, col)
                wall_down  = self._walls[WallOrient.H][row+1][col]
                wall_right = self._walls[WallOrient.V][row][col+1]

                yield cell, wall_down, wall_right

    # Utilitary methods used by different generation algorithms.
    def set_wall_of_cell(self, cell, direction, value):
        if direction == Direction.UP:
            idx = (WallOrient.H, cell.row, cell.col)
        elif direction == Direction.DOWN:
            idx = (WallOrient.H, cell.row + 1, cell.col)
        elif direction == Direction.LEFT:
            idx = (WallOrient.V, cell.row, cell.col)
        elif direction == Direction.RIGHT:
            idx = (WallOrient.V, cell.row, cell.col + 1)

        self.set_wall_idx(*idx, value)

    def wall_is_removable(self, orient, row, col):
        return not ((orient == WallOrient.H and (row == 0 or row == self.map_rows)) or \
                    (orient == WallOrient.V and (col == 0 or col == self.map_cols)) or \
                    (orient == WallOrient.H and col == self.map_cols) or \
                    (orient == WallOrient.V and row == self.map_rows))

    def set_wall_idx(self, orient, row, col, value):
        if not self.wall_is_removable(orient, row, col):
            raise IndexError(f'Wall {(orient.name, row, col)} is not removable')

        self._walls[orient][row][col] = value

    def is_cell_in_map(self, cell):
        return cell.row >= 0 and cell.row < self.map_rows and cell.col >= 0 and cell.col < self.map_cols
        
    def get_list_of_removable_walls(self):
        return [(orient, row, col) for orient in WallOrient for row in range(self.num_h_walls) for col in range(self.num_v_walls) if self.wall_is_removable(orient, row, col)]

    def get_cells_around_wall(self, orient, row, col):
        if orient == WallOrient.H:
            return Cell(row-1, col), Cell(row, col)
        
        return Cell(row, col-1), Cell(row, col)

    def get_walls_around_cell(self, cell):
        walls = [(WallOrient.H, cell.row, cell.col),
                 (WallOrient.H, cell.row + 1, cell.col), 
                 (WallOrient.V, cell.row, cell.col), 
                 (WallOrient.V, cell.row, cell.col + 1)]

        return [wall for wall in walls if self.wall_is_removable(*wall)]

    def get_valid_neighbours(self, cell, prev_direction = None):
        valid_neighbours = []

        left_cell = Cell(cell.row, cell.col-1)
        if self.is_cell_in_map(left_cell) and prev_direction != Direction.RIGHT:
            valid_neighbours.append((Direction.LEFT, left_cell))
        
        right_cell = Cell(cell.row, cell.col+1)
        if self.is_cell_in_map(right_cell) and prev_direction != Direction.LEFT:
            valid_neighbours.append((Direction.RIGHT, right_cell))

        up_cell = Cell(cell.row-1, cell.col)
        if self.is_cell_in_map(up_cell) and prev_direction != Direction.DOWN:
            valid_neighbours.append((Direction.UP, up_cell))

        down_cell = Cell(cell.row+1, cell.col)
        if self.is_cell_in_map(down_cell) and prev_direction != Direction.UP:
            valid_neighbours.append((Direction.DOWN, down_cell))

        return valid_neighbours