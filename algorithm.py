import data as dt
import random

def cost(chromosome):
    prof_cost = 0
    classrooms_cost = 0
    groups_cost = 0
    subjects_cost = 0
    for prof in chromosome[1]:
        prof_cost += sum(i > 1 for i in chromosome[1][prof])

    for classroom in chromosome[2]:
        classrooms_cost += sum(i > 1 for i in chromosome[2][classroom])

    for group in chromosome[3]:
        groups_cost += sum(i > 1 for i in chromosome[3][group])

    return (prof_cost + classrooms_cost + groups_cost)

def tournament_selection(cost_f, population, size):
    z = []
    while len(z) < size:
        z.append(random.choice(population))
    best = None
    best_f = None
    for e in z:
        ff = cost_f(e)
        if best is None or ff < best_f:
            best_f = ff
            best = e
    return best

def uniform_crossover(c1, c2):
    c3_class = []
    c4_class = []

    c3_professors = {}
    c3_classrooms = {}
    c3_groups = {}
    c3_subjects = {}

    c4_professors = {}
    c4_classrooms = {}
    c4_groups = {}
    c4_subjects = {}

    for single_class in c1[0]:
        c3_professors[single_class['Nastavnik']] = [0] * 60
        for classroom in single_class['Ucionica']:
            c3_classrooms[classroom] = [0] * 60
        for group in single_class['Grupe']:
            c3_groups[group] = [0] * 60
        c3_subjects[single_class['Predmet']] = {'P': -1, 'V': -1, 'L': -1}

    for single_class in c2[0]:
        c4_professors[single_class['Nastavnik']] = [0] * 60
        for classroom in single_class['Ucionica']:
            c4_classrooms[classroom] = [0] * 60
        for group in single_class['Grupe']:
            c4_groups[group] = [0] * 60
        c4_subjects[single_class['Predmet']] = {'P': -1, 'V': -1, 'L': -1}

    for i in range(len(c1[0])):
        if random.random() > 0.5:
            c3_class.append(c1[0][i].copy())
            c4_class.append(c2[0][i].copy())

            for j in range(c1[0][i]['Zadato_vreme'], c1[0][i]['Zadato_vreme'] + int(c1[0][i]['Trajanje'])):
                c3_professors[c1[0][i]['Nastavnik']][j] += 1
                c3_classrooms[classroom][j] += 1
                for group in c1[0][i]['Grupe']:
                    c3_groups[group][j] += 1
                c3_subjects[c1[0][i]['Predmet']][c1[0][i]['Tip']] = c1[0][i]['Zadato_vreme']

            for j in range(c2[0][i]['Zadato_vreme'], c2[0][i]['Zadato_vreme'] + int(c2[0][i]['Trajanje'])):
                c4_professors[c2[0][i]['Nastavnik']][j] += 1
                c4_classrooms[classroom][j] += 1
                for group in c2[0][i]['Grupe']:
                    c4_groups[group][j] += 1
                c4_subjects[c2[0][i]['Predmet']][c2[0][i]['Tip']] = c2[0][i]['Zadato_vreme']
        else:
            c3_class.append(c2[0][i].copy())
            c4_class.append(c1[0][i].copy())

            for j in range(c1[0][i]['Zadato_vreme'], c1[0][i]['Zadato_vreme'] + int(c1[0][i]['Trajanje'])):
                c4_professors[c1[0][i]['Nastavnik']][j] += 1
                c4_classrooms[classroom][j] += 1
                for group in c1[0][i]['Grupe']:
                    c4_groups[group][j] += 1
                c4_subjects[c1[0][i]['Predmet']][c1[0][i]['Tip']] = c1[0][i]['Zadato_vreme']

            for j in range(c2[0][i]['Zadato_vreme'], c2[0][i]['Zadato_vreme'] + int(c2[0][i]['Trajanje'])):
                c3_professors[c2[0][i]['Nastavnik']][j] += 1
                c3_classrooms[classroom][j] += 1
                for group in c2[0][i]['Grupe']:
                    c3_groups[group][j] += 1
                c3_subjects[c2[0][i]['Predmet']][c2[0][i]['Tip']] = c2[0][i]['Zadato_vreme']

    return (c3_class, c3_professors, c3_classrooms, c3_groups, c3_subjects), (c4_class, c4_professors, c4_classrooms, c4_groups, c4_subjects)

