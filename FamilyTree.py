from __future__ import print_function
from sys import stdin
import unittest

'''
Description: Family Tree
Author: Nick Barnes
Version: 1.0
Help received from: 
Help provided to:
'''

class FamilyTree(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.left = self.right = None
        self.parent = parent

    def __iter__(self):
        if self.left:
            for node in self.left:
                yield node

        yield self.name

        if self.right:
            for node in self.right:
                yield node

    def __str__(self):
        return ','.join(str(node) for node in self)

    def add_below(self, parent, child):
        ''' Add a child below a parent. Only two children per parent
            allowed. '''

        where = self.find(parent)

        if not where:
            raise ValueError('could not find ' + parent)

        if not where.left:
            where.left = FamilyTree(child, where)
        elif not where.right:
            where.right = FamilyTree(child, where)
        else:
            raise ValueError(self + 'already has the allotted two children')

    # Not a BST; have to search up to the whole tree
    def find(self, name):
        if self.name == name: return self

        if self.left:
            left = self.left.find(name)
            if left: return left

        if self.right:
            right = self.right.find(name)
            if right: return right

        return None

    def Parent(self, name):
        parent = None
        if self.name == name:
            return self.parent
        if self.left:
            if self.left.name == name:
                return self.name
            elif not parent:
                parent = self.left.Parent(name)
        if self.right:
            if self.right.name == name:
                return self.name
            elif not parent:
                parent = self.right.Parent(name)
        return parent

    def grandparent(self, name):
        grandparent = None
        parent = self.Parent(name)
        grandparent = self.Parent(parent)
        return grandparent

    def root(self):
        if self.parent == None:
            return self.name
        else: self.root(self.Parent)

    def generations(self):
        ''' Return a list of lists, where each sub-list is a generation.  '''

        # First, create a list 'this_level' with the root, and three empty
        # lists: 'next_level', 'result', and 'names'

        # While 'this_level' has values
            # Remove the first element and append its name to 'names'

            # If the first element has a left, append it to 'next_level'
            # and do the same for the right

            # If 'this_level' is now empty
                # Append 'names' to 'result', set "this_level' to
                # 'next_level', and 'next_level' and 'names' to empty
                # lists

        this_level = [self.name]
        next_level =[]
        result =[]
        names = []

        while this_level:
            for element in range(len(this_level)):
                names.append(this_level[element])
                if self.find(this_level[element]).left:
                    next_level.append(self.find(this_level[element]).left.name)
                if self.find(this_level[element]).right:
                    next_level.append(self.find(this_level[element]).right.name)
            this_level = next_level
            result.append(names)
            names = []
            next_level = []

        # return result
        return result

    def inorder(self):
        ''' Return a list of the in-order traversal of the tree. '''
        family = []
        if self.left: family.extend(self.left.inorder())
        family.append(self.name)
        if self.right: family.extend(self.right.inorder())
        return family

    def preorder(self):
        ''' Return a list of the pre-order traversal of the tree. '''
        family = []
        family.append(self.name)
        if self.left: family.extend(self.left.preorder())
        if self.right: family.extend(self.right.preorder())
        return family

    def postorder(self):
        ''' Return a list of the post-order traversal of the tree. '''
        family = []
        if self.left: family.extend(self.left.postorder())
        if self.right: family.extend(self.right.postorder())
        family.append(self.name)
        return family

class CLevelTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(str(FamilyTree(None)), 'None')
    def setUp(self):
        self.tree = FamilyTree("Grandpa")
        self.tree.add_below("Grandpa", "Homer")
        self.tree.add_below("Grandpa", "Herb")
        self.tree.add_below("Homer", "Bart")
        self.tree.add_below("Homer", "Lisa")
    def test_str(self):
        self.assertEqual(str(self.tree), "Bart,Homer,Lisa,Grandpa,Herb")

    ''' Write tests for your pre, in, and post-order traversals. '''
    def test_inorder(self):
        self.assertEqual(self.tree.inorder(), ["Bart", "Homer", "Lisa", "Grandpa", "Herb"])

    def test_preorder(self):
        self.assertEqual(self.tree.preorder(), ["Grandpa", "Homer", "Bart", "Lisa", "Herb"])

    def test_postorder(self):
        self.assertEqual(self.tree.postorder(), ["Bart", "Lisa", "Homer", "Herb", "Grandpa"])

class BLevelTests(unittest.TestCase):
    def setUp(self):
        self.tree = FamilyTree("Grandpa")
        self.tree.add_below("Grandpa", "Homer")
        self.tree.add_below("Grandpa", "Herb")
        self.tree.add_below("Homer", "Bart")
        self.tree.add_below("Homer", "Lisa")
        self.tree.add_below("Bart", "Picard")
        self.tree.add_below("Bart", "Kirk")
        self.tree.add_below("Lisa", "Zia")
    def testParent(self):
        self.assertEquals(self.tree.Parent("Lisa"), "Homer")
        self.assertEquals(self.tree.Parent("Homer"), "Grandpa")
        self.assertEquals(self.tree.Parent("Bart"), "Homer")
        self.assertEquals(self.tree.Parent("Herb"), "Grandpa")
        self.assertEquals(self.tree.Parent("Kirk"), "Bart")
        self.assertEquals(self.tree.Parent("Picard"), "Bart")
        self.assertEquals(self.tree.Parent("Zia"), "Lisa")
    def test_grandparent(self):
        self.assertEquals(self.tree.grandparent("Lisa"), "Grandpa")
        self.assertEquals(self.tree.grandparent("Zia"), "Homer")
        self.assertEquals(self.tree.grandparent("Kirk"), "Homer")
        self.assertEquals(self.tree.grandparent("Picard"), "Homer")
        self.assertEquals(self.tree.grandparent("Bart"), "Grandpa")
    def test_no_grandparent(self):
        self.assertEquals(self.tree.grandparent("Homer"), None)

class ALevelTests(unittest.TestCase):
    def setUp(self):
        self.tree = FamilyTree("Grandpa")
        self.tree.add_below("Grandpa", "Homer")
        self.tree.add_below("Grandpa", "Herb")
        self.tree.add_below("Homer", "Bart")
        self.tree.add_below("Homer", "Lisa")
        self.tree.add_below("Bart", "Picard")
        self.tree.add_below("Bart", "Kirk")
        self.tree.add_below("Lisa", "Zia")
    def test_generations(self):
        self.assertEqual(self.tree.generations(), \
            [["Grandpa"], ["Homer", "Herb"], ["Bart", "Lisa"], ["Picard", "Kirk", "Zia"]])

    def test_root(self):
        self.assertEqual(self.tree.root(), "Grandpa")


class ExtraTest(unittest.TestCase):
    def setUp(self):
         self.tree = FamilyTree("Grandpa")
         self.tree.add_below("Grandpa", None)
         self.tree.add_below(None, "Grandson")

    def test_EmptyNode(self):
        self.assertEqual(self.tree.generations(), \
                             [["Grandpa"], [None], ["Grandson"]])


    ''' Write some more tests, especially for your generations method. '''

if '__main__' == __name__:
    ''' Read from standard input a list of relatives. The first line must
        be the ultimate ancestor (the root). The following lines are in the
        form: parent child.'''

    for line in stdin:
        a = line.strip().split(" ")
        if len(a) == 1:
            ft = FamilyTree(a[0])
        else:
            ft.add_below(a[0], a[1])

    print(ft.generations())
