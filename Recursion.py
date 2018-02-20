from __future__ import print_function
import unittest

'''
Description: Recursion
Author: Nick Barnes 
Version: 1.0
Help received from:
Help provided to:
'''

def findandreplace(find, replace, string):
    if find == None: return string
    if replace == None: return string
    result = type(string)()
    if string == result: return result
    if len(find) == len(string):
        if find == string:
            string = replace
            return string
    if len(find) > 1:
        length = len(find)
        stringslice = string[:length]
        if stringslice != find:
            return string[:1] + findandreplace(find, replace, string[1:])
        if stringslice == find:
            stringslice = replace
        return stringslice + findandreplace(find, replace, string[length:])
    stringslice = string[:1]
    if stringslice == find:
        stringslice = replace
    return stringslice + findandreplace(find, replace, string[1:])


'''
    Replace all instances of find with replace in string.

    Recursive approach:
    If the string starts with find, return replace and findandreplace
    with the rest of the string, else return the first character of the
    string and findandreplace with the rest of the string
'''


class TestFindAndReplace(unittest.TestCase):
    def test_all_none(self):
        self.assertEqual(findandreplace(None, None, None), None)
    def test_find_none(self):
        self.assertEqual(findandreplace(None, "a", "aabb"), "aabb")
    def test_find_empty(self):
        self.assertEqual(findandreplace("", "a", "aabb"), "aabb")
    def test_replace_none(self):
        self.assertEqual(findandreplace("a", None, "aabb"), "aabb")
    def test_string_none(self):
        self.assertEqual(findandreplace("a", "b", None), None)
    def test_simple(self):
        self.assertEqual(findandreplace("a", "b", "aabb"), "bbbb")
    def test_remove(self):
        self.assertEqual(findandreplace(" ", "", " a abb"), "aabb")
    def test_gettysburg(self):
        self.assertEqual(findandreplace("Four score", "Twenty", \
            "Four score and seven years ago"), "Twenty and seven years ago")
    def test_middle(self):
        self.assertEqual(findandreplace("o", "e", "food"), "feed")
    def test_middlegettysburg(self):
        self.assertEqual(findandreplace("seven years", "a million days", \
            "Four score and seven years ago"), "Four score and a million days ago")
    def test_endgettysburg(self):
        self.assertEqual(findandreplace("years ago", "months from now", \
            "Four score and seven years ago"), "Four score and seven months from now")

if '__main__' == __name__:
    unittest.main()