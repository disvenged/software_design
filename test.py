import image_handling

png_path = r"temp\page.png"
pdf_path = input("What is the question path? ").replace("\\", "\\\\")
answers_path = input("What is the answers path? ").replace("\\", "\\\\")
page_start = int(input("What is the first page of multiple choice questions? "))
page_end = int(input("What is the last page of multiple choice questions? "))
question_amount = int(input("How many questions are there? "))

"""
image_handling.seperate_questions(image_handling.find_questions(pdf_path, png_path, page_start, page_end, question_amount))
"""

image_handling.pdf_to_image(answers_path, png_path.replace("page.png", "answers.png"), 1, 1)

answers_page_array = image_handling.image_to_array(png_path.replace("page.png", "answers_1.png"), 255)
template_array_num = image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Answer Symbol Templates\template_9.png", 255, True)
template_array_chr = image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Answer Symbol Templates\template_A.png", 255, True)
locations_num = image_handling.compare_array(answers_page_array, template_array_num, 0, len(answers_page_array[0]))
locations_chr = image_handling.compare_array(answers_page_array, template_array_chr, 0, len(answers_page_array[0]))

print(locations_num)
print(locations_chr)
