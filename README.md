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
