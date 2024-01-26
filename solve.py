# -*- coding: utf-8 -*-

import argparse
import random
from os import path

from solvers import SOLVER_ALGORITHMS, get_solver_constructor


def _check_args(args):
    """
    Function checking validity of program parameters and applying default to unspecified arguments.
    """

    # Retrieve path of input maze as a string.
    args.input, = args.input

    # Check path of solved maze argument.
    if args.output is None:
        directory, filename = path.split(args.input)
        args.output = path.join(directory, 'solved_' + filename)

    else:
        args.output, = args.output

    # Check of algorithm argument.
    if args.algorithm is None:
         args.algorithm = random.choice(SOLVER_ALGORITHMS)

    else:
        args.algorithm, = args.algorithm

        if args.algorithm not in SOLVER_ALGORITHMS:
            raise ValueError(f"Unknown algorithm to solve maze selected. Must be one of {', '.join(SOLVER_ALGORITHMS)}.")

    return args
    




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Program solving a maze provided as an image.')
    parser.add_argument('--input' , '-i', type = str, nargs = 1, default = None, required = True,
                        help = 'The image containing the maze to solve.')
    parser.add_argument('--output', '-o', type = str, nargs = 1, default = None, required = False,
                        help = 'The image in which the solved maze will be drawn.')
    parser.add_argument('--algorithm', '-a', type = str, nargs = 1, default = None, required = False,
                        help = 'Algorithm to use to solve the maze.')
    
    args = parser.parse_args()
    args = _check_args(args)
    
    get_solver_constructor(args.algorithm)().solve(args.input).save_solution_as_img(args.output)