# -*- coding: utf-8 -*-

from .random_depth_first_search import RandomDepthFirstSearch 
from .random_kruskal import RandomKruskal
from .random_prim import RandomPrim
from .wilson import Wilson
from .aldous_broder import AldousBroder
from .recursive_division import RecursiveDivision


__generator_constructor = {'random_depth_first_search': RandomDepthFirstSearch,
                           'random_kruskal'           : RandomKruskal,
                           'random_prim'              : RandomPrim,
                           'wilson'                   : Wilson,
                           'aldous_broder'            : AldousBroder,
                           'recursive_division'       : RecursiveDivision}


GENERATOR_ALGORITHMS = list(__generator_constructor.keys())


get_generator_constructor = lambda algorithm: __generator_constructor[algorithm]
