# VSB Class Tracker
This program helps with prepping for course registration McGill University.
When given a list of courses you are interested in taking, this program will find the number of seats in each of the classes of that course for the given term.
At the moment, this program only works on future terms and can break down if you select an ongoing term.
vsbClass.py is currently the main file.

# Disclaimer!
McGill does not allow you to register for courses using bots. Thus this program cannot and will not in the future help you register for the classes themselves. I would also advise against anyone doing so.


# Requirements
This program requires the Selenium Chrome Driver to be installed in the same directory as these files to run properly.


# Instructions
Call the main(list_of_desired_courses, term_of_interest) function in vsbClass.py.
For the term_of_interest parameter, you can either specify the term by a numeric representation of a month (1-5 for winter, 6-8 for summer, and 9-12 for Fall) or by typing "w" for winter, "f" for Fall, and "s" for the summer session.
