from __future__ import print_function
import unittest
import math

'''
Description: Dictionary
Author: Nick Barnes
Version: 1.0
Help provided to: 
Help received from: 
'''

'''
    Implement a dictionary using chaining.
    You may assume every key has a hash() method, e.g.:
    >>> hash(1)
    1
    >>> hash('hello world')
    -2324238377118044897
'''

class dictionary:
    def __init__(self, init=None):
        self.__limit = 10
        self.__items = [[] for _ in range(self.__limit)]
        self.__count = 0

        if init:
            for i in init:
                self.__setitem__(i[0], i[1])

    def __len__(self):
        return self.__count

    def __flattened(self):
        return [item for inner in self.__items for item in inner]

    def __iter__(self):
        return(iter(self.__flattened()))

    def __str__(self):
        return(str(self.__flattened()))

    def __rehashUp(self):
        self.__limit = self.__limit * 2
        tmp = self.__items
        self.__items = [[] for _ in range(self.__limit)]
        self.__count = 0
        for item in tmp:
            if item is not []:
                for i in item:
                    key = i[0]
                    value = i[1]
                    self.__setitem__(key, value)

    def __rehashDown(self):
        self.__limit = int(self.__limit / 2)
        tmp = self.__items
        self.__items = [[] for _ in range(self.__limit)]
        self.__count = 0
        for item in tmp:
            if item is not []:
                for i in item:
                    key = i[0]
                    value = i[1]
                    self.__setitem__(key, value)

    def limit(self):
        return self.__limit

    def count(self):
        return self.__count

    def __setitem__(self, key, value):
        if self.__items[int(math.fabs(hash(key)) % self.__limit)] == []:
            self.__items[int(math.fabs(hash(key)) % self.__limit)].append([key, value])
            self.__count = 1 + self.__count
            if ((self.__count / self.__limit) >= 0.75):
                self.__rehashUp()
        else:
            found = False
            notFound = False
            while found is not True and notFound is not True:
                i = 0
                while i is not self.__limit:
                    test = self.__items[i]
                    if test != []:
                        if test[0][0] == key:
                            found = True
                            break
                    i += 1
                notFound = True
            if found is not True:
                self.__items[int(math.fabs(hash(key))) % self.__limit].insert(0, [key, value])
                self.__count = 1 + self.__count
                if ((self.__count / self.__limit) >= 0.75):
                    self.__rehashUp()

    def __getitem__(self, key):
        if self.__items[int(math.fabs(hash(key))) % self.__limit] != []:
            i = 0
            while i <= self.__limit - 1:
                test = self.__items[i]
                if test != []:
                    if test[0][0] == key:
                        return test[0][1]
                i = i + 1
        return -1

    def __contains__(self, key):
        found = False
        if self.__items[int(math.fabs(hash(key)) % self.__limit)] != []:
            i = 0
            while i <= self.__limit - 1:
                foo = self.__items[i]
                if foo != []:
                    for item in foo:
                        if item[0] == key:
                            found = True
                i = i + 1
        return found

    def __delitem__(self, key):
        if self.__items[int(math.fabs(hash(key))) % self.__limit] != []:
            i = 0
            while i <= self.__limit - 1:
                foo = self.__items[i]
                if foo != []:
                    for item in foo:
                        if item[0] == key:
                            self.__items[i].remove(item)
                            self.__count -= self.__count
                            if ((self.__count / self.__limit) <= 0.25):
                                self.__rehashDown()
                            break
                i = i + 1

    def keys(self):
        keys = []
        for item in self.__items:
            if item is not []:
                for i in item:
                    key = i[0]
                    keys.append(key)
        return keys

    def values(self):
        values = []
        for item in self.__items:
            if item is not []:
                for i in item:
                    value = i[1]
                    values.append(value)
        return values

    def __eq__(self, other):
        equal = False
        if self.__str__() == other.__str__():
            equal = True
        return equal

    def items(self):
        items = []
        for item in self.__items:
            if item is not []:
                for i in item:
                    key = i[0]
                    value = i[1]
                    tuple = (key, value)
                    items.append(tuple)
        return items

''' C-level work
'''

class test_add_two(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        self.assertEqual(len(s), 2)
        self.assertEqual(s[1], "one")
        self.assertEqual(s[2], "two")

class test_add_twice(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[1] = "one"
        self.assertEqual(len(s), 1)
        self.assertEqual(s[1], "one")

class test_store_false(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = False
        self.assertTrue(1 in s)
        self.assertTrue(1 in s)
        self.assertFalse(s[1])

class test_store_none(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = None
        self.assertTrue(1 in s)
        self.assertEqual(s[1], None)

class test_none_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[None] = 1
        self.assertTrue(None in s)
        self.assertEqual(s[None], 1)

class test_False_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[False] = 1
        self.assertTrue(False in s)
        self.assertEqual(s[False], 1)

class test_collide(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        self.assertEqual(len(s), 2)
        self.assertTrue(0 in s)
        self.assertTrue(10 in s)

''' B-level work
    Add doubling and rehashing when load goes over 75%
    Add __delitem__(self, key)
'''

class test_rehashUp(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[4] = "four"
        s[44] = "forty four"
        s[5] = "five"
        s[8] = "eight"
        s[12] = "twelve"
        s[7] = "seven"
        s[9] = "nine"
        s[88] = "eighty eight"
        self.assertEqual(s.limit(), 20)
        self.assertEqual(s.count(), 8)

class test_deleteItem(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        s.__delitem__(0)
        self.assertFalse(0 in s)
        self.assertTrue(10 in s)

''' A-level work
    Add halving and rehashing when load goes below 25%
    Add keys()
    Add values()
'''

class test_rehashDown(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[4] = "four"
        s[44] = "forty four"
        s[5] = "five"
        s[8] = "eight"
        s[12] = "twelve"
        s[7] = "seven"
        s[9] = "nine"
        s[88] = "eighty eight"
        self.assertEqual(s.limit(), 20)
        self.assertEqual(s.count(), 8)
        s.__delitem__(4)
        s.__delitem__(12)
        s.__delitem__(9)
        s.__delitem__(88)
        self.assertEqual(s.limit(), 10)
        self.assertEqual(s.count(), 4)

class test_keys(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[4] = "four"
        s[44] = "forty four"
        s[5] = "five"
        s[8] = "eight"
        self.assertEqual(s.keys(), [44, 4, 5, 8])

class test_values(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[4] = "four"
        s[44] = "forty four"
        s[5] = "five"
        s[8] = "eight"
        self.assertEqual(s.values(), ["forty four", "four", "five", "eight"])

''' Extra credit
    Add __eq__()
    Add items(), "a list of D's (key, value) pairs, as 2-tuples"
'''

class test_equal(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[4] = "four"
        s[44] = "forty four"
        s[5] = "five"
        s[8] = "eight"
        d = dictionary()
        d[4] = "four"
        d[44] = "forty four"
        d[5] = "five"
        d[8] = "eight"
        self.assertEqual(s.__eq__(d), True)

class test_items(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[4] = "four"
        s[44] = "forty four"
        s[5] = "five"
        self.assertEqual(s.items(), [(44, "forty four"), (4, "four"), (5, "five")])

if '__main__' == __name__:
    unittest.main()