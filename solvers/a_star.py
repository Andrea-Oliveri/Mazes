# -*- coding: utf-8 -*-


from collections import defaultdict
from dataclasses import dataclass, field
from enum import IntEnum
import heapq

from .solver import Solver


# Define constants for possible priority queues usable by the A* and Dijkstra algorihthms.
PriorityQueue = IntEnum('PriorityQueue', ['ORDERED_DOUBLE_LINKED_LIST', 'BINARY_HEAP', 'BUCKET_QUEUE'])


class Node:
    """Class used to identify a node in the Double Linked List class."""

    __slots__ = 'priority', 'data', 'right', 'left'

    def __init__(self, priority, data, right = None, left = None):
        self.priority = priority
        self.data = data
        self.right = right
        self.left = left


class OrderedDoubleLinkedList:
    """
    Class implementing a priority queue using a double linked list as data structure. 
    Elements added to linked list are ordered by increasing priority from start to end. 
    No order guarantees are provided among elements of same priority. 
    """

    def __init__(self):
        self.start = None
        self.end = None
        self.len = 0

    def __bool__(self):
        return self.len > 0

    def add(self, priority, data = None):
        self.len += 1
        node = Node(priority, data)

        if self.start is None:
            self.start = self.end = node
            node.left = node.right = None

        else:

            if self.start.priority >= node.priority:
                # Add to start of linked list.
                node.right = self.start
                node.left = None
                self.start.left = node
                self.start = node

            elif self.end.priority <= node.priority:
                # Add to end of linked list.
                node.right = None
                node.left = self.end
                self.end.right = node
                self.end = node

            else:
                right = self.start.right

                while right.priority < node.priority:
                    right = right.right

                node.left = right.left
                node.right = right
                node.left.right = node
                node.right.left = node
        
    def pop_first(self):
        if self.len <= 0:
            raise IndexError('pop_first from empty double linked list.')

        self.len -= 1

        popped = self.start
        self.start = self.start.right

        if self.start is not None:
            self.start.left = None

        return popped.priority, popped.data




@dataclass(order=True)
class PrioritizedItem:
    """
    Dataclass implementing an item in a priority queue for which the
    value of the item should not play an order in determining the order,
    and instead only priority defines the order.
    """
    priority: int
    item: object=field(compare=False)



class BinaryHeap:
    """
    Class implementing a binary heap by wrapping Python's heapq module.
    """

    def __init__(self):
        self.q = []

    def add(self, priority, data = None):
        heapq.heappush(self.q, PrioritizedItem(priority, data))

    def __bool__(self):
        return len(self.q) > 0

    def pop_first(self):
        elem = heapq.heappop(self.q)
        return elem.priority, elem.item




class BucketQueue:
    """
    Class implementing a bucket queue using a dictionary.
    """
    
    def __init__(self):
        self.buckets = {}

    def add(self, priority, data = None):
        if priority in self.buckets:
            self.buckets[priority].append(data)
        else:
            self.buckets[priority] = [data]

    def __bool__(self):
        return bool(self.buckets)

    def pop_first(self):
        min_priority = min(self.buckets.keys())
        min_priority_bucket = self.buckets[min_priority]
        
        element = min_priority_bucket.pop()

        if not min_priority_bucket:
            del self.buckets[min_priority]

        return min_priority, element




class AStar(Solver):
    """
    Child Solver class implementing the A* Maze solving algorithm, using L1 distance as heuristic.
    """

    def __init__(self, priority_queue_type = PriorityQueue.ORDERED_DOUBLE_LINKED_LIST):
        super().__init__()

        priority_queue_dict = {PriorityQueue.ORDERED_DOUBLE_LINKED_LIST: OrderedDoubleLinkedList,
                               PriorityQueue.BINARY_HEAP               : BinaryHeap,
                               PriorityQueue.BUCKET_QUEUE              : BucketQueue}
        
        self.priority_queue_type = priority_queue_dict[priority_queue_type]


    def _compute_priority(self, distance, cell, end):
        # This A* implementation uses L1 distance as heuristic.
        return distance + abs(cell.row - end.row) + abs(cell.col - end.col)


    def _solve_implementation(self, array, start, end):
        distances = defaultdict(lambda: float('inf'))
        previous = defaultdict(lambda: None)
        priority_queue = self.priority_queue_type()

        distances[start] = 0
        previous[start] = None
        priority_queue.add(self._compute_priority(distances[start], start, end), (distances[start], start))

        while priority_queue:
            _, (distance, current_cell) = priority_queue.pop_first()

            if distances[current_cell] != distance:
                continue

            if current_cell == end:
                break

            for delta_distance, neighbour in self._get_neighbours(current_cell):
                if self._is_walkable_cell(array, neighbour):
                    alternative_distance = distances[current_cell] + delta_distance

                    if alternative_distance < distances[neighbour]:
                        distances[neighbour] = alternative_distance
                        previous[neighbour] = current_cell

                        neighbour_priority = self._compute_priority(alternative_distance, neighbour, end)
                        
                        priority_queue.add(neighbour_priority, (alternative_distance, neighbour))

        self.solution = []
        solution_cell = previous[end]
        while solution_cell != start:
            self.solution.append(solution_cell)
            solution_cell = previous[solution_cell]

        return self