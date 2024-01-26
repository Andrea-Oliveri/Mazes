# -*- coding: utf-8 -*-

import random

from .maps import Map, Cell
from .generator import Generator



class DisjointSet:
    """
    Utilitary class implementing the Disjoint Set data structure.
    """

    def __init__(self, nodes = [], parents = None):
        self.nodes = nodes
        self.parents = parents if parents is not None else {elem: elem for elem in self.nodes}

    def add_node(self, node, parent = None):
        """
        Adds a new node to the disjoint set, putting it into a set of its own.
        If node already exists in the disjoint set, no operation is performed.
        """
        if node not in self.nodes:
            self.nodes.append(node)
            self.parents[node] = parent if parent is None else node

    def find(self, item):
        """
        Implementation of find algorithm for disjoint sets with no recursion and using path halving.
        """

        parent = self.parents[item]

        while parent != item:
            grandparent = self.parents[parent]
            self.parents[item] = grandparent
            item = parent
            parent = grandparent
            
        return item

    def union(self, node1, node2):
        """
        Merges the two sets contained the nodes passed as parameter into a single set.
        Returns true if the two nodes were already in the same set, else False.
        """

        root1 = self.find(node1)
        root2 = self.find(node2)
        self.parents[root1] = root2

        # Return true if node1 and node2 belonged to the same set already. 
        return root1 == root2




class RandomKruskal(Generator):
    """
    Child Generator class implementing the Randomized Kruskal Maze generation algorithm.
    This algorithm is biased towards generating mazes with many short dead ends.
    """

    def _generate_implementation(self):
        
        map_rows, map_cols = self.dimention
        
        self.map = Map(self.dimention, init_all_walls_up = True)

        walls = self.map.get_list_of_removable_walls()
        random.shuffle(walls)
                
        cells_sets = DisjointSet([Cell(row, col) for row in range(map_rows) for col in range(map_cols)])

        for wall in walls:
            cells = self.map.get_cells_around_wall(*wall) 

            if not cells_sets.union(*cells):
                self.map.set_wall_idx(*wall, value = False)
        
        return self