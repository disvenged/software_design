"""Compare an image to a template and return position of template within image.

Imported modules
----------------
    PIL.Image           -Opens and handles images
    subprocess.Popen    -Executes commands on command prompt
    time.sleep          -Stops execution of code for given time period

Included funtions
-----------------
    find_questions
    find_answers
    init_template_answers
    seperate_questions
    pdf_to_image            -Convert a specified amount of pages from a pdf to an image and save them in specified location
    image_to_array          -Convert an image to an array and return it
    find_line               -Return position of 400 by 3 line within file
    find_whitespace         -Return amount of whitespace in first line of array before first black pixel
    init_template_questions -Load templates into dictionary of arrays
    compare_array           -Return position of one array within another

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

    """Convert pages specified to images in specified folder."""
    pdf_to_image(pdf_path, save_path, page_start, page_end)

    """Load number templates for questions."""
    number_templates = init_template_questions()

    """Question one is done seperately as it is a special case."""

    """Load page 1 into an array."""
    page_array = image_to_array(save_path.replace(".png", "_1.png"), 255)

    """Add position of question 1 to array of positions."""
    num_positions.append([compare_array(page_array, number_templates[1], find_line(page_array), 80, searching_questions=True), 1])

    """
    Set start position of the next search to the position of the first questionself.
    Set the question number to be searched for to 2.
    Set the page number to be searched to 1.
    """
    y_start = num_positions[0][0][0][1]
    question_num = 2
    page_num = 1

    """Begin iterating in a pre-test loop, that stops when all the questions are found, or there are no more pages to search."""
    while question_num <= question_amount and page_num <= page_end - page_start+1:
        """
        Load page to be searched into an array.
        Load template to search for into an array.
        """
        page_array = image_to_array(save_path.replace(".png", "_"+str(page_num)+".png"), 255)
        template_array = number_templates[question_num]

        """Search for the template array in the page array, and return an array of spots where it was found"""
        found_spots = compare_array(page_array, template_array, y_start, 80)

        """If only 1 of the template was found in the page, add it's position to an array of the found questions."""
        if len(found_spots) == 1:
            num_positions.append([found_spots, page_num])
            """
            Set current question to the next question.
            Set start of next search to position of previously found question.
            Continue to next iteration of loop
            """
            question_num += 1
            y_start = num_positions[question_num-2][0][0][1]
            continue

            """Else if no templates are found in page, begin searching next page from the top."""
        elif len(found_spots) == 0:
            page_num += 1
            y_start = 0
            continue

            """Else if more than 1 templates are found in page, break loop.
            # TODO: Remove need for this.
            """
        else:
            break
    """Return positions and page number of questions."""
    return num_positions


def find_answers(ans_path, save_path, question_amount):
    """Find and write answers for questions to a text file.

    Parameters
    ----------
        ans_path
        save_path
        question_amount

    Variables
    ---------
        template_array_num
        curr_question
        answer_below
        answers

    Counter/temporary variables
    ---------------------------
        i
        f

    """
    """Convert answer page to image."""
    pdf_to_image(ans_path, save_path, 1, 1)

    """Load answer page image into array."""
    answers_page_array = image_to_array(save_path, 255)

    """Load template of answer page numbers and characters."""
    templates_chr = init_template_answers()

    """Create blank array for answers."""
    answers = []

    """Counted loop that executes once for each question."""
    for i in range(1, question_amount+1):
        """
        Load template of current question number.
        Find template in array of answers and set curr_question to its position.
        Set the position to search from to the positin of the found number
        """
        template_array_num = templates_chr[i]
        curr_question = compare_array(answers_page_array, template_array_num, 0, len(answers_page_array[0]), searching_for=1)
        answer_below = curr_question[0][1]

        """If a certain letter is the first one to be found after that position, add the letter and the question number to the answers array."""
        if len(compare_array(answers_page_array, templates_chr["A"], answer_below-1, len(answers_page_array[0]), searching_for=1, y_end=answer_below+5)):
            answers.append([i, "A"])
        elif len(compare_array(answers_page_array, templates_chr["B"], answer_below-1, len(answers_page_array[0]), searching_for=1, y_end=answer_below+5)):
            answers.append([i, "B"])
        elif len(compare_array(answers_page_array, templates_chr["C"], answer_below-1, len(answers_page_array[0]), searching_for=1, y_end=answer_below+5)):
            answers.append([i, "C"])
        else:
            answers.append([i, "D"])

    """Create text file named answers containing answer data."""
    with open(r"temp\paper\answers.txt", 'w') as f:
        for answer in answers:
            f.write(str(answer[0])+" "+str(answer[1])+"\n")


