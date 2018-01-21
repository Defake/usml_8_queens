# -*- coding: utf-8 -*-

from functools import reduce
import random

### Chess Logic ###

def empty_board():
    return [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]

def fields_attacked_by_queen(queen_coords):
    fields = []
    # horizontal fields
    for i in range(8): fields.append([i, queen_coords[1]])
    # vertical fields
    for i in range(8): fields.append([queen_coords[0], i])
    # ascending diagonal
    x = max(0, queen_coords[0] - queen_coords[1])
    y = max(0, queen_coords[1] - queen_coords[0])
    while x < 8 and y < 8:
        fields.append([x, y])
        x += 1
        y += 1
    # descending diagonal
    x = max(0, queen_coords[0] - (7 - queen_coords[1]))
    y = min(7, queen_coords[0] + queen_coords[1])
    while x < 8 and y >= 0:
        fields.append([x, y])
        x += 1
        y -= 1
    return fields

def apply_attacked_fields(board, fields):
    for f in fields:
        board[f[0]][f[1]] = 1
    return board

def attacked_board(queen_coords):
    return apply_attacked_fields(empty_board(), fields_attacked_by_queen(queen_coords))

def index_to_coord(index):
    return [index // 8, index % 8]

def func_add_cord(coords, index):
    coords.append(index_to_coord(index))
    return coords

def inline_board_to_coords(fields_list):
    return reduce(lambda coords, i: func_add_cord(coords, i) if fields_list[i] == 1 else coords,
                  range(len(fields_list)), [])

def checks_count(inline_board):
    queens_coords = inline_board_to_coords(inline_board)
    checks = 0
    while len(queens_coords) > 1:
        q = queens_coords.pop()
        board = attacked_board(q)
        for q2 in queens_coords:
            if board[q2[0]][q2[1]] == 1:
                checks += 1
    return checks

def get_visualization(inline_board):
    coords = inline_board_to_coords(inline_board)
    board = []
    for row in range(8):
        board.append([])
        for i in range(8):
            board[row].append('+')
    for q in coords:
        board[q[0]][q[1]] = 'Q'
    vis = ""
    for row in board:
        for cell in row:
            vis += cell
        vis += "\n"
    return vis

### genetic algo ###

def chromosome_score(chromosome):
    checks_err = checks_count(chromosome)
    missing_queens_err = max(0, 8 - sum(chromosome))
    return 1 / (checks_err + missing_queens_err + 1)

def overall_score(individuals):
    return reduce(lambda score, ind: score + ind[1], individuals, 0)

def scored_individuals(chromosomes):
    return reduce(lambda ix, i: ix + [[i, chromosome_score(i)]], chromosomes, [])

def select_parent(individuals, overall_score):
    rand = random.random() * overall_score
    i = 0
    score = 0
    while True:
        if score <= rand < score + individuals[i][1]:
            return list(individuals[i])
        else:
            score += individuals[i][1]

def select_parents(individuals):
    overall = overall_score(individuals)
    return reduce(lambda parents, _: parents + [select_parent(individuals, overall)],
                  individuals, [])

def create_chromosomes(size):
    return reduce(lambda ix, i: ix + [[random.randint(0, 1) for i in range(64)]], range(size), [])

def create_population(size):
    return scored_individuals(create_chromosomes(size))

def get_best(individuals):
    individuals.sort(key=(lambda x: x[1]), reverse=True)
    return individuals[0]

class Solver_8_queens:

    def __init__(self, pop_size=150, cross_prob=0.6, mut_prob=0.3):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

    def solve(self, min_fitness=1.0, max_epochs=2000):
        pop = create_population(self.pop_size)
        generation_n = 1
        while True:
            best = get_best(pop)
            if (max_epochs and generation_n >= max_epochs) \
               or (min_fitness and best[1] >= min_fitness):
                break
            pop = self.evolve(pop)
            generation_n += 1
        best_fit = best[1]
        epoch_num = generation_n
        visualization = get_visualization(best[0])
        return best_fit, epoch_num, visualization

    def evolve(self, individuals):
        parents = select_parents(individuals)
        new_gen = self.new_generation(parents)
        #best_ind = get_best(individuals)
        return scored_individuals(new_gen)# + [best_ind[0]])

    def mutate(self, chromosome):
        if random.random() < self.mut_prob:
            i = random.randint(0, len(chromosome) - 1)
            chromosome[i] = (1 if chromosome[i] == 0 else 0)
        return chromosome

    def new_childs(self, parent1, parent2):
        if random.random() < self.cross_prob:
            border = random.randint(1, len(parent1[0]) - 1)
            child1 = parent1[0][:border] + parent2[0][border:]
            child2 = parent2[0][:border] + parent1[0][border:]
        else:
            child1 = parent1[0]
            child2 = parent2[0]
        return [self.mutate(list(child1)), self.mutate(list(child2))]

    def new_generation(self, parents):
        """parents - individuals, but returns pure chromosomes without score."""
        halflen = len(parents) // 2
        p1, p2 = parents[:halflen], parents[halflen:]
        return reduce(lambda g, i: g + self.new_childs(p1[i], p2[i]), range(halflen), [])
