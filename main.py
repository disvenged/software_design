"""Main module, combine the other modules to perform the full program.

Imported modules
---------------
    os
    image_handling

Inputs
------
    question_path
    answers_path

Outputs
-------
    Extracted answers
    Seperated questions
Constants
---------
    progress_file
    temp_path
    page_start
    page_end

Variables
---------
    found_questions
    question_amount
"""
import image_handling
import os

"""Set location for progress to be output to."""
progress_file = "progress.txt"

"""Set location to save temporary files"""
temp_path = "temp"

"""Read parameters from text file."""
with open("parameters.txt", 'r') as f:
    year = f.readline().strip()
    question_path = f.readline().replace("//", "////").strip()
    answers_path = f.readline().replace("//", "////").strip()

"""Set location to save the paper."""
save_path = "Paper\\"+str(year)

"""Output current progress to progress file."""
with open(progress_file, 'w') as f:
    f.write("parameters loaded")

"""Create folder to store paper in."""
os.makedirs(save_path)

"""Create array containing found questions."""
found_questions = image_handling.find_questions(question_path, temp_path+"\\page.png", progress_file)
"""Set question amount to the length of the array containing the questions found."""
question_amount = len(found_questions)

"""Seperate and save questions in specified save folder."""
image_handling.seperate_questions(found_questions, save_path, progress_file, temp_path)

"""Find and save answers."""
image_handling.find_answers(answers_path, save_path+"\\answers.png", question_amount, temp_path+"\\answers.png", progress_file)

"""Output progress to progress file."""
with open(progress_file, "w") as f:
    f.write("done")
