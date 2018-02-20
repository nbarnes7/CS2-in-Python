from __future__ import print_function
from sys import stdin
import unittest

'''
Description: Dijkstra's 
Author: Nick Barnes
Version: 1.0
Help received from:
Help provided to:
'''

# set to True if your result includes the path
global track_prev
track_prev = False


class weighted_digraph:

    class __edge(object):
        def __init__(self, to_node, weight):
            self.to_node = to_node
            self.weight = weight

    class __node(object):
        def __init__(self, value):
            self.value = value
            self.edges = []

        def __str__(self):
            result = str(self.value)
            for edge in self.edges:
                result += "->" + str(edge.to_node.value) + \
                          "(" + str(edge.weight) + ")"
            return (result)

        def add_edge(self, new_edge):
            if not self.is_adjacent(new_edge.to_node):
                self.edges.append(new_edge)

        def remove_edge(self, to_node):
            for edge in self.edges:
                if edge.to_node == to_node:
                    self.edges.remove(edge)

        def is_adjacent(self, node):
            for edge in self.edges:
                if edge.to_node == node:
                    return (True)
            return (False)

    def __init__(self, directed=True):
        self.__nodes = []
        self.__directed = directed

    def __len__(self):
        return (len(self.__nodes))

    def __str__(self):
        result = ""
        for node in self.__nodes:
            result += str(node) + '\n'
        return (result)

    def get_nodes(self):
        return self.__nodes[:]

    def find(self, value):
        for node in self.__nodes:
            if node.value == value:
                return (node)

        return (None)

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_node(self, value):
        if not self.find(value):
            self.__nodes.append(self.__node(value))

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge[0], edge[1], edge[2])

    """ Add an edge between two values. If the nodes
        for those values aren't already in the graph,
        add those. """

    def add_edge(self, from_value, to_value, weight):
        from_node = self.find(from_value)
        to_node = self.find(to_value)

        if not from_node:
            self.add_node(from_value)
            from_node = self.find(from_value)
        if not to_node:
            self.add_node(to_value)

            to_node = self.find(to_value)

        from_node.add_edge(self.__edge(to_node, weight))
        if not self.__directed:
            to_node.add_edge(self.__edge(from_node, weight))

    def remove_edge(self, from_value, to_value, weight):
        from_node = self.find(from_value)
        to_node = self.find(to_value)

        from_node.remove_edge(to_node)
        if not self.directed:
            to_node.remove_edge(from_node)

    def are_adjacent(self, value1, value2):
        return (self.find(value1).is_adjacent(self.find(value2)))

    def dijkstra(self, start):
        global track_prev
        result = []
        l = self.__nodes
        for node in l:
            node.distance = float("inf")
            node.previous = None
        source = self.find(start)
        source.distance = 0
        todo = [source]
        while len(todo) is not 0:
            for node in todo:
                smallest = min(todo, key=lambda node: node.distance)
                todo.remove(smallest)
                if track_prev is False:
                    result.append([smallest.distance, smallest.value])
                if track_prev is True:
                   if smallest.previous == None:
                        result.append([smallest.distance, smallest.value])
                   elif smallest.previous == start:
                        result.append([smallest.distance, smallest.value, smallest.previous.value])
                   else:
                       x = []
                       i = smallest.previous
                       while i.value is not start:
                           x.append(i.value)
                           i = i.previous
                       x.append(1)
                       temp_list = [[smallest.distance], [smallest.value], x]
                       flat_list = [item for sublist in temp_list for item in sublist]
                       result.append(flat_list)

            for edge in smallest.edges:
                temp = smallest.distance + edge.weight
                if temp < edge.to_node.distance:
                    edge.to_node.distance = temp
                    edge.to_node.previous = smallest
                    if edge.to_node not in todo:
                        todo.append(edge.to_node)

        return result

        '''
            For all the nodes in the graph, set distance
            equal to infinity and previous equal to none

            Set the source to the start, and start's distance
            to zero

            Create a todo set and add source to it

            While there is something to do
                Find the node with the minimum distance

                Remove it from the todo set
                Add it to the result

                For each of the edges in the minimum distance node
                    Calculate a possible new distance to the adjacent
                    node

                    If the new distance is less than the previous
                    distance
                        Set the distance to the newly calculated
                        distance and set the previous reference to the
                        node we just choose
                        Add the node to the todo set

            return result
        '''


