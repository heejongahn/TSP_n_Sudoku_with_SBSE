import sys
import math
import random
import numpy as np

evals = 0
budget = 0
fixed = {}

class Solution:
    def __init__(self, board):
        self.board = board
        self.fitness = sys.float_info.max

def read_data(filename):
    global fixed

    with open(filename) as f:
        lines = f.readlines()
        if '|' in lines[0]:
            line_no = 0

            for line in lines:
                if "-" in line:
                    continue
                line = line.strip().replace("|", "").split()
                print line
                for i, x in enumerate(line):
                    if x != ".":
                        fixed[9 * line_no + i] = int(x)

                line_no += 1
        else:
            line = list(lines[0].strip().replace(" ", ""))
            for i, x in enumerate(line):
                if x != ".":
                    fixed[i] = int(x)

def initialize_generation(size):
    global fixed

    pop = []
    while len(pop) < size:
        board = []

        # Nine cells
        for cell_no in range(9):
            start = (cell_no / 3) * 9 + (cell_no % 3) * 3
            cell = np.zeros(9)
            cell.shape = 3, 3

            available = range(1, 10)
            for i in range(3):
                for j in range(3):
                    pos = start + i * 9 + j

                    if pos in fixed:
                        cell[i][j] = fixed[pos]
                        available.remove(cell[i][j])

            for i in range(3):
                for j in range(3):
                    pos = start + i * 9 + j

                    if cell[i][j] == 0:
                        x = random.choice(available)
                        cell[i][j] = x
                        available.remove(x)

            cell.shape = 9
            board.append(cell)
            sol = Solution(board)

        pop.append(sol)

    return pop

def evaluate(sol):
    board = sol.board
    f = 0

    # row violation
    for i in range(9):
        row = []
        for j in range(3):
            for k in range(3):
                row.append(board[(i / 3) * 3 + j][(i % 3) * 3 + k])

        f += count_violation(row)

    # column violation
    for i in range(9):
        col = []
        for j in range(3):
            for k in range(3):
                col.append(board[(i / 3) + j * 3][(i % 3) + k * 3])

        f += count_violation(col)

    sol.fitness = f


def count_violation(line):
    v = 0
    for i in range(1, 10):
        v += abs(1 - line.count(i))

    v /= 2

    return v


if __name__ == '__main__':
    budget = 5000000
