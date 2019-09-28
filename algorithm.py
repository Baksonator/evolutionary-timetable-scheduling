import data as dt
import cost_functions
import mutation
from copy import deepcopy

max_generations = 5000
num_runs = 1
input_file = 'classes/input3.json'
output_file = 'classes/output3.json'
cost_function = cost_functions.cost
cost_function2 = cost_functions.cost2

def evolutionary_algorithm():
    best_timetable = None
    data = dt.load_data(input_file)
    neighbour = mutation.neighbour
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

        if best_timetable is None or cost_function2(chromosome) <= cost_function2(best_timetable):
            best_timetable = deepcopy(chromosome)

    chromosome = best_timetable

    neighbour2 = mutation.neighbour2

    for j in range(3 * max_generations):
        new_chromosome = neighbour2(deepcopy(chromosome))
        ft = cost_function2(chromosome)
        ftn = cost_function2(new_chromosome)
        if ftn <= ft:
            chromosome = new_chromosome
        if j % 200 == 0:
            print('Iteration', j, 'cost', cost_function2(chromosome))

    print('Run', 'cost', cost_function2(chromosome), 'chromosome', chromosome)

    dt.write_data(chromosome[0], output_file)

    professor_hard = True
    classroom_hard = True
    group_hard = True
    allowed_classrooms = True

    # Check hard constraints
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

    # Check preferred order statistics
    subjects_cost = 0
    for single_class in chromosome[4]:
        subject_cost = 0
        for lab in chromosome[4][single_class]['L']:
            for practice in chromosome[4][single_class]['V']:
                for grupa in lab[1]:
                    if grupa in practice[1] and lab[0] < practice[0]:
                        subject_cost += 1
            for lecture in chromosome[4][single_class]['P']:
                for grupa in lab[1]:
                    if grupa in lecture[1] and lab[0] < lecture[0]:
                        subject_cost += 1
        for practice in chromosome[4][single_class]['V']:
            for lecture in chromosome[4][single_class]['P']:
                for grupa in practice[1]:
                    if grupa in lecture[1] and practice[0] < lecture[0]:
                        subject_cost += 1
        subjects_cost += subject_cost
        print('Subject cost for subject', single_class, 'is:', subject_cost)
    print('Total subject cost:', subjects_cost)

    # Check group statistics
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

    # Check professor statistics
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