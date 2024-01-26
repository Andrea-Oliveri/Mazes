# -*- coding: utf-8 -*-


from .a_star import AStar


class Dijkstra(AStar):
    """
    Child Solver class implementing the Dijkstra Maze solving algorithm.
    """

    def _compute_priority(self, distance, cell, end):
        return distance