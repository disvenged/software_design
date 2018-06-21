"""Compare an image to a template and return position of template within image.

Imported modules
----------------
    PIL.Image           -Opens and handles images
    subprocess.Popen    -Executes commands on command prompt


Included funtions
-----------------
    find_questions
    pdf_to_image        -Convert a specified amount of pages from a pdf to an image and save them in specified location
    image_to_array      -Convert an image to an array and return it
    find_line           -Return position of 400 by 3 line within file
    find_whitespace     -Return amount of whitespace in first line of array before first black pixel
    templates_init      -Load templates into dictionary of arrays
    compare_array       -Return position of one array within another

"""

from subprocess import Popen
from PIL import Image
from time import sleep


def find_questions(pdf_path, save_path, page_start, page_end, question_amount):
    """Find the y coordinate and the page number of the questions in a PDF document.

    Parameters
    ----------
        pdf_path            -Directory of PDF
        save_path           -Directory to save images
        page_start          -first page
        page_end            -last page
        question_amount     -Amount of questions

    Variables
    ----------
        number_templates    -Dictionary of arrays for each number template from 1-20
        page_array          -Array of first page, as first page must be done seperately to rest
        num_positions       -Arrays of number positions in form array[question][[x coordinate, y coordinate], page number]
        y_start             -Where to start search in page from
        question_num        -Question being searched for
        page_num            -Page being searched
        page_array          -Array of search page
        template            -Template being searched for
        found_spots         -Array returned by compare_array function

    """
    num_positions = []

    pdf_to_image(pdf_path, save_path, page_start, page_end)

    number_templates = templates_init()

    page_array = image_to_array(save_path.replace(".png", "_1.png"), 255)

    num_positions.append([compare_array(page_array, number_templates[1], find_line(page_array), 80, searching_questions=True), 1])
    print(num_positions)
    y_start = num_positions[0][0][0][1]
    question_num = 2
    page_num = 1
    while question_num <= question_amount and page_num <= page_end - page_start+1:
        page_array = image_to_array(save_path.replace(".png", "_"+str(page_num)+".png"), 255)
        template_array = number_templates[question_num]

        found_spots = compare_array(page_array, template_array, y_start, 80)

        if len(found_spots) == 1:
            num_positions.append([found_spots, page_num])
            question_num += 1
            y_start = num_positions[question_num-2][0][0][1]
            continue

        elif len(found_spots) == 0:
            page_num += 1
            y_start = 0
            continue

        else:
            break
    return num_positions


def seperate_questions(question_locations, save_dir):
    """Crop and save images of find_questions.

    Parameters
    ----------
        question_locations      -array of question locations and page numbers

    Variables
    ---------
        page_number             -current page being cropped
        page_array              -array of current page being cropped
        start                   -location of start of crop
        end                     -location of end of crop
        new_img                 -cropped image to be written

    Counter variables
    -----------------
        question_number         -current question number
        y                       -y coordinate of pixel to be written
        x                       -x coordinate of pixel to be written

    """
    png_path = r"temp\page.png"

    for question_number in range(len(question_locations)):
        page_number = question_locations[question_number][1]
        page_array = image_to_array(png_path.replace(".png", "_"+str(page_number)+".png"), 255)

        white_line = False
        start = question_locations[question_number][0][0][1]
        while not white_line:
            if 0 not in page_array[start]:
                white_line = True
            else:
                start -= 1
        white_line = False
        black_line = False
        try:
            if question_locations[question_number+1][1] == question_locations[question_number][1]:
                end = question_locations[question_number+1][0][0][1] - 20
                while not black_line:
                    if 0 not in page_array[end]:
                        end -= 1
                    else:
                        black_line = True
            else:
                end = len(page_array) - 60
                while not black_line:
                    if 0 not in page_array[end]:
                        end -= 1
                    else:
                        black_line = True
        except IndexError:
            end = len(page_array) - 60
            while not black_line:
                if 0 not in page_array[end]:
                    end -= 1
                else:
                    black_line = True
        black_line = False

        new_img = Image.new("1", (len(page_array[0]), end-start+2))
        for y in range(start, end+2):
            for x in range(len(page_array[1])):
                new_img.putpixel((x, y-start), page_array[y][x])
        new_img.save(save_dir+"\\question_"+str(question_number+1)+".png")


def pdf_to_image(pdf_path, png_path, start, end):
    """Convert PDF to JPG.

    Parameters
    ----------
        pdf_path    -path to PDF file to convert to jpg
        png_path    -path to save PNG file
        start       -page number to start conversion at
        end         -page number to end conversion at

    Counter variables
    -----------------
        i

    """
    for i in range(start-1, end):
        params = [r"C:\Program Files (x86)\ImageMagick-7.0.7-Q16\magick.exe", pdf_path+"["+str(i)+"]", "-alpha", "off", png_path.replace(".png", "_"+str(i-start+2)+".png")]
        Popen(params, shell=True)
    sleep(5)


def image_to_array(image_path, cutoff, template=False):
    """Convert image to array.

    Array created in form array[y][x] where y is rows and x is columns

    Parameters
    ----------
        image_path              -path to image to be converted
        cutoff                  -cutoff for pixel to be white

    Variables
    ---------
        converted_array         -array of converted image
        temp_array              -temporary array to store x values in
        image                   -image object to create array from
        cutoff_to_compare       -comparison that changes based on format of image

    Counting variables
    ------------------
        x                       -horizontal pixels
        y                       -vertical pixels

    """
    image = Image.open(image_path)

    converted_array = []
    temp_array = []

    if template:
        cutoff_to_compare = cutoff
    elif type(image.getpixel((0, 0))) is tuple:
        cutoff_to_compare = (cutoff, cutoff, cutoff)
    elif image.getpixel((0, 0)) == 0:
        cutoff_to_compare = 0
    elif image.getpixel((0, 0)) == 1:
        cutoff_to_compare == 1
    else:
        cutoff_to_compare = cutoff

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if image.getpixel((x, y)) == cutoff_to_compare:
                temp_array.append(1)
            else:
                temp_array.append(0)
        converted_array.append(temp_array)
        temp_array = []
    return converted_array


