import json
import random

def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    for university_class in data['Casovi']:
        classroom = university_class['Ucionica']
        university_class['Ucionica'] = data['Ucionice'][classroom]

    data = data['Casovi']

    return data

def generate_chromosome(data):
    professors = {}
    classrooms = {}
    groups = {}
    subjects = {}

    new_data = []

    for single_class in data:
        professors[single_class['Nastavnik']] = [0] * 60
        for classroom in single_class['Ucionica']:
            classrooms[classroom] = [0] * 60
        for group in single_class['Grupe']:
            groups[group] = [0] * 60
        subjects[single_class['Predmet']] = {'P' : -1, 'V' : -1, 'L' : -1}

    for single_class in data:
        new_single_class = single_class.copy()

        classroom = random.choice(single_class['Ucionica'])
        day = random.randrange(0, 5)
        period = random.randrange(0, 13 - int(single_class['Trajanje']))
        new_single_class['Zadata_ucionica'] = classroom
        time = 12 * day + period
        new_single_class['Zadato_vreme'] = time

        for i in range(time, time + int(single_class['Trajanje'])):
            professors[new_single_class['Nastavnik']][i] += 1
            classrooms[classroom][i] += 1
            for group in new_single_class['Grupe']:
                groups[group][i] += 1
            subjects[new_single_class['Predmet']][new_single_class['Tip']] = time

        new_data.append(new_single_class)

    return (new_data, professors, classrooms, groups, subjects)

# data = load_data('classes/ulaz1.json')
# print(data)
# (chromosome, professors, classrooms, groups, subjects) = generate_chromosome(data)
# x = generate_chromosome(data)
# x = generate_population(data, 100)
# print(x)
# print(x[1])
# print(x[2])
# print(x[3])
# print(x[4])

def generate_population(data, pop_size):
    population = []
    for i in range(pop_size):
        chromosome = generate_chromosome(data)
        population.append(chromosome)
    return population

# x = generate_population(data, 3)
# for i in range(3):
#     print(x[i])