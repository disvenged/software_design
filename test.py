import image_handling

png_path = r"temp\page.png"
save_dir = r"temp\paper"
pdf_path = input("What is the question path? ").replace("\\", "\\\\")
answers_path = input("What is the answers path? ").replace("\\", "\\\\")
page_start = int(input("What is the first page of multiple choice questions? "))
page_end = int(input("What is the last page of multiple choice questions? "))
question_amount = int(input("How many questions are there? "))

image_handling.seperate_questions(image_handling.find_questions(pdf_path, png_path), save_dir)

image_handling.find_answers(answers_path, save_dir+r"\answers.png", question_amount)
