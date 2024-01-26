# -*- coding: utf-8 -*-

import random

from .maps import Map, Cell, Direction
from .generator import Generator



class ListSetHybrid:
    """
    Utilitary class implementing a data structure containing reference to its elements
    both inside a list and a set. This allow for list-like ordered storage of elements
    and O(1) check of elements inside list. 
    """

    def __init__(self, elements = []):
        self._list = list(elements)
        self._set  = set(self._list)

    def __contains__(self, elem):
        return elem in self._set

    def __getitem__(self, idx):
        return self._list[idx]

    def append(self, elem):
        self._list.append(elem)
        self._set.add(elem)

    def pop(self):
        last_elem = self._list.pop()
        self._set.remove(last_elem)
        return last_elem

    def get_set(self):
        return self._set



class Wilson(Generator):
    """
    Child Generator class implementing the Wilson Maze generation algorithm.
    This algorithm samples in an unbiased way a random maze from the uniform
    distribution over all mazes. However, on large maze sizes, the generation
    time may be extremely long, as it implements a loop-erasing random walk.
    """

    def _generate_implementation(self):

        inverse_direction = {Direction.UP: Direction.DOWN,
                             Direction.DOWN: Direction.UP,
                             Direction.RIGHT: Direction.LEFT,
                             Direction.LEFT: Direction.RIGHT}

        map_rows, map_cols = self.dimention
        
        self.map = Map(self.dimention, init_all_walls_up = True)

        unvisited_cells = set(Cell(row, col) for row in range(map_rows) for col in range(map_cols))

        # Initialize maze with one cell chosen randomly.
        unvisited_cells.remove(Cell(random.randrange(map_rows), random.randrange(map_cols)))

        while unvisited_cells:
            current_cell, = random.sample(unvisited_cells, k=1)
            walk_cells = ListSetHybrid([current_cell])
            walk_directions = []

            direction, next_cell = random.choice(self.map.get_valid_neighbours(current_cell))
            while current_cell in unvisited_cells:
                neighbours_next_cell = self.map.get_valid_neighbours(next_cell, direction)

                # Check if loop was made.
                loop_made = False
                for _, neighbour in neighbours_next_cell:
                    if neighbour in walk_cells:
                        loop_made = True

                        # Undo changes to map.
                        prev_last_cell = None
                        last_cell = walk_cells.pop()
                        while last_cell != neighbour:
                            last_direction = walk_directions.pop()

                            opposite_last_direction = inverse_direction[last_direction]
                            self.map.set_wall_of_cell(last_cell, opposite_last_direction, value = True)

                            prev_last_cell = last_cell
                            last_cell = walk_cells.pop()
                            
                        # Put variables back in correct state.
                        current_cell = last_cell
                        walk_cells.append(last_cell)
                        next_cell = prev_last_cell
                        direction = last_direction

                # If no loop found, proceed as normal.
                if not loop_made:
                    self.map.set_wall_of_cell(current_cell, direction, value = False)
                    
                    walk_cells.append(next_cell)
                    walk_directions.append(direction)
                    current_cell = next_cell
                    direction, next_cell = random.choice(neighbours_next_cell)

            unvisited_cells -= walk_cells.get_set()


        return self