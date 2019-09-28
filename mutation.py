import random

def neighbour(chromosome):
    """
    Returns a mutated chromosome. The mutation is done by searching for all classes that violate some hard constraint
    (with any resource) and randomly choosing one of them. Then, transfer that class in an unoccupied time frame, in
    one of the allowed classrooms for that class. If there exists no such combination of time frame and classroom,
    transfer the class into a random time frame in one of the allowed classrooms.
    :param chromosome: Current timetable
    :return: Mutated timetable
    """
    candidates = []
    for k in range(len(chromosome[0])):     # Search for all classes violating hard constraints
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
        i = random.choice(candidates)

    # Remove that class from its time frame and classroom
    for j in range(chromosome[0][i]['Zadato_vreme'], chromosome[0][i]['Zadato_vreme'] + int(chromosome[0][i]['Trajanje'])):
        chromosome[1][chromosome[0][i]['Nastavnik']][j] -= 1
        chromosome[2][chromosome[0][i]['Zadata_ucionica']][j] -= 1
        for group in chromosome[0][i]['Grupe']:
            chromosome[3][group][j] -= 1
    chromosome[4][chromosome[0][i]['Predmet']][chromosome[0][i]['Tip']].remove((chromosome[0][i]['Zadato_vreme'], chromosome[0][i]['Grupe']))

    # Find a free time and place
    length = int(chromosome[0][i]['Trajanje'])
    found = False
    pairs = []
    for classroom in chromosome[2]:
        c = 0
        # If class can't be held in this classroom
        if classroom not in chromosome[0][i]['Ucionica']:
            continue
        for k in range(len(chromosome[2][classroom])):
            if chromosome[2][classroom][k] == 0 and k % 12 + length <= 12:
                c += 1
                # If we found x consecutive hours where x is length of our class
                if c == length:
                    time = k + 1 - c
                    # Friday 8pm is reserved for free hour
                    if k != 59:
                        pairs.append((time, classroom))
                        found = True
                    c = 0
            else:
                c = 0
    # Find a random time
    if not found:
        classroom = random.choice(chromosome[0][i]['Ucionica'])
        day = random.randrange(0, 5)
        # Friday 8pm is reserved for free hour
        if day == 4:
            period = random.randrange(0, 12 - int(chromosome[0][i]['Trajanje']))
        else:
            period = random.randrange(0, 13 - int(chromosome[0][i]['Trajanje']))
        time = 12 * day + period

        chromosome[0][i]['Zadata_ucionica'] = classroom
        chromosome[0][i]['Zadato_vreme'] = time

    # Set that class to a new time and place
    if found:
        novo = random.choice(pairs)
        chromosome[0][i]['Zadata_ucionica'] = novo[1]
        chromosome[0][i]['Zadato_vreme'] = novo[0]

    for j in range(chromosome[0][i]['Zadato_vreme'], chromosome[0][i]['Zadato_vreme'] + int(chromosome[0][i]['Trajanje'])):
        chromosome[1][chromosome[0][i]['Nastavnik']][j] += 1
        chromosome[2][chromosome[0][i]['Zadata_ucionica']][j] += 1
        for group in chromosome[0][i]['Grupe']:
            chromosome[3][group][j] += 1
    chromosome[4][chromosome[0][i]['Predmet']][chromosome[0][i]['Tip']].append((chromosome[0][i]['Zadato_vreme'], chromosome[0][i]['Grupe']))

    return chromosome

def neighbour2(chromosome):
    """
    Returns a mutated chromosome. pick two classes at random and swap their places and assigned times. Besides this,
    check if the two classes are compatible for swapping (if they use the same type of classrooms).
    :param chromosome: Current timetable
    :return: Mutated timetable
    """
    first_index = random.randrange(0, len(chromosome[0]))

    first = chromosome[0][first_index]
    satisfied = False

    c = 0
    # Find two candidates that can be swapped (constraints are type of classroom and length, because of overlapping days)
    while not satisfied:
        # Return the same chromosome after 100 failed attempts
        if c == 100:
            return chromosome
        second_index = random.randrange(0, len(chromosome[0]))

        second = chromosome[0][second_index]
        if first['Zadata_ucionica'] in second['Ucionica'] and second['Zadata_ucionica'] in first['Ucionica']\
                and first['Zadato_vreme'] % 12 + int(second['Trajanje']) <= 12 \
                and second['Zadato_vreme'] % 12 + int(first['Trajanje']) <= 12:
            if first['Zadato_vreme'] + int(second['Trajanje']) != 60 and second['Zadato_vreme'] + int(first['Trajanje']) != 60\
                    and first != second:
                satisfied = True
        c += 1

    # Remove the two classes from their time frames and classrooms
    for j in range(first['Zadato_vreme'], first['Zadato_vreme'] + int(first['Trajanje'])):
        chromosome[1][first['Nastavnik']][j] -= 1
        chromosome[2][first['Zadata_ucionica']][j] -= 1
        for group in first['Grupe']:
            chromosome[3][group][j] -= 1
    chromosome[4][first['Predmet']][first['Tip']].remove((first['Zadato_vreme'], first['Grupe']))

    for j in range(second['Zadato_vreme'], second['Zadato_vreme'] + int(second['Trajanje'])):
        chromosome[1][second['Nastavnik']][j] -= 1
        chromosome[2][second['Zadata_ucionica']][j] -= 1
        for group in second['Grupe']:
            chromosome[3][group][j] -= 1
    chromosome[4][second['Predmet']][second['Tip']].remove((second['Zadato_vreme'], second['Grupe']))

    # Swap the times and classrooms
    tmp = first['Zadato_vreme']
    first['Zadato_vreme'] = second['Zadato_vreme']
    second['Zadato_vreme'] = tmp

    tmp_ucionica = first['Zadata_ucionica']
    first['Zadata_ucionica'] = second['Zadata_ucionica']
    second['Zadata_ucionica'] = tmp_ucionica

    # Set the classes to new timse and places
    for j in range(first['Zadato_vreme'], first['Zadato_vreme'] + int(first['Trajanje'])):
        chromosome[1][first['Nastavnik']][j] += 1
        chromosome[2][first['Zadata_ucionica']][j] += 1
        for group in first['Grupe']:
            chromosome[3][group][j] += 1
    chromosome[4][first['Predmet']][first['Tip']].append((first['Zadato_vreme'], first['Grupe']))

    for j in range(second['Zadato_vreme'], second['Zadato_vreme'] + int(second['Trajanje'])):
        chromosome[1][second['Nastavnik']][j] += 1
        chromosome[2][second['Zadata_ucionica']][j] += 1
        for group in second['Grupe']:
            chromosome[3][group][j] += 1
    chromosome[4][second['Predmet']][second['Tip']].append((second['Zadato_vreme'], second['Grupe']))

    return chromosome