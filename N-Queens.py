from __future__ import print_function
import unittest, sys

'''

Author: Nick Barnes
Version: 1.0
Assignment: N-Queens

    Given the location of two queens, find if they are safe
    from each other.
'''
def safe(one, two):
    if one[0] == two[0]: return False
    if one[1] == two[1]: return False
    if abs(two[0]-one[0]) == abs(two[1]-one[1]): return False
    return True

def print_solution(size, placed):
    print("for:", size)
    if placed == []:
        print("no solution found")
        return

    print('-' * size)

    for i in range(size):
        for j in range(size):
            if [i, j] in placed:
                sys.stdout.write("Q")
            else:
                sys.stdout.write(".")
        print()

    print('-' * size)

def solve_queens(size, row, placed):
    if row == size:
        return placed

    for column in range(size):
        temp = True
        for queen in placed:
            if temp and not safe([row, column], queen):
                temp = False
                break
        if temp:
            foo = solve_queens(size, row + 1, placed + [[row, column]])
            if foo:
                return foo
    return []
'''
solve_queens(size, row, placed)
    if the row is greater than the size of the board, we're done

    go through the columns in this row
        go through all the already placed queens and see if
            placing a new queen at (row, column) is safe

        if it is
            tmp = solve_queens(size, row+1, placed+[(row, column)])
            if tmp
                return tmp
'''
class test__queens(unittest.TestCase):
    def test_Four(self):
        placed = solve_queens(4, 0, [])
        print_solution(4, placed)

    def test_Eight(self):
        placed = solve_queens(8, 0, [])
        print_solution(8, placed)

    def test_Sixteen(self):
        placed = solve_queens(16, 0, [])
        print_solution(16, placed)

    def test_unsafe(self):
        self.assertFalse(safe([1,1], [1,2]))

    def test_safe(self):
        self.assertTrue(safe([0,0], [1,2]))