from __future__ import print_function
import unittest

''' when run with "-m unittest", the following produces:
    FAILED (failures=9, errors=2)
    your task is to fix the failing tests by implementing the necessary
    methods. '''

class LinkedList(object):
    class Node(object):
        # pylint: disable=too-few-public-methods
        ''' no need for get or set, we only access the values inside the
            LinkedList class. and really, never have setters. '''
        def __init__(self, value, next_node):
            self.value = value
            self.next_node = next_node

    def __init__(self, initial = None):
        self.front = self.back = self.current = None
        if initial is not None:
                for i in range(len(initial)):
                    self.push_front(str(initial[i]))

    def empty(self):
        return self.front == self.back == None

    def __iter__(self):
        self.current = self.front
        return self

    def __next__(self):
        if self.current:
            tmp = self.current.value
            self.current = self.current.next_node
            return tmp
        else:
            raise StopIteration()

    def __str__(self):
        tmp = ""
        while not self.empty():
            tmp += str(self.pop_back()) + ', '
        return tmp[:-2]

    def __repr__(self):
        if self.empty():
            tmp = "LinkedList()"
        else:
            tmp = "LinkedList((" + self.__str__() + "))"
        return tmp

    def delete_value(self, value):
        current = self.front
        while current.next_node is not None:
            if value == current.value:
                current.value = None
                tmp.next_node = current.next_node
            else:
                tmp = current
                current = current.next_node

    def mid_value(self):
        first = self.front
        second = self.front
        while first.next_node is not None:
            first = first.next_node
            if first.next_node is not None:
                first = first.next_node
                second = second.next_node
        return second.value

    def push_front(self, value):
        new = self.Node(value, self.front)
        if self.empty():
            self.front = self.back = new
        else:
            self.front = new

    ''' you need to(at least) implement the following three methods'''
    def pop_front(self):
        if self.empty():
            raise RuntimeError
        temp = self.front.value
        if self.front == self.back:
            self.front = self.back = None
        else:
            self.front = self.front.next_node
        return temp

    def push_back(self, value):
        new = self.Node(value, None)
        if self.empty():
            self.front = self.back = new
        else:
            self.back.next_node = new
            self.back = new


    def pop_back(self):
        if self.empty():
            raise RuntimeError
        temp = self.back.value
        current = self.front
        if self.front == self.back:
            self.front = self.back = None
        else:
            while current.next_node is not self.back:
                current = current.next_node
            if current.next_node == self.back:
                self.back = current
                self.back.next_node = None
        return temp

''' C-level work '''
class TestEmpty(unittest.TestCase):
    def test(self):
        self.assertTrue(LinkedList().empty())

class TestPushFrontPopBack(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_back(), 1)
        self.assertEqual(linked_list.pop_back(), 2)
        self.assertEqual(linked_list.pop_back(), 3)
        self.assertTrue(linked_list.empty())

class TestPushFrontPopFront(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        self.assertEqual(linked_list.pop_front(), 3)
        self.assertEqual(linked_list.pop_front(), 2)
        self.assertEqual(linked_list.pop_front(), 1)
        self.assertTrue(linked_list.empty())

class TestPushBackPopFront(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back(2)
        linked_list.push_back(3)
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_front(), 1)
        self.assertEqual(linked_list.pop_front(), 2)
        self.assertEqual(linked_list.pop_front(), 3)
        self.assertTrue(linked_list.empty())

class TestPushBackPopBack(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back("foo")
        linked_list.push_back([3, 2, 1])
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_back(), [3, 2, 1])
        self.assertEqual(linked_list.pop_back(), "foo")
        self.assertEqual(linked_list.pop_back(), 1)
        self.assertTrue(linked_list.empty())

''' B-level work '''
class TestInitialization(unittest.TestCase):
    def test(self):
        linked_list = LinkedList(("one", 2, 3.141592))
        self.assertEqual(linked_list.pop_back(), "one")
        self.assertEqual(linked_list.pop_back(), "2")
        self.assertEqual(linked_list.pop_back(), "3.141592")

class TestStr(unittest.TestCase):
    def test(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.__str__(), '1, 2, 3')

''' A-level work '''
class TestRepr(unittest.TestCase):
    def test(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.__repr__(), 'LinkedList((1, 2, 3))')

class TestErrors(unittest.TestCase):
    def test_pop_front_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().pop_front())
    def test_pop_back_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().pop_back())

''' write some more test cases. '''

class TestEmptyRepr(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        self.assertEqual(linked_list.__repr__(),'LinkedList()')

class TestEmptyStr(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        self.assertEqual(linked_list.__str__(),'')


''' extra credit.
    - write test cases for and implement a delete(value) method.
    - write test cases for and implement a method that finds the middle
      element with only a single traversal.
'''
class TestDeleteValue(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        linked_list.push_front(4)
        linked_list.push_front(5)
        linked_list.delete_value(2)
        linked_list.delete_value(4)
        self.assertEqual(linked_list.pop_front(), 5)
        self.assertEqual(linked_list.pop_front(), 3)
        self.assertEqual(linked_list.pop_front(), 1)

class TestOddMiddle(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        linked_list.push_front(4)
        linked_list.push_front(5)
        self.assertEqual(linked_list.mid_value(), 3)


''' the following is a demonstration that uses our data structure as a
    stack'''

def fact(number):
    '''"Pretend" to do recursion via a stack and iteration'''

    if number < 0: raise ValueError("Less than zero")
    if number == 0 or number == 1: return 1

    stack = LinkedList()
    while number > 1:
        stack.push_front(number)
        number -= 1

    result = 1
    while not stack.empty():
        result *= stack.pop_front()

    return result

class TestFactorial(unittest.TestCase):
    def test_less_than_zero(self):
        self.assertRaises(ValueError, lambda: fact(-1))
    def test_zero(self):
        self.assertEqual(fact(0), 1)
    def test_one(self):
        self.assertEqual(fact(1), 1)
    def test_two(self):
        self.assertEqual(fact(2), 2)
    def test_10(self):
        self.assertEqual(fact(10), 10*9*8*7*6*5*4*3*2*1)

if '__main__' == __name__:
    unittest.main()