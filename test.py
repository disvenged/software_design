import image_handling

pdf_path = input("What is the pdf path? ").replace("\\", "\\\\")
png_path = "temp\page.png"
page_start = int(input("What is the first page of multiple choice questions? "))
page_end = int(input("What is the last page of multiple choice questions? "))
question_amount = int(input("How many questions are there? "))

for i in image_handling.find_questions(pdf_path, png_path, page_start, page_end, question_amount):
    page_number = i[1]
    
