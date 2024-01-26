# -*- coding: utf-8 -*-

import random
from collections import namedtuple

from .maps import Map, WallOrient
from .generator import Generator


# Define namedtuple used to identify a chamber in the maze and access its attributes without indexing. 
Chamber = namedtuple('Chamber', ['row', 'col', 'width', 'height'])



class RecursiveDivision(Generator):
    """
    Child Generator class implementing the Recursive Division Maze generation algorithm.
    This algorithm results in mazes with long straight walls crossing their space, making
    it easy to see areas to avoid entering.
    """

    def _generate_implementation(self):
        map_rows, map_cols = self.dimention
        
        self.map = Map(self.dimention, init_all_walls_up = False)

        chambers_to_divide = [Chamber(row = 0, col = 0, width = map_cols, height = map_rows)]

        while chambers_to_divide:
            current_chamber = chambers_to_divide.pop()

            # Choose direction along which chamber is divided.
            if current_chamber.width == 1 or current_chamber.height == 1:
                continue
            elif current_chamber.width == current_chamber.height:
                divide_orient = random.choice([WallOrient.H, WallOrient.V])
            elif current_chamber.width < current_chamber.height:
                divide_orient =  WallOrient.H
            else:
                divide_orient = WallOrient.V
            
            # Add random chamber wall and hole, add sub-chambers to queue.
            if divide_orient == WallOrient.H:
                chamber_wall_row = random.randrange(1, current_chamber.height)
                chamber_wall_hole_col = random.randrange(1, current_chamber.width)

                for col in range(current_chamber.width):
                    if col != chamber_wall_hole_col:
                        self.map.set_wall_idx(divide_orient,
                                              chamber_wall_row + current_chamber.row, 
                                              col + current_chamber.col,
                                              value = True)

                chambers_to_divide.append(Chamber(row = current_chamber.row, 
                                                  col = current_chamber.col,
                                                  width = current_chamber.width,
                                                  height = chamber_wall_row))
                                               
                chambers_to_divide.append(Chamber(row = current_chamber.row + chamber_wall_row, 
                                                  col = current_chamber.col,
                                                  width = current_chamber.width,
                                                  height = current_chamber.height - chamber_wall_row))

            else:
                chamber_wall_col = random.randrange(1, current_chamber.width)
                chamber_wall_hole_row = random.randrange(1, current_chamber.height)

                for row in range(current_chamber.height):
                    if row != chamber_wall_hole_row:
                        self.map.set_wall_idx(divide_orient,
                                              row + current_chamber.row, 
                                              chamber_wall_col + current_chamber.col,
                                              value = True)

                chambers_to_divide.append(Chamber(row = current_chamber.row, 
                                                  col = current_chamber.col,
                                                  width = chamber_wall_col,
                                                  height = current_chamber.height))
                                               
                chambers_to_divide.append(Chamber(row = current_chamber.row, 
                                                  col = current_chamber.col + chamber_wall_col,
                                                  width = current_chamber.width - chamber_wall_col,
                                                  height = current_chamber.height))

        return self