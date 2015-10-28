import sys
import math
import random
import numpy as np

evals = 0
budget = 0
fixed = []

class Solution:
    def __init__(self, answer):
        self.cells = cells
        self.fitness = sys.float_info.max

def read_data(filename):
    global fixed

    with open(filename) as f:
        lines = f.readlines()
        if ['|'] in lines[0]:
            line_num = 0
            for line in lines:
                line = list(line.strip().replace("|", ""))
                for i, x in enumerate(line):
                    if x != ".":
                        fixed.append[9*linenum + i]
        else:
            line = list(lines[0].strip())
            for i, x in enumerate(line):
                if x != ".":
                    fixed.append[i]

    return num

def initialize_generation(size):
    global fixed

    pop = []
    while len(pop) < size:
        board = np.zeros(9)

        # Nine cells
        for cell_no in range(9):
            start = (cell_no / 3) * 9 + (cell_no % 3) * 3
            cell = np.zeros(9)

            for i in range(3):
                for j in range(3):
                    pos = start + i + 3 * j

                    # Each cell contains 1 to 9 exactly once
                    if pos in fixed:
                        cell.append(fixed[pos])

                    x = random.randrange(1,10)
                    while x in cell:
                        x = random.randrange(1, 10)

                    cell.append(x)

            cell.shape = 3, 3
            board.append(cell)

        board.shape(3, 3)
        popuplation.append(board)

    return population

def evaluate(sol):
    global evals
    evals += 1
    sol.fitness = 0
    for i in range(len(sol.permutation) - 1):
        sol.fitness += dist[sol.permutation[i]][sol.permutation[i+1]]
    sol.fitness += dist[sol.permutation[0]][sol.permutation[-1]]

def two_opt(filename):
    num = read_data(filename)

    original = Solution(np.random.permutation(range(num)))
    evaluate(original)
    best = original
    print best.fitness

    while evals < budget:
        for i in range(0, num-1):
            for k in range(i+1, num):
                newsol = two_opt_swap(original, i, k)
                if newsol.fitness < best.fitness:
                    best = newsol

        if best == original:
            break

        print best.fitness
        original = best

    return best

def two_opt_swap(sol, i, k):
    source = list(sol.permutation)
    source[i:k+1] = reversed(source[i:k+1])
    newsol = Solution(np.asarray(source))
    evaluate(newsol)
    return newsol

if __name__ == '__main__':
    budget = 5000000
    sol = two_opt(sys.argv[1])
    print ", ".join([str(x) for x in list(sol.permutation)])
    print sol.fitness
