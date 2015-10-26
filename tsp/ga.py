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
    lines = open(filename).readlines()
    coords = []
    for line in lines:
        if line[0].isdigit():
            no, x, y = line.strip().split(" ")
            coords.append((float(x), float(y)))
    num = len(coords)
    dist = np.zeros(num ** 2)
    dist.shape = (num, num)
    for i in range(num - 1):
        for j in range(1, num):
            dist[i][j] = math.sqrt((coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2)
    return num, dist

def evaluate(sol):
    global evals
    evals += 1
    sol.fitness = 0
    for i in range(len(sol.permutation) - 1):
        sol.fitness += dist[sol.permutation[i]][sol.permutation[i+1]]

class Crossover:
    def pmx(self, parent_a, parent_b):
        assert(len(parent_a.permutation) == len(parent_b.permutation))
        size = len(parent_a.permutation)

        cp1 = random.randrange(size)
        cp2 = random.randrange(size)
        while(cp2 == cp1):
            cp2 = random.randrange(size)

        if cp2 < cp1:
            cp1, cp2 = cp2, cp1

        map_a = {}
        map_b = {}
        
        child_a = Solution(parent_a.permutation)
        child_b = Solution(parent_b.permutation)
        for i in range(cp1, cp2 + 1):
            item_a = child_a.permutation[i]
            item_b = child_b.permutation[i]
            child_a.permutation[i] = item_b
            child_b.permutation[i] = item_a
            map_a[item_b] = item_a
            map_b[item_a] = item_b

        self.check_unmapped_items(child_a, map_a, cp1, cp2)
        self.check_unmapped_items(child_b, map_b, cp1, cp2)

        return child_a, child_b

    def check_unmapped_items(self, child, mapping, cp1, cp2):
        assert(cp1 < cp2)
        for i in range(len(child.permutation)):
            if i < cp1 or i > cp2:
                mapped = child.permutation[i]
                while(mapped in mapping):
                    mapped = mapping[mapped]
                child.permutation[i] = mapped
        return child
       
class Mutation:
    def mutate(self, solution):
        size = len(solution.permutation)

        mp1 = random.randrange(size)
        mp2 = random.randrange(size)
        while(mp2 == mp1):
            mp2 = random.randrange(size)
        solution.permutation[mp1], solution.permutation[mp2] = solution.permutation[mp2], solution.permutation[mp1]
        return solution

class BinaryTournament:
    def select(self, population):
        i = random.randrange(len(population))
        j = random.randrange(len(population))
        while i == j:
           j = random.randrange(len(population))
        
        a = population[i]
        b = population[j]
        if a.fitness < b.fitness:
            return a
        else: 
            return b

def ga(filename):
    num, dist = read_data(filename)

    population = []
    selection_op = BinaryTournament()
    crossover_op = Crossover()
    mutation_op = Mutation()
    
    pop_size = 200
    for i in range(pop_size):                      
        new_individual = Solution(np.random.permutation(range(num)))
        evaluate(new_individual)
        population.append(new_individual)
    
    current_best = Solution(np.random.permutation(range(num)))
    population = sorted(population, key=attrgetter('fitness'))
    
    generation = 0

    while evals < budget:
        nextgeneration = []
        nextgeneration.append(population[0])
        nextgeneration.append(population[pop_size - 1])
        
        while len(nextgeneration) < pop_size:
            parent_a = selection_op.select(population)
            parent_b = selection_op.select(population)
            child_a, child_b = crossover_op.pmx(parent_a, parent_b)
            if random.random() < 0.1:
                child_a = mutation_op.mutate(child_a)
            if random.random() < 0.1:
                child_b = mutation_op.mutate(child_b)
            
            evaluate(child_a)
            evaluate(child_b)

            nextgeneration.append(child_a)
            nextgeneration.append(child_b)
            # print child_a
            # print child_b
        population = sorted(nextgeneration, key=attrgetter('fitness'))
        best = population[0]
        # print generation, best.fitness, best.translate(coded_word)
        if best.fitness < current_best.fitness:
            current_best = best
            # print current_best_str
        print ",".join([str(generation), str(current_best.fitness)])
        generation += 1
    return best

if __name__ == '__main__':
    budget = 1000000
    sol = ga(sys.argv[1])
