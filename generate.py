# -*- coding: utf-8 -*-

import argparse
import random
from time import time_ns

from generators import GENERATOR_ALGORITHMS, get_generator_constructor


def _check_args(args):
    """
    Function checking validity of program parameters and applying default to unspecified arguments.
    """

    # Default values for program arguments and definition of function used to generate random weights distribution.
    default_dimention = (50, 50)
    min_side_dimention = 2
    weight_func = lambda row, col, start_row, start_col: (abs(start_row - row) + abs(start_col - col))**2

    # Check of dimention argument.
    if args.dimention is None:
        args.dimention = default_dimention
    else:
        if len(args.dimention) != len(default_dimention):
            raise ValueError("Wrong number of integers provided for dimention. Expected two integers: rows, columns.")
        
        elif any(elem < min_side_dimention for elem in args.dimention):
            raise ValueError(f"Dimention of maze must be at least {min_side_dimention}x{min_side_dimention}.")
        
    # Check of dimention argument.
    if args.start is None:
        args.start = tuple(random.randrange(elem) for elem in args.dimention)
    else:
        if len(args.start) != len(default_dimention):
            raise ValueError("Wrong number of integers provided for start. Expected two integers: row, column.")
        
        elif any(start_coord < 0 or start_coord >= dimention_coord for start_coord, dimention_coord in zip(args.start, args.dimention)):
            raise ValueError("Value of start out of maze bounds.")

    # Check of end argument.
    if args.end is None:
        n_rows, n_cols = args.dimention
        start_row, start_col = args.start

        # Randomly sample a end poisition weighting the probability by distance from start position. 
        coords  = [(row, col) for row in range(n_rows) for col in range(n_cols)]
        weights = [weight_func(row, col, start_row, start_col) for row, col in coords]
        args.end, = random.choices(coords, weights, k = 1)
    else:
        if len(args.end) != len(default_dimention):
            raise ValueError("Wrong number of integers provided for end. Expected two integers: row, column.")
        
        elif any(end_coord < 0 or end_coord >= dimention_coord for end_coord, dimention_coord in zip(args.end, args.dimention)):
            raise ValueError("Value of end out of maze bounds.")

    # Check of algorithm argument.
    if args.algorithm is None:
         args.algorithm = random.choice(GENERATOR_ALGORITHMS)
    else:
        args.algorithm, = args.algorithm

        if args.algorithm not in GENERATOR_ALGORITHMS:
            raise ValueError(f"Unknown algorithm to generate maze selected. Must be one of {', '.join(GENERATOR_ALGORITHMS)}.")

    # Check of output argument.
    if args.output is None:
        args.output = f"./maze_{time_ns()}.png"

    else:
        args.output, = args.output

    return args
    









if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Program generating a maze with desired dimentions, start and end. Generating algorithm can also be chosen.')
    parser.add_argument('--dimention', '-d', type = int, nargs = '+', default = None, required = False,
                        help = 'Number of rows and columns making up the maze.')
    parser.add_argument('--start'    , '-s', type = int, nargs = '+', default = None, required = False,
                        help = 'Row and column to use as starting point of maze.')
    parser.add_argument('--end'      , '-e', type = int, nargs = '+', default = None, required = False,
                        help = 'Row and column to use as ending point of maze.')
    parser.add_argument('--algorithm', '-a', type = str, nargs = 1  , default = None, required = False,
                        help = 'Algorithm to use to generate the maze.')
    parser.add_argument('--output'   , '-o', type = str, nargs = 1  , default = None, required = False,
                        help = 'The image in which the generated maze will be drawn.')
    
    args = parser.parse_args()
    args = _check_args(args)

    get_generator_constructor(args.algorithm)(args.dimention, args.start, args.end).generate().save_map_as_img(args.output)