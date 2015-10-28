import sys
import math
import random
import numpy as np
import copy

evals = 0
budget = 0
fixed = {}

class Solution:
    def __init__(self, board):
        self.board = board
        self.fitness = sys.float_info.max

def read_data(filename):
    global fixed, available

    with open(filename) as f:
        lines = f.readlines()
        if '|' in lines[0]:
            line_no = 0

            for line in lines:
                if "-" in line:
                    continue
                line = line.strip().replace("|", "").split()
                for i, x in enumerate(line):
                    if x != ".":
                        fixed[9 * line_no + i] = int(x)
                line_no += 1

        else:
            line = list(lines[0].strip().replace(" ", ""))
            for i, x in enumerate(line):
                if x != ".":
                    fixed[i] = int(x)

def evaluate(sol):
    global evals
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
    evals += 1

def count_violation(line):
    v = 0
    for i in range(1, 10):
        v += abs(1 - line.count(i))
    return v / 2

def init_population(gen_size):
    global fixed
    population = []

    for _ in range(gen_size):
        board = []

        # Nine cells
        for cell_no in range(9):
            start = (cell_no / 3) * 9 + (cell_no % 3) * 3
            cell = np.zeros(9)
            cell.shape = 3, 3

            unfixed = range(1, 10)
            for i in range(3):
                for j in range(3):
                    pos = start + i * 9 + j

                    if pos in fixed:
                        cell[i][j] = fixed[pos]
                        unfixed.remove(cell[i][j])

            for i in range(3):
                for j in range(3):
                    pos = start + i * 9 + j

                    if cell[i][j] == 0:
                        x = random.choice(unfixed)
                        cell[i][j] = x
                        unfixed.remove(x)

            cell.shape = 9
            board.append(cell)
            sol = Solution(board)

        evaluate(sol)
        population.append(sol)
    return population

def crossover(parent_1, parent_2):
    cp = random.choice(range(1, 9))

    sol_1 = Solution(parent_1.board[:cp] + parent_2.board[cp:])
    sol_2 = Solution(parent_2.board[:cp] + parent_1.board[cp:])

    return sol_1, sol_2

def mutate(sol):
    cell_no = random.choice(range(0, 9))
    cell = sol.board[cell_no]
    start = (cell_no / 3) * 9 + (cell_no % 3) * 3

    unfixed = range(1, 10)
    for i in range(3):
        for j in range(3):
            pos = start + i * 9 + j
            if pos in fixed:
                unfixed.remove(fixed[pos])

    num = len(unfixed)
    a, b = random.choice(unfixed), random.choice(unfixed)

    while a == b:
        b = random.choice(unfixed)

    i, j = np.where(cell==a)[0][0], np.where(cell==b)[0][0]

    cell[i], cell[j] = cell[j], cell[i]

def ga(filename):
    read_data(filename)
    best = Solution([])
    population = init_population(200)

    for sol in population:
        if sol.fitness < best.fitness:
            best = sol

    while evals < budget:
        new_gen = []
        while len(new_gen) < 200:
            parent_1 = random.choice(population)
            parent_2 = random.choice(population)
            child_1, child_2 = crossover(parent_1, parent_2)

            if random.random < 0.1:
                mutate(child_1)
            if random.random < 0.1:
                mutate(child_2)

            evaluate(child_1)
            evaluate(child_2)
            new_gen.append(child_1)
            new_gen.append(child_2)

        population = new_gen

        for sol in population:
            if sol.fitness < best.fitness:
                best = sol

        print best.fitness


if __name__ == '__main__':
    budget = 5000000
    ga(sys.argv[1])
