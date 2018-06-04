import image_handling

pdf_path = input("What is the pdf path? ").replace("\\", "\\\\")
png_path = "C:\\Users\\waca2\\OneDrive\\Software Design - HSC Major Project\\temp\\page.png"
page_start = int(input("What is the first page of multiple choice questions? "))
page_end = int(input("What is the last page of multiple choice questions? "))

question_amount = 20

num_positions = []

image_handling.pdf_to_image(pdf_path, png_path, page_start, page_end)

number_templates = {
    1:    image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_1.png", 255),
    2:    image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_2.png", 255),
    3:    image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_3.png", 255),
    4:    image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_4.png", 255),
    5:    image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_5.png", 255),
    6:    image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_6.png", 255),
    7:    image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_7.png", 255),
    8:    image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_8.png", 255),
    9:    image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_9.png", 255),
    10:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_10.png", 255),
    11:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_11.png", 255),
    12:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_12.png", 255),
    13:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_13.png", 255),
    14:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_14.png", 255),
    15:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_15.png", 255),
    16:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_16.png", 255),
    17:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_17.png", 255),
    18:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_18.png", 255),
    19:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_19.png", 255),
    20:   image_handling.image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Number Templates\template_20.png", 255)
}

page_1_array = image_handling.image_to_array(png_path.replace(".png", "_1.png"), 255)
num_positions.append(image_handling.compare_array(page_1_array, number_templates[1], image_handling.find_line(page_1_array), 80))
print(num_positions)

"""for i in range((2, question_amount+1):
    page_num, = 1
    page_array = image_handling.image_to_array(png_path.replace(".png", "_"+str(page_num)+".png"))
    template = number_templates[i]

    found_spots = image_handling.compare_array(page_array, template, 0, 80)
    """
