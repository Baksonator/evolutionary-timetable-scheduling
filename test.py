import json

with open('classes/ulaz1.json', 'r') as read_file:
    data = json.load(read_file)

c = 0
for university_class in data['Casovi']:
    classroom = university_class['Ucionica']
    university_class['Ucionica'] = data['Ucionice'][classroom]
    if university_class['Trajanje'] == '3':
        c += 1

data = data['Casovi']
print(type(data))
print(c)