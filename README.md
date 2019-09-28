# Evolutionary timetable scheduling

## Abstract

This project covers methods used for solving the timetable scheduling problem specific for timetable formats at the *Faculty of Computing, Belgrade*. The algorithms described represent a hybrid approach combining a 1+1 evolutionary strategy with shotgun hill-climbing. Apart from these, methods that were and taken into account and tested are simulated annealing and a classical genetic algorithm. However, the last two techniques have not yielded results as good as the forementioned ones.

## Problem description

The problem discussed is an NP-hard problem of generating a valid and highly optimal timetable for the *Faculty of Computing, Belgrade*. By valid we mean that there are no conflicts in the timetable, i.e. no two classes are in the same classroom at the same time, nor can a professor hold two classes at the same time, etc. 
Next, we describe the specific timetable format we will be analyzing. Classes are defined in the following fashion:
- Subject that is being taught
- Type of class (lectures or practicals)
- The professor conducting the class
- All of the student groups listening to the class toghether at the same time
- Classroom type allowed (i.e. some classrooms require students to have access to computers, some do not)
- Length (1 to 4 hours)
We assume that all classrooms are of the same size and have the required capacity. Valid hours for holding classes are from 9am to 9pm. The task at hand is to assign a time and classroom for each of the classes given in the mentioned format.

## Constraints

1. Resources must not overlap in time:
   - No professor can hold two classes at the same time
   - No student group can attend two classes at the same time
   - No classroom can host to classes at the same time
   - **Note**: the term "same time" does not only mean the starting time of a class, but what also must be taken into account is the length of a class. If a resources is taken at time *T<sub>1</sub>* and the class lasts for *t*, then the resource can be taken again only at time *T<sub>2</sub>*.
2. The class must be held in one of the allowed classrooms for it (most practicals require computers)
3. If a subject has multiple forms of classes, such as lectures, practicals and labs, the preferred order is: lecture, practical, lab.

Constraints 1 and 2 must be met (hard constraints), while constraint 3 is a "soft" constraint and can be violated.

Additional possible criteria for the assessment of the solution:
- Minimize total idleness for each group (pauses between classes)
- Minimize total idleness for each professor (pauses between classes)
- Provide one free hour a week with no classes, for a professors union meeting
- Minimize daily load for professors and groups (less than 6 hours of class a day)

## Solution

Since we are using a 1+1 evolutionary strategy with shotgun hill-climbing, there is only one chromosome which represents a timetable (which can be either valid or not). The timetable is represented in a similar way as is the input data, with the only changes being that each class in the timetable has a list of acceptable classrooms instead of a type of classroom, and each class has an assigned classroom and assigned time (a number from 0 to 59, where 0 is 9am on Monday, and 59 is 8pm on Friday). Additionally, each timetable will have a dictionary of professors, classrooms, groups and subjects, where each entry in the dictionary will be an array of integers of the size of 60 (5 days x 12 possible hours for a class), where each element of the array represents the load of that resource in that hour (i.e. for a professor, the first element represents how many classes that professor is scheduled to hold at 9am on Monday in that timetable). These data structures are used for efficiently calculating the cost function. Ideally, we want all the elements in all of these array to be either 0 or 1 (2 or more indicates a conflict for that resource). When we find a feasbile solution, only the first part of the chromosome will be saved to a file, since we do not need the additional dictionaries for representing the timetable.

It is worth mentioning that for simplicity, the dictionary used has keys that are in Serbian, since the input file is a JSON file in Serbian. You can find the translations for all the relevant words here:
- Predmet = Subject
- Tip = Type
- Nastavnik = Professor
- Grupe = Groups
- Ucionica = Classroom (allowed classrooms)
- Trajanje = Length
- Zadata ucionica = Assigned classroom
- Zadato vreme = Assigned time

## Algorithm

The algorithm is comprised in the following way:

1. **Loading and processing the data**  
   Load all the data from the input file and process it so that each class in the timetable has a list of acceptable classrooms instead    of a type of classroom.
2. **1+1 evolutionary strategy with shotgun hill-climbing (hard constraints)**  
   This is the phase of the algorithm were we generate an arbitrary number of schedules that try to optimize for hard constraints, hence this is shotgun hill-climbing. They way we do this for each of these schedules is: Firstly, we generate a completely random timetable. Then, we use the 1+1 evolutionary strategy to improve out solution. The way in which find a neighboring solution (one that we compare with the current one) is by using a mutation operator. As part of the mutation, we search for all classes that violate some hard constraint (with any resource) and we randomly choose one of them. Then we transfer that class in an unoccupied time frame, in one of the allowed classrooms for that class. If there exists no such combination of time frame and classroom, we transfer the class into a random time frame in one of the allowed classrooms. Also, we are careful of not accidentally placing a class to overlap days (start Monday evening, finish Tuesday morning) which is possible since we are representing the whole week as an array. If there are no more classes that violate hard constraints, we choose a random one and transfer it to an unoccupied time frame (in this phase we also optimize for the soft constraint of preferred order). Of all of the timetables we get by shotgun hill-climbing (recommended number is 5) we choose the best one (the one with the lowest cost function) to propagate to the next phase. Also, the recommended number of iterations for the 1+1 evolutionary strategy is 5000.
3. **1+1 evolutionary strategy (soft constraints)**  
   In this phase we optimize for soft constraints only, but we are wary of not violating any hard constraints in the process. The way we do this is similar as in the previous step. We run 15000 iterations of 1+1 evolutionary strategy on the previously obtained timetable. The difference compared to the previous step is that we use a different cost function (which takes into account all of the soft constraints, as well as the hard ones). Furthermore, we mutate the chromosome in a different way: We pick two classes at random and swap their places and assigned times. Besides this, we check if the two classes are compatible for swapping (if they use the same type of classrooms). After 15000 iterations, we assert that the algorithm has converged and we have our solution.
4. **Saving the solution and displaying statistics**  
   In the final step, we save the obtained schedule in a JSON file and we display all the relevant metrics regarding our solution. We also show metrics individually for all subjects, groups and professors.
   
## Testing and results

All the parameters used are purely empirical and not guaranteed to be the best for every possible problem.

The algorithm was tested on 3 different timetables (input1.json, input2.json, input3.json).

The metrics are displayed in the following table.

| | *input1.json* | *input2.json* | *input3.json* |
| --- | --- | --- | --- |
| Number of runs | 5 | 5 | 5 |
| Hard constraints satisfied | Yes | Yes | Yes |
| Maximum idleness for a group | 2 | 6 | 6 |
| Average idleness for a group | 0.25 | 0.7 | 1.14 |
| Days with more than 6 hours of class for a group | 0 | 7 | 6 |
| Maximum idleness for a professor | 0 | 7 | 6 |
| Average idleness for a professor | 0 | 0.3 | 0.54 |
| Days with more than 6 hours of class for a professor | 0 | 0 | 1 |
| Number of time that preferred order is not satisfied | 0 | 7 | 24 |
| Free hour | Friday 8pm | Friday 8pm | Friday 8pm |

## Running the scheduler

You can run the program by running the script `algorithm.py`. The parameters, including the input and output files, can be set in that script.
