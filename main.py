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
temp_path = "temp"
save_path = "temp\\paper"
with open("parameters.txt", 'r') as f:
    question_path = f.readline().replace("//", "////").strip()
    answers_path = f.readline().replace("//", "////").strip()

found_questions = image_handling.find_questions(question_path, temp_path+"\\page.png")
question_amount = len(found_questions)

image_handling.seperate_questions(found_questions, save_path)

image_handling.find_answers(answers_path, save_path+"\\answers.png", question_amount, temp_path+"\\answers.png")

print(found_questions)

with open("parameters.txt", "w") as f:
    f.write("done")
