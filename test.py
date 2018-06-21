import image_handling

png_path = r"temp\page.png"
save_dir = r"temp\paper"
pdf_path = input("What is the question path? ").replace("\\", "\\\\")
answers_path = input("What is the answers path? ").replace("\\", "\\\\")
page_start = int(input("What is the first page of multiple choice questions? "))
page_end = int(input("What is the last page of multiple choice questions? "))
question_amount = int(input("How many questions are there? "))

image_handling.seperate_questions(image_handling.find_questions(pdf_path, png_path, page_start, page_end, question_amount), save_dir)

image_handling.pdf_to_image(answers_path, png_path.replace("page.png", "answers.png"), 1, 1)

answers_page_array = image_handling.image_to_array(png_path.replace("page.png", "answers_1.png"), 255)
template_array_num = image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Answer Symbol Templates\template_9.png", 255, True)

templates_chr = {
    "A": image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Answer Symbol Templates\template_A.png", 255, True),
    "B": image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Answer Symbol Templates\template_B.png", 255, True),
    "C": image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Answer Symbol Templates\template_C.png", 255, True),
    "D": image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Answer Symbol Templates\template_D.png", 255, True)
}

answers = []
for i in range(1, question_amount+1):
    template_array_num = image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Answer Symbol Templates\template_"+str(i)+".png", 255, True)

    curr_question = image_handling.compare_array(answers_page_array, template_array_num, 0, len(answers_page_array[0]), searching_for=1)
    answer_below = curr_question[0][1]

    print(curr_question, answer_below)

    if len(image_handling.compare_array(answers_page_array, templates_chr["A"], answer_below-1, len(answers_page_array[0]), searching_for=1, y_end=answer_below+5)):
        answers.append([i, "A"])
    elif len(image_handling.compare_array(answers_page_array, templates_chr["B"], answer_below-1, len(answers_page_array[0]), searching_for=1, y_end=answer_below+5)):
        answers.append([i, "B"])
    elif len(image_handling.compare_array(answers_page_array, templates_chr["C"], answer_below-1, len(answers_page_array[0]), searching_for=1, y_end=answer_below+5)):
        answers.append([i, "C"])
    else:
        answers.append([i, "D"])

print(answers)

with open(r"temp\paper\answers.txt", 'w') as f:
    for answer in answers:
        f.write(str(answer[0])+" "+str(answer[1])+"\n")