def find_line(s_array):
    """Search array for line of 0s, 400 wide and 3 down.

    Same as compare_array, except restricted to specific case
    Variables are the same, but only returns y value
    """
    found = False
    breaking = False
    for y in range(len(s_array)):
        for x in range(len(s_array[0])):
            if s_array[y][x] == 0:
                found = True
                breaking = True
                for s_y in range(2):
                    for s_x in range(400):
                        if s_array[y+s_y][s_x+x] != 0:
                            found = False
                            break
                    if not found:
                        break
                if found:
                    return y
            if breaking:
                breaking = False
                break
    return 0


def find_whitespace(template_array):
    """Find the whitespace in the first line of a template array.

    Takes a template array in from template[y][x], returns position of first black pixel
    """
    template_whitespace = 0
    for x in range(len(template_array[0])):
        if template_array[0][x] == 0:
            template_whitespace = x+1
            break
    return template_whitespace - 1


def templates_init():
    """Load template arrays into dictionary and return dictionary refering to them."""
    number_templates = {
        1:    image_to_array("Question Number Templates\\template_1.png", 255, True),
        2:    image_to_array("Question Number Templates\\template_2.png", 255, True),
        3:    image_to_array("Question Number Templates\\template_3.png", 255, True),
        4:    image_to_array("Question Number Templates\\template_4.png", 255, True),
        5:    image_to_array("Question Number Templates\\template_5.png", 255, True),
        6:    image_to_array("Question Number Templates\\template_6.png", 255, True),
        7:    image_to_array("Question Number Templates\\template_7.png", 255, True),
        8:    image_to_array("Question Number Templates\\template_8.png", 255, True),
        9:    image_to_array("Question Number Templates\\template_9.png", 255, True),
        10:   image_to_array("Question Number Templates\\template_10.png", 255, True),
        11:   image_to_array("Question Number Templates\\template_11.png", 255, True),
        12:   image_to_array("Question Number Templates\\template_12.png", 255, True),
        13:   image_to_array("Question Number Templates\\template_13.png", 255, True),
        14:   image_to_array("Question Number Templates\\template_14.png", 255, True),
        15:   image_to_array("Question Number Templates\\template_15.png", 255, True),
        16:   image_to_array("Question Number Templates\\template_16.png", 255, True),
        17:   image_to_array("Question Number Templates\\template_17.png", 255, True),
        18:   image_to_array("Question Number Templates\\template_18.png", 255, True),
        19:   image_to_array("Question Number Templates\\template_19.png", 255, True),
        20:   image_to_array("Question Number Templates\\template_20.png", 255, True)
    }
    return number_templates


def compare_array(search_array, template_array, y_start, x_end, searching_questions=False, searching_for=0, y_end=0):
    """Compare image to template and return position.

    Parameters
    ----------
        search_array        -2d array to search
        template_array      -2d array of template to search for
        y_start             -vertical value to start search from
        x_end               -horizontal value to end search at

    Variables
    ---------
        found_spots         -array of spots in the file where the number is found
        template_whitespace -whitespace before template arrays first black pixel

    Counter variables
    -----------------
        x                   -horizontal values
        y                   -vertical values
        s_x                 -searching horizontal values
        s_y                 -searching vertcal values

    Flags
    -----
        found               -set to true when template is found and when called the position is added to found_spots

    arrays in form [y][x] where:
        x                   -horizontal distance from top left of image
        y                   -vertical distance from top left of image

    template_array          -has no excess whitespace, ie black pixel in every line, where a 0 is black, 1 is white
    search_array            -same as above bar excess whitespace

    """
    if not y_end:
        y_end = len(search_array)
    found = False
    breaking = False
    found_spots = []
    template_whitespace = find_whitespace(template_array)
    for y in range(y_start, y_end):
        for x in range(x_end):
            """Iterate through array to be searched."""
            if search_array[y][x] == 0 and len(search_array)-y >= len(template_array) and len(search_array[0])-x >= len(template_array) and x >= template_whitespace:
                """Start searching if there is enough room left in search_array for the template and if a black pixel is found."""
                found = True
                for s_y in range(len(template_array)):
                    for s_x in range(len(template_array[0])):
                        """Iterate through template_array and compare to corresponding spots in search_array."""
                        if search_array[y+s_y][x-template_whitespace+s_x] != template_array[s_y][s_x]:
                            found = False
                    if not found:
                        break
                if found:
                    found_spots.append((x, y))
                if (searching_questions):
                    break
            if (searching_for > 0 and len(found_spots) == searching_for):
                breaking = True
                break
        if breaking:
            break
    return found_spots


if __name__ == "__main__":
    """Executes if module is called directly"""
    template = image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\Question Number Templates\template_1.png", 255)
    search = image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\temp\page_1.png", 255)
    number_templates = templates_init()
    print(find_line(search))

    for y in range(len(template)):
        for x in range(len(template[0])):
            print(template[y][x], end="")
        print()

    for y in range(len(search)):
        for x in range(90):
            print(search[y][x], end="")
        print()

    print(compare_array(search, number_templates[1], find_line(search), len(search[0]), searching_questions=True))