def mutate(chromosome, probability):
    if random.random() <= probability:
        # nb_change = random.randrange(len(chromosome[0]) // 2)
        indices_change = random.sample(range(len(chromosome[0])), 3)

        for i in indices_change:

            for j in range(chromosome[0][i]['Zadato_vreme'], chromosome[0][i]['Zadato_vreme'] + int(chromosome[0][i]['Trajanje'])):
                chromosome[1][chromosome[0][i]['Nastavnik']][j] -= 1
                chromosome[2][chromosome[0][i]['Zadata_ucionica']][j] -= 1
                for group in chromosome[0][i]['Grupe']:
                    chromosome[3][group][j] -= 1
                chromosome[4][chromosome[0][i]['Predmet']][chromosome[0][i]['Tip']] = -1

            classroom = random.choice(chromosome[0][i]['Ucionica'])
            day = random.randrange(0, 5)
            period = random.randrange(0, 13 - int(chromosome[0][i]['Trajanje']))
            time = 12 * day + period

            chromosome[0][i]['Zadata_ucionica'] = classroom
            chromosome[0][i]['Zadato_vreme'] = time

            for j in range(chromosome[0][i]['Zadato_vreme'], chromosome[0][i]['Zadato_vreme'] + int(chromosome[0][i]['Trajanje'])):
                chromosome[1][chromosome[0][i]['Nastavnik']][j] += 1
                chromosome[2][chromosome[0][i]['Zadata_ucionica']][j] += 1
                for group in chromosome[0][i]['Grupe']:
                    chromosome[3][group][j] += 1
                chromosome[4][chromosome[0][i]['Predmet']][chromosome[0][i]['Tip']] = time

max_generations = 500
mut_rate = 0.5
population_size = 100
child_pool_size = 50
num_runs = 1
input_file = 'classes/ulaz1.json'
cost_function = cost
crossover_selection = tournament_selection

# data = dt.load_data(input_file)
# population = dt.generate_population(data, population_size)
# for chromosome in population:
#     print(cost(chromosome))
# print("Prvi", population[0])
# print("Drugi", population[1])
# c3, c4 = uniform_crossover(population[0], population[1])
# print("Dete1", c3)
# print("Dete2", c4)
# mutate(population[0], mut_rate)
# print("Mutiran", population[0])

def timetable():
    best_ever_sol = None
    best_ever_f = None
    for k in range(num_runs):
        print('Starting GA', k + 1, ', population size: ', population_size, ', maximum generations: ', max_generations,
              ', mutation rate:', mut_rate, ', number of runs:', num_runs)
        best = None
        best_f = None
        t = 0
        data = dt.load_data(input_file)
        population = dt.generate_population(data, population_size)
        while t < max_generations:
            new_population = population[:]
            while len(new_population) < population_size + child_pool_size:
                c1 = crossover_selection(cost_function, population, 3)
                c2 = crossover_selection(cost_function, population, 3)
                c3, c4 = uniform_crossover(c1, c2)
                mutate(c3, mut_rate)
                mutate(c4, mut_rate)
                new_population.append(c3)
                new_population.append(c4)
            population = sorted(new_population, key=lambda l: cost_function(l))[:population_size]
            f = cost_function(population[0])
            average_f = sum(map(cost_function, population)) / population_size
            print('Iteration:', t + 1, ', best solution: ', f, ', average cost:', average_f)
            t += 1
            if best_f is None or best_f > f:
                best_f = f
                best = population[0]
        if best_ever_f is None or best_ever_f > best_f:
            best_ever_f = best_f
            best_ever_sol = best
        print('Best solution in run:', k + 1, ', composition of best chromosome:', best, ', best cost:', best_f)
    print(best_ever_sol)
    print(best_f)

timetable()