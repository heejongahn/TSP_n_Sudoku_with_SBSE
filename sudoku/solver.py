import sys
import math
import random
import numpy as np
import copy
from collections import OrderedDict

evals = 0
budget = 0
fixed = {}
available = []
for _ in range(81):
    available.append([True] * 9)
candidates = []

class Solution:
    def __init__(self, board):
        self.board = board
        self.fitness = sys.float_info.max

# # # # # # # # # # # # # # # # #
#  Read data (Only called once) #
# # # # # # # # # # # # # # # # #

def read_data(filename):
    global fixed, available, candidates

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
                        pencilmark(9 * line_no + i, int(x))
                line_no += 1

        else:
            line = list(lines[0].strip().replace(" ", ""))
            for i, x in enumerate(line):
                if x != ".":
                    fixed[i] = int(x)
                    pencilmark(i, int(x))

    for cell in available:
        candidates.append([(i + 1) for i, x in enumerate(cell) if x])

def pencilmark(pos, cddtue):
    global available

    available[pos] = [False] * 9

    row_start = (pos / 9) * 9
    col_start = pos % 9

    cell_a = pos / 27
    cell_b = (pos % 9) / 3

    cell_start = cell_a * 27 + cell_b * 3

    # Row
    for i in range(9):
        available[row_start + i][cddtue - 1] = False

    # Column
    for i in range(9):
        available[col_start + 9 * i][cddtue - 1] = False

    # Cell
    for i in range(3):
        for j in range(3):
            available[cell_start + 9 * i + j][cddtue - 1] = False

def update():
    global candidates

    while True:
        changed = False
        candidates = []
        for cell in available:
            candidates.append([(i + 1) for i, x in enumerate(cell) if x])


        # Row
        for i in range(9):
            occurrence = [-2] * 9
            for j in range(9):
                for cddt in candidates[i * 9 + j]:
                    if occurrence[cddt-1] == -2:
                        occurrence[cddt-1] = j
                    else:
                        occurrence[cddt-1] = -1

            for cddt, j in enumerate(occurrence):
                if 0 <= j:
                    changed = True
                    fixed[i * 9 + j] = cddt + 1
                    pencilmark(i * 9 + j, cddt + 1)

        # Column
        for i in range(9):
            occurrence = [-2] * 9
            for j in range(9):
                for cddt in candidates[i + j * 9]:
                    if occurrence[cddt-1] == -2:
                        occurrence[cddt-1] = j
                    else:
                        occurrence[cddt-1] = -1

            for cddt, j in enumerate(occurrence):
                if 0 <= j:
                    changed = True
                    fixed[i + j * 9] = cddt + 1
                    pencilmark(i + j * 9, cddt + 1)

        # Cell
        for start in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
            occurrence = [-2] * 9
            for i in range(3):
                for j in range(3):
                    k = i * 9 + j
                    pos = start + k
                    for cddt in candidates[pos]:
                        if occurrence[cddt-1] == -2:
                            occurrence[cddt-1] = k
                        else:
                            occurrence[cddt-1] = -1

            for cddt, k in enumerate(occurrence):
                if 0 <= k:
                    changed = True
                    fixed[start + k] = cddt + 1
                    pencilmark(start + k, cddt + 1)

        if not changed:
            print "Update routine end"
            break

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

# # # # # # # # # # # # # #
#  Population Initialize  #
# # # # # # # # # # # # # #

def init_population(gen_size):
    global fixed, candidates
    population = []

    for _ in range(gen_size):
        board = []

        # Nine cells
        for cell_no in range(9):
            start = (cell_no / 3) * 27 + (cell_no % 3) * 3
            p_cell = np.zeros(9)
            p_cell.shape = 3, 3

            p_unfixed = range(1, 10)
            for i in range(3):
                for j in range(3):
                    pos = start + i * 9 + j

                    if pos in fixed:
                        p_cell[i][j] = fixed[pos]
                        p_unfixed.remove(p_cell[i][j])

            while True:
                cell = copy.deepcopy(p_cell)
                unfixed = p_unfixed[:]


                for i in range(3):
                    for j in range(3):
                        pos = start + i * 9 + j

                        if cell[i][j] == 0:
                            x = random.choice(unfixed)
                            cell[i][j] = x
                            unfixed.remove(x)

                v = 0
                for i in range(3):
                    for j in range(3):
                        pos = start + i * 9 + j
                        if candidates[pos] != [] and cell[i][j] not in candidates[pos]:
                            v += 1

                if v < 1:
                    break

            cell.shape = 9
            board.append(cell)

        sol = Solution(board)
        evaluate(sol)
        population.append(sol)
    return population

# # # # # # # # # # # #
#  Genetic Algorithm  #
# # # # # # # # # # # #

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
    update()
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
                print best.board

        print best.fitness

if __name__ == '__main__':
    budget = 500000
    ga(sys.argv[1])