def init_template_answers():
    """Load templates for answer page into dictionary."""
    templates_chr = {
        "A": image_to_array(r"Answer Symbol Templates\template_A.png", 255, True),
        "B": image_to_array(r"Answer Symbol Templates\template_B.png", 255, True),
        "C": image_to_array(r"Answer Symbol Templates\template_C.png", 255, True),
        "D": image_to_array(r"Answer Symbol Templates\template_D.png", 255, True),
        1:   image_to_array("Answer Symbol Templates\\template_1.png", 255, True),
        2:   image_to_array("Answer Symbol Templates\\template_2.png", 255, True),
        3:   image_to_array("Answer Symbol Templates\\template_3.png", 255, True),
        4:   image_to_array("Answer Symbol Templates\\template_4.png", 255, True),
        5:   image_to_array("Answer Symbol Templates\\template_5.png", 255, True),
        6:   image_to_array("Answer Symbol Templates\\template_6.png", 255, True),
        7:   image_to_array("Answer Symbol Templates\\template_7.png", 255, True),
        8:   image_to_array("Answer Symbol Templates\\template_8.png", 255, True),
        9:   image_to_array("Answer Symbol Templates\\template_9.png", 255, True),
        10:  image_to_array("Answer Symbol Templates\\template_10.png", 255, True),
        11:  image_to_array("Answer Symbol Templates\\template_11.png", 255, True),
        12:  image_to_array("Answer Symbol Templates\\template_12.png", 255, True),
        13:  image_to_array("Answer Symbol Templates\\template_13.png", 255, True),
        14:  image_to_array("Answer Symbol Templates\\template_14.png", 255, True),
        15:  image_to_array("Answer Symbol Templates\\template_15.png", 255, True),
        16:  image_to_array("Answer Symbol Templates\\template_16.png", 255, True),
        17:  image_to_array("Answer Symbol Templates\\template_17.png", 255, True),
        18:  image_to_array("Answer Symbol Templates\\template_18.png", 255, True),
        19:  image_to_array("Answer Symbol Templates\\template_19.png", 255, True),
        20:  image_to_array("Answer Symbol Templates\\template_20.png", 255, True)
    }
    return templates_chr


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
        white_line
        black_line

    Counter variables
    -----------------
        question_number         -current question number
        y                       -y coordinate of pixel to be written
        x                       -x coordinate of pixel to be written

    """
    """Set save path to internal folder."""
    png_path = r"temp\page.png"

    """Counted for loop to iterate through questions"""
    for question_number in range(len(question_locations)):
        """
        Set current page to the page that the question is in.
        Convert current page to array.
        """
        page_number = question_locations[question_number][1]
        page_array = image_to_array(png_path.replace(".png", "_"+str(page_number)+".png"), 255)

        """The next section handles the determining of the location of the question starts and ends."""

        """
        Create flag white_line for breaking loop.
        Set start location to location of first question number.
        """
        white_line = False
        start = question_locations[question_number][0][0][1]
        """Move start location up the page until a line filled with white pixels is found."""
        while not white_line:
            if 0 not in page_array[start]:
                white_line = True
            else:
                start -= 1
        """Set flag for next loop."""
        white_line = False

        """Create flag for line containing black pixel to break the loop"""
        black_line = False

        """Try structure catches exception IndexError, in order to catch and prevent error from occuring."""
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


def init_template_questions():
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
    template = image_to_array(r"Question Number Templates\template_10.png", 255)
    search = image_to_array(r"C:\Users\waca2\OneDrive\Software Design - HSC Major Project\temp\page_4.png", 255)
    number_templates = init_template_questions()
    print(find_line(search))

    for y in range(len(template)):
        for x in range(len(template[0])):
            print(template[y][x], end="")
        print()

    for y in range(len(search)):
        for x in range(90):
            print(search[y][x], end="")
        print()

    print(compare_array(search, number_templates[10], find_line(search), len(search[0]), searching_questions=True))
