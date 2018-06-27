"""Main module, combine the other modules to perform the full program.

Inputs
------
    question_path
    answers_path

Constants
---------
    save_path_temp
    page_start
    page_end

Variables
---------
    question_amount
"""
import image_handling

with open("parameters.txt", 'r') as f:
    question_path = f.readline().replace("//", "////").strip()
    answers_path = f.readline().replace("//", "////").strip()

print(question_path)
print(answers_path)