class test_weighted_digraph(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(len(weighted_digraph()), 0)

    def test_one(self):
        g = weighted_digraph()
        g.add_node(1)
        self.assertEqual(len(g), 1)

    def test_duplicate(self):
        g = weighted_digraph()
        g.add_node(1)
        g.add_node(1)
        self.assertEqual(len(g), 1)

    def test_two(self):
        g = weighted_digraph()
        g.add_node(1)
        g.add_node(2)
        self.assertEqual(len(g), 2)

    def test_edge(self):
        g = weighted_digraph()
        g.add_node(1)
        g.add_node(2)
        g.add_edge(1, 2, 3)
        self.assertEqual(str(g), '1->2(3)\n2\n')

    def test_adding_ints(self):
        g = weighted_digraph()
        g.add_nodes([1, 2])
        g.add_edges([(1, 2, 3), (2, 1, 3)])
        self.assertEqual(str(g), '1->2(3)\n2->1(3)\n')

    def test_adding_strings(self):
        g = weighted_digraph()
        g.add_nodes(['Denver', 'Boston'])
        g.add_edges([('Denver', 'Boston', 1971.8), ('Boston', 'Denver', 1971.8)])
        self.assertEqual(str(g), 'Denver->Boston(1971.8)\nBoston->Denver(1971.8)\n')

    def test_are_adjacent(self):
        g = weighted_digraph()
        g.add_nodes(['Denver', 'Boston'])
        g.add_edges([('Denver', 'Boston', 1971.8), ('Boston', 'Denver', 1971.8)])
        self.assertTrue(g.are_adjacent('Denver', 'Boston'))

    def test_arent_adjacent(self):
        g = weighted_digraph()
        g.add_nodes(['Denver', 'Boston', 'Milano'])
        g.add_edges([('Denver', 'Boston', 1971.8), ('Boston', 'Denver', 1971.8)])
        self.assertFalse(g.are_adjacent('Denver', 'Milano'))

    def test_arent_adjacent_directed(self):
        g = weighted_digraph()
        g.add_edges([('Denver', 'Boston', 1971.8)])
        self.assertFalse(g.are_adjacent('Denver', 'Milano'))
        self.assertFalse(g.are_adjacent('Boston', 'Denver'))
        self.assertTrue(g.are_adjacent('Denver', 'Boston'))

    def test_arent_adjacent_undirected(self):
        g = weighted_digraph(False)
        g.add_edges([('Denver', 'Boston', 1971.8)])
        self.assertTrue(g.are_adjacent('Boston', 'Denver'))
        self.assertTrue(g.are_adjacent('Denver', 'Boston'))

    def test_add_edges_without_nodes(self):
        g = weighted_digraph()
        g.add_edges([('Denver', 'Boston', 1971.8), ('Boston', 'Denver', 1971.8)])
        self.assertEqual(str(g), \
                         'Denver->Boston(1971.8)\nBoston->Denver(1971.8)\n')

    ''' C-level work '''

    def test_dijkstra(self):
        g = weighted_digraph()
        g.add_edges([(1, 2, 2), (1, 3, 1), (2, 3, 1), (2, 4, 1), \
                     (2, 5, 2), (3, 5, 5), (4, 5, 3), (4, 6, 6), (5, 6, 1)])
        global track_prev
        track_prev = False
        self.assertEqual(g.dijkstra(1), [[0, 1], [1, 3], [2, 2], \
                                          [3, 4],[4, 5], [5, 6]])

    ''' B-level work '''

    def test_dijkstra_with_path(self):
        g = weighted_digraph()
        g.add_edges([(1, 2, 2), (1, 3, 1), (2, 3, 1), (2, 4, 1), \
                     (2, 5, 2), (3, 5, 5), (4, 5, 3), (4, 6, 6), (5, 6, 1)])
        global track_prev
        track_prev = True
        self.assertEqual(g.dijkstra(1), [[0, 1], [1, 3, 1], [2, 2, 1], \
                                           [3, 4, 2, 1], [4, 5, 2, 1], [5, 6, 5, 2, 1]])


''' A-level work '''
if '__main__' == __name__:
    with open("highway.txt") as stdin:
        g = weighted_digraph(False)
        for line in stdin:
            a = line.strip().split(" ")
            g.add_edge(a[0], a[1], int(a[2]))
        result = g.dijkstra("Denver")
        for city in result:
            print(city[1], "is", city[0], 'miles from Denver')
            if track_prev:
                for path in city[2:]:
                    print("     ", path)

