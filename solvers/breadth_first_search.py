# -*- coding: utf-8 -*-


from collections import namedtuple

from .solver import Solver


# Define namedtuple used to identify a node in the tree class.
TreeNode = namedtuple('TreeNode', ['parent_node', 'cell'])


class SimpleTree:
    """
    Simple tree class using TreeNode for its node, and keeping track
    of leaves at all times in a list.
    """

    def __init__(self):
        self.leaves = []

    def add_leaf(self, cell, parent_node = None):
        leaf = TreeNode(parent_node, cell)
        self.leaves.append(leaf)

    def get_and_clear_leaves(self):
        leaves = self.leaves
        self.leaves = []
        return leaves

    @staticmethod
    def get_path(node):

        path = [node.cell]
        parent = node.parent_node
        while parent is not None:
            path.append(parent.cell)
            parent = parent.parent_node

        return path[::-1]
    
        


class BreadthFirstSearch(Solver):
    """
    Child Solver class implementing the Breadth-First-Search Maze solving algorithm.
    """

    def _grow_tree(self, tree, visited, array, end):
        for leaf in tree.get_and_clear_leaves():
            for _, neighbour in self._get_neighbours(leaf.cell):
                
                # If current leaf is a neighbour of end, early stop search.
                if neighbour == end:
                    return leaf

                if self._is_walkable_cell(array, neighbour) and neighbour not in visited:
                    tree.add_leaf(neighbour, leaf)
                    visited.add(neighbour)
                    

    def _solve_implementation(self, array, start, end):

        tree = SimpleTree()
        tree.add_leaf(start)

        visited = set([start])

        last_node = None
        while last_node is None:
            last_node = self._grow_tree(tree, visited, array, end)

        self.solution = tree.get_path(last_node)

        # Remove start from solution.
        self.solution = self.solution[1:]

        return self