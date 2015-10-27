import sys
import math
import random
from operator import attrgetter
import numpy as np

evals = 0
budget = 0
dist = None

class Solution:
    def __init__(self, permutation, random=False):
        self.permutation = permutation
        self.fitness = sys.float_info.max

def read_data(filename):
    global dist
    coords = []

    with open(filename) as f:
        while True:
            line = f.readline()
            if line == 'NODE_COORD_SECTION\n':
                break

        for line in f.readlines():
            if 'EOF' in line:
                break

            _, x, y = line.strip().split(" ")
            coords.append((float(x), float(y)))
            num = len(coords)
            dist = np.zeros(num ** 2)
            dist.shape = (num, num)
            for i in range(num):
                for j in range(num):
                    dist[i][j] = math.sqrt((coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2)

    return num

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
