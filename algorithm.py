import data as dt
import random
from copy import deepcopy

def cost(chromosome):
    prof_cost = 0
    classrooms_cost = 0
    groups_cost = 0
    subjects_cost = 0

    for single_class in chromosome[0]:
        time = single_class['Zadato_vreme']
        class_len = single_class['Trajanje']

        for i in range(time, time + int(class_len)):
            if chromosome[1][single_class['Nastavnik']][i] > 1:
                prof_cost += 1
            if chromosome[2][single_class['Zadata_ucionica']][i] > 1:
                classrooms_cost += 1
            for group in single_class['Grupe']:
                if chromosome[3][group][i] > 1:
                    groups_cost += 1

    for single_class in chromosome[4]:
        for lab in chromosome[4][single_class]['L']:
            for practice in chromosome[4][single_class]['V']:
                if lab < practice:
                    subjects_cost += 0.01
            for lecture in chromosome[4][single_class]['P']:
                if lab < lecture:
                    subjects_cost += 0.01
        for practice in chromosome[4][single_class]['V']:
            for lecture in chromosome[4][single_class]['P']:
                if practice < lecture:
                    subjects_cost += 0.01

    return prof_cost + classrooms_cost + groups_cost + round(subjects_cost, 2)

def cost2(chromosome):
    groups_empty = 0
    prof_empty = 0
    load_groups = 0
    load_prof = 0

    original_cost = cost(chromosome)

    for group in chromosome[3]:
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(12):
                time = day * 12 + hour
                if chromosome[3][group][time] >= 1:
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        groups_empty += (time - last_seen - 1) / 500
                    last_seen = time
            if current_load > 6:
                load_groups += 0.005

    for prof in chromosome[1]:
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(12):
                time = day * 12 + hour
                if chromosome[1][prof][time] >= 1:
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        prof_empty += (time - last_seen - 1) / 2000
                    last_seen = time
            if current_load > 6:
                load_prof += 0.0025

    return original_cost + round(groups_empty, 3) + round(prof_empty, 5) + round(load_prof, 3) + round(load_groups, 4)

max_generations = 5000
num_runs = 5
input_file = 'classes/ulaz3.json'
output_file = 'classes/izlaz3.json'
cost_function = cost
cost_function2 = cost2

def neighbour(chromosome):
    candidates = []
    for k in range(len(chromosome[0])):
        for j in range(len(chromosome[2][chromosome[0][k]['Zadata_ucionica']])):
            if chromosome[2][chromosome[0][k]['Zadata_ucionica']][j] >= 2:
                candidates.append(k)
        for j in range(len(chromosome[1][chromosome[0][k]['Nastavnik']])):
            if chromosome[1][chromosome[0][k]['Nastavnik']][j] >= 2:
                candidates.append(k)
        for group in chromosome[0][k]['Grupe']:
            for j in range(len(chromosome[3][group])):
                if chromosome[3][group][j] >= 2:
                    candidates.append(k)

    if not candidates:
        i = random.randrange(len(chromosome[0]))
    else:
        # i = sorted(candidates)
        i = random.choice(candidates)

    for j in range(chromosome[0][i]['Zadato_vreme'], chromosome[0][i]['Zadato_vreme'] + int(chromosome[0][i]['Trajanje'])):
        chromosome[1][chromosome[0][i]['Nastavnik']][j] -= 1
        chromosome[2][chromosome[0][i]['Zadata_ucionica']][j] -= 1
        for group in chromosome[0][i]['Grupe']:
            chromosome[3][group][j] -= 1
    chromosome[4][chromosome[0][i]['Predmet']][chromosome[0][i]['Tip']].remove(chromosome[0][i]['Zadato_vreme'])

    trajanje = int(chromosome[0][i]['Trajanje'])
    found = False
    pairs = []
    for ucionica in chromosome[2]:
        c = 0
        if ucionica not in chromosome[0][i]['Ucionica']:
            continue
        for k in range(len(chromosome[2][ucionica])):
            if chromosome[2][ucionica][k] == 0 and k % 12 + trajanje <= 12:
                c += 1
                if c == trajanje:
                    time = k + 1 - c
                    if k != 59:
                        pairs.append((time, ucionica))
                        found = True
                    c = 0
            else:
                c = 0
    if not found:
        classroom = random.choice(chromosome[0][i]['Ucionica'])
        day = random.randrange(0, 5)
        if day == 4:
            period = random.randrange(0, 12 - int(chromosome[0][i]['Trajanje']))
        else:
            period = random.randrange(0, 13 - int(chromosome[0][i]['Trajanje']))
        time = 12 * day + period

        chromosome[0][i]['Zadata_ucionica'] = classroom
        chromosome[0][i]['Zadato_vreme'] = time

    if found:
        novo = random.choice(pairs)
        chromosome[0][i]['Zadata_ucionica'] = novo[1]
        chromosome[0][i]['Zadato_vreme'] = novo[0]

    for j in range(chromosome[0][i]['Zadato_vreme'], chromosome[0][i]['Zadato_vreme'] + int(chromosome[0][i]['Trajanje'])):
        chromosome[1][chromosome[0][i]['Nastavnik']][j] += 1
        chromosome[2][chromosome[0][i]['Zadata_ucionica']][j] += 1
        for group in chromosome[0][i]['Grupe']:
            chromosome[3][group][j] += 1
    chromosome[4][chromosome[0][i]['Predmet']][chromosome[0][i]['Tip']].append(chromosome[0][i]['Zadato_vreme'])

    return chromosome

