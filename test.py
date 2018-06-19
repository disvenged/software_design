import image_handling

pdf_path = input("What is the question path? ").replace("\\", "\\\\")
answers_path = input("What is the answers path? ").replace("\\", "\\\\")
png_path = r"temp\page.png"
page_start = int(input("What is the first page of multiple choice questions? "))
page_end = int(input("What is the last page of multiple choice questions? "))
question_amount = int(input("How many questions are there? "))

image_handling.seperate_questions(image_handling.find_questions(pdf_path, png_path, page_start, page_end, question_amount))

#image_handling.pdf_to_image(answers_path, png_path.replace("page.png", "answers.png"), 1, 1)
