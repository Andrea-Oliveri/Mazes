# -*- coding: utf-8 -*-

from .a_star import AStar, PriorityQueue
from .dijkstra import Dijkstra
from .breadth_first_search import BreadthFirstSearch


__solver_constructor = {'a_star'               : AStar,
                        'a_star_linked_list'   : lambda: AStar(PriorityQueue.ORDERED_DOUBLE_LINKED_LIST),
                        'a_star_binary_heap'   : lambda: AStar(PriorityQueue.BINARY_HEAP),
                        'a_star_bucket_queue'  : lambda: AStar(PriorityQueue.BUCKET_QUEUE),
                        'dijkstra'             : Dijkstra,
                        'dijkstra_linked_list' : lambda: Dijkstra(PriorityQueue.ORDERED_DOUBLE_LINKED_LIST),
                        'dijkstra_binary_heap' : lambda: Dijkstra(PriorityQueue.BINARY_HEAP),
                        'dijkstra_bucket_queue': lambda: Dijkstra(PriorityQueue.BUCKET_QUEUE),
                        'breadth_first_search' : BreadthFirstSearch}


SOLVER_ALGORITHMS = list(__solver_constructor.keys())


get_solver_constructor = lambda algorithm: __solver_constructor[algorithm]