def neighbour2(chromosome):
    first_index = random.randrange(0, len(chromosome[0]))

    first = chromosome[0][first_index]
    satisfied = False

    c = 0
    while not satisfied:
        if c == 100:
            return chromosome
        second_index = random.randrange(0, len(chromosome[0]))

        second = chromosome[0][second_index]
        if first['Zadata_ucionica'] in second['Ucionica'] and second['Zadata_ucionica'] in first['Ucionica']\
                and first['Zadato_vreme'] % 12 + int(second['Trajanje']) <= 12 \
                and second['Zadato_vreme'] % 12 + int(first['Trajanje']) <= 12:
            if first['Zadato_vreme'] + int(second['Trajanje']) != 60 and second['Zadato_vreme'] + int(first['Trajanje']) != 60:
                satisfied = True
        c += 1

    for j in range(first['Zadato_vreme'], first['Zadato_vreme'] + int(first['Trajanje'])):
        chromosome[1][first['Nastavnik']][j] -= 1
        chromosome[2][first['Zadata_ucionica']][j] -= 1
        for group in first['Grupe']:
            chromosome[3][group][j] -= 1
    chromosome[4][first['Predmet']][first['Tip']].remove(first['Zadato_vreme'])

    for j in range(second['Zadato_vreme'], second['Zadato_vreme'] + int(second['Trajanje'])):
        chromosome[1][second['Nastavnik']][j] -= 1
        chromosome[2][second['Zadata_ucionica']][j] -= 1
        for group in second['Grupe']:
            chromosome[3][group][j] -= 1
    chromosome[4][second['Predmet']][second['Tip']].remove(second['Zadato_vreme'])

    tmp = first['Zadato_vreme']
    first['Zadato_vreme'] = second['Zadato_vreme']
    second['Zadato_vreme'] = tmp

    tmp_ucionica = first['Zadata_ucionica']
    first['Zadata_ucionica'] = second['Zadata_ucionica']
    second['Zadata_ucionica'] = tmp_ucionica

    for j in range(first['Zadato_vreme'], first['Zadato_vreme'] + int(first['Trajanje'])):
        chromosome[1][first['Nastavnik']][j] += 1
        chromosome[2][first['Zadata_ucionica']][j] += 1
        for group in first['Grupe']:
            chromosome[3][group][j] += 1
    chromosome[4][first['Predmet']][first['Tip']].append(first['Zadato_vreme'])

    for j in range(second['Zadato_vreme'], second['Zadato_vreme'] + int(second['Trajanje'])):
        chromosome[1][second['Nastavnik']][j] += 1
        chromosome[2][second['Zadata_ucionica']][j] += 1
        for group in second['Grupe']:
            chromosome[3][group][j] += 1
    chromosome[4][second['Predmet']][second['Tip']].append(second['Zadato_vreme'])

    return chromosome

