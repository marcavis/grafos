#!/usr/bin/env python3
class Sudoku():
    def __init__(self, matriz=[]):
        if matriz == []:
            self.matriz = self.novaMatriz()
        else:
            self.matriz = matriz

    def novaMatriz(self):
        return [[None] * 9] * 9

    def __str__(self):
        return "olá"

s = Sudoku()
t = Sudoku([[None,   3,None,None,None,   5,   1,   7,None],
            [   5,None,None,None,   3,None,None,None,   2],
            [None,None,None,None,   2,None,None,None,   6],
            [None,None,None,None,   7,None,None,None,   9],
            [None,   1,   6,None,None,None,   2,   3,None],
            [   9,None,None,None,   8,None,None,None,None],
            [   6,None,None,None,   1,None,None,None,None],
            [   1,None,None,None,   9,None,None,None,   8],
            [None,   7,   8,   6,None,None,None,   4,None]])
print(t)
