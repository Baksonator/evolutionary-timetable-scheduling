import json
import random

def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    # c = 0
    new_data = []

    for university_class in data['Casovi']:
        classroom = university_class['Ucionica']
        # if classroom == 'r':
        #     c += int(university_class['Trajanje'])
        university_class['Ucionica'] = data['Ucionice'][classroom]
            # new_data.append(university_class)


    # print(c)
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
        subjects[single_class['Predmet']] = {'P' : [], 'V' : [], 'L' : []}

    for single_class in data:
        new_single_class = single_class.copy()

        classroom = random.choice(single_class['Ucionica'])
        day = random.randrange(0, 5)
        if day == 4:
            period = random.randrange(0, 12 - int(single_class['Trajanje']))
        else:
            period = random.randrange(0, 13 - int(single_class['Trajanje']))
        new_single_class['Zadata_ucionica'] = classroom
        time = 12 * day + period
        new_single_class['Zadato_vreme'] = time

        for i in range(time, time + int(single_class['Trajanje'])):
            professors[new_single_class['Nastavnik']][i] += 1
            classrooms[classroom][i] += 1
            for group in new_single_class['Grupe']:
                groups[group][i] += 1
        subjects[new_single_class['Predmet']][new_single_class['Tip']].append(time)

        new_data.append(new_single_class)

    return (new_data, professors, classrooms, groups, subjects)

def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)