def evolutionary_algorithm():
    best_timetable = None
    data = dt.load_data(input_file)
    for i in range(num_runs):
        chromosome = dt.generate_chromosome(data)

        for j in range(max_generations):
            new_chromosome = neighbour(deepcopy(chromosome))
            ft = cost_function(chromosome)
            if ft == 0:
                break
            ftn = cost_function(new_chromosome)
            if ftn <= ft:
                chromosome = new_chromosome
            if j % 200 == 0:
                print('Iteration', j, 'cost', cost_function(chromosome))

        print('Run', i + 1, 'cost', cost_function(chromosome), 'chromosome', chromosome)

        if best_timetable is None or cost_function(chromosome) <= cost_function(best_timetable):
            best_timetable = deepcopy(chromosome)

    chromosome = best_timetable

    for j in range(3 * max_generations):
        new_chromosome = neighbour(deepcopy(chromosome))
        ft = cost_function2(chromosome)
        ftn = cost_function2(new_chromosome)
        if ftn <= ft:
            chromosome = new_chromosome
        if j % 200 == 0:
            print('Iteration', j, 'cost', cost_function2(chromosome))

    print('Run', 1, 'cost', cost_function2(chromosome), 'chromosome', chromosome)

    dt.write_data(chromosome[0], output_file)

    professor_hard = True
    classroom_hard = True
    group_hard = True
    allowed_classrooms = True

    for single_class in chromosome[0]:
        if single_class['Zadata_ucionica'] not in single_class['Ucionica']:
            allowed_classrooms = False
    for profesor in chromosome[1]:
        for i in range(len(chromosome[1][profesor])):
            if chromosome[1][profesor][i] > 1:
                professor_hard = False
    for ucionica in chromosome[2]:
        for i in range(len(chromosome[2][ucionica])):
            if chromosome[2][ucionica][i] > 1:
                classroom_hard = False
    for grupa in chromosome[3]:
        for i in range(len(chromosome[3][grupa])):
            if chromosome[3][grupa][i] > 1:
                group_hard = False

    print('Are hard restrictions for professors satisfied:', professor_hard)
    print('Are hard restrictions for classrooms satisfied:', classroom_hard)
    print('Are hard restrictions for groups satisfied:', group_hard)
    print('Are hard restrictions for allowed classrooms satisfied:', allowed_classrooms)

    subjects_cost = 0
    for single_class in chromosome[4]:
        subject_cost = 0
        for lab in chromosome[4][single_class]['L']:
            for practice in chromosome[4][single_class]['V']:
                if lab < practice:
                    subject_cost += 1
            for lecture in chromosome[4][single_class]['P']:
                if lab < lecture:
                    subject_cost += 1
        for practice in chromosome[4][single_class]['V']:
            for lecture in chromosome[4][single_class]['P']:
                if practice < lecture:
                    subject_cost += 1
        subjects_cost += subject_cost
        print('Subject cost for subject', single_class, 'is:', subject_cost)
    print('Total subject cost:', subjects_cost)

    total_group_cost = 0
    total_group_load = 0
    max_group_cost = 0
    for group in chromosome[3]:
        group_cost = 0
        group_load = 0
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(12):
                time = day * 12 + hour
                if chromosome[3][group][time] >= 1:
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        group_cost += (time - last_seen - 1)
                    last_seen = time
            if current_load > 6:
                group_load += 1
        print('Group cost for group', group, 'is:', group_cost, ', number of hard days:', group_load)
        if max_group_cost < group_cost:
            max_group_cost = group_cost
        total_group_cost += group_cost
        total_group_load += group_load
    print('Maximum group cost is:', max_group_cost)
    print('Average group cost is:', total_group_cost / len(chromosome[3]))
    print('Total group load is:', total_group_load)

    total_prof_cost = 0
    total_prof_load = 0
    free_hour = True
    max_prof_cost = 0
    for prof in chromosome[1]:
        prof_cost = 0
        prof_load = 0
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(12):
                time = day * 12 + hour
                if chromosome[1][prof][time] >= 1:
                    if time == 59:
                        free_hour = False
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        prof_cost += (time - last_seen - 1)
                    last_seen = time
            if current_load > 6:
                prof_load += 1
        print('Prof cost for prof', prof, 'is:', prof_cost, ', number of hard days:', prof_load)
        if max_prof_cost < prof_cost:
            max_prof_cost = prof_cost
        total_prof_cost += prof_cost
        total_prof_load += prof_load
    print('Max prof cost is:', max_prof_cost)
    print('Average prof cost is:', total_prof_cost / len(chromosome[1]))
    print('Total prof load is:', total_prof_load)
    print('Free hour:', free_hour, ', 59')

evolutionary_algorithm()