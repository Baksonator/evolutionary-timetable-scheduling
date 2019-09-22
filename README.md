The scheduler is run by running algorithm.py. 

The input to the algorithm are files located in the classes folder. These files contain the subject for each class, the type of class, the teacher, the student groups that are listening to that class, the allowed type of classroom and the length of the class.

The output for a file is in the form of a JSON file, where for each class from the input a time and classroom have been allocated. The algortihm takes into account several factors when computing the cost function, the most important one being the existance of a conflict of time or place.
