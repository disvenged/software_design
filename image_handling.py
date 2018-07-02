"""Compare an image to a template and return position of template within image.

Imported modules
----------------
    PIL.Image           -Opens and handles images
    subprocess.Popen    -Executes commands on command prompt
    time.sleep          -Stops execution of code for given time period

Included funtions
-----------------
    find_questions          -Find and output the locations of each question in order
    find_answers            -Find and save the answers to each question from a given answers PDF
    init_template_answers   -Load templates into a dictionary
    seperate_questions      -Seperate and save each individual question
    pdf_to_image            -Convert a specified amount of pages from a pdf to an image and save them in specified location
    image_to_array          -Convert an image to an array and return it
    find_line               -Return position of 400 by 3 line within file
    find_whitespace         -Return amount of whitespace in first line of array before first black pixel
    init_template_questions -Load templates into dictionary of arrays
    compare_array           -Return position of one array within another

"""

import os
from subprocess import Popen
from PIL import Image
from time import sleep


def find_questions(pdf_path, save_path, progress_file):
    """Find the y coordinate and the page number of the questions in a PDF document.

    Parameters
    ----------
        pdf_path            -Directory of PDF
        save_path           -Directory to save images permanently
        progress_file       -File to write progress to

    Variables
    ----------
        number_templates    -Dictionary of arrays for each number template from 1-20
        num_positions       -Arrays of number positions in form array[question][[x coordinate, y coordinate], page number]
        y_start             -Where to start search in page from
        page_array          -Array of search page
        template_array      -Template being searched for
        found_spots         -Array returned by compare_array function

    Counter variables
    -----------------
        page_num            -Page being searched
        question_num        -Question being searched for

    """
    """Create blank array for num_positions"""
    num_positions = []

    """Convert pages specified to images in specified folder."""
    pdf_to_image(pdf_path, save_path, 2, 12)

    """Load number templates for questions."""
    number_templates = init_template_questions()

    """Question one is done seperately as it is a special case."""

    """Load page 1 into an array."""
    page_array = image_to_array(save_path.replace(".png", "_1.png"), 255)

    """Add position of question 1 to array of positions."""
    num_positions.append([compare_array(page_array, number_templates[1], find_line(page_array), 80, searching_questions=True), 1])
    with open(progress_file, 'w') as f:
        f.write("Question 1 found.")
    print("Question 1 found.")
    """
    Set start position of the next search to the position of the first questionself.
    Set the question number to be searched for to 2.
    Set the page number to be searched to 1.
    """
    y_start = num_positions[0][0][0][1]
    question_num = 2
    page_num = 1

    """Begin iterating in a pre-test loop, that stops when there are no more pages to search."""
    while page_num <= 11 and question_num <= 20:
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
            with open(progress_file, 'w') as f:
                f.write("Question "+str(question_num)+" found.")
            print("Question "+str(question_num)+" found.")
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


def find_answers(ans_path, save_path, question_amount, temp_path, progress_file):
    """Find and write answers for questions to a text file.

    Parameters
    ----------
        ans_path                -Path to answers PDF
        save_path               -Folder to save to permanently
        question_amount         -Amount of questions to find answers to
        temp_path               -Path to save temporary files
        progress_file           -Path to file to output progress to

    Variables
    ---------
        answer_page_array       -Array of answers page
        templates_answers       -Dictionary containing templates for answers
        template_array          -Array of template
        curr_question_position           -Results of comparing template to page
        answer_below            -Answer for current question is below this point
        answers                 -Array of question numbers with answers

    Counter/temporary variables
    ---------------------------
        question_number         -Current quetion number
        f                       -Temporary file variable

    """
    """Convert answer page to image."""
    pdf_to_image(ans_path, temp_path, 1, 1)

    """Load answer page image into array."""
    answers_page_array = image_to_array(temp_path.replace(".png", "_1.png"), 255)

    """Load template of answer page numbers and characters."""
    templates_answers = init_template_answers()

    """Create blank array for answers."""
    answers = []

    """Counted loop that executes once for each question."""
    for question_number in range(1, question_amount+1):
        """
        Load template of current question number.
        Find template in array of answers and set curr_question_position to its position.
        Set the position to search from to the positin of the found number.
        """
        template_array = templates_answers[question_number]
        curr_question_position = compare_array(answers_page_array, template_array, 0, len(answers_page_array[0]), searching_for=1)

        answer_below = curr_question_position[0][1]

        """If a certain letter is the first one to be found after that position, add the letter and the question number to the answers array."""
        if len(compare_array(answers_page_array, templates_answers["A"], answer_below-1, len(answers_page_array[0]), searching_for=1, y_end=answer_below+5)):
            answers.append([question_number, "A"])
        elif len(compare_array(answers_page_array, templates_answers["B"], answer_below-1, len(answers_page_array[0]), searching_for=1, y_end=answer_below+5)):
            answers.append([question_number, "B"])
        elif len(compare_array(answers_page_array, templates_answers["C"], answer_below-1, len(answers_page_array[0]), searching_for=1, y_end=answer_below+5)):
            answers.append([question_number, "C"])
        else:
            answers.append([question_number, "D"])

        """Write current progress to an external file."""
        with open(progress_file, 'w') as f:
            f.write("Answer "+str(question_number)+" found.")
        print("Answer "+str(question_number)+" found.")

    """Create text file named answers containing answer data."""
    with open(save_path.replace(".png", ".txt"), 'w') as f:
        for answer in answers:
            f.write(str(answer[0])+" "+str(answer[1])+"\n")

    """Write current progress to an external file."""
    with open(progress_file, 'w') as f:
        f.write("Answers saved.")
    print("Answers saved.")


def init_template_answers():
    """Load templates for answer page into dictionary.

    Convert each template to array using image_to_array and store in dictionary.
    """
    templates_answers = {
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
    return templates_answers


def seperate_questions(question_locations, save_dir, progress_file, temp_path):
    """Crop and save images of find_questions.

    Parameters
    ----------
        question_locations      -array of question locations and page numbers
        save_dir                -Directory to permanently save files
        progress_file           -File to write progress to
        temp_path               -Directory to temporarily save files

    Variables
    ---------
        page_number             -current page being cropped
        page_array              -array of current page being cropped
        start                   -location of start of crop
        end                     -location of end of crop
        new_img                 -cropped image to be written
        black_line              -flag to tell if pixel in line
        white_line              -flag to tell if pixel in line
        png_path                -Location to save images

    Counter variables
    -----------------
        question_number         -current question number
        y                       -y coordinate of pixel to be written
        x                       -x coordinate of pixel to be written

    """
    """Set save path to internal folder."""
    png_path = temp_path+"\\page.png"

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

        """Create flag for line containing black pixel to break the loop"""
        black_line = False

        """Try structure catches exception IndexError, in order to catch and prevent the expected error from occuring."""
        try:
            """If next question is on the same page as the current question."""
            if question_locations[question_number+1][1] == question_locations[question_number][1]:
                """Set end of crop to vertical position of next question number"""
                end = question_locations[question_number+1][0][0][1] - 20

                """While current line being searched does not contain black pixel"""
                while not black_line:
                    if 0 not in page_array[end]:
                        """If no black pixel in line, set end to line above"""
                        end -= 1
                    else:
                        """If black pixel in line, break loop"""
                        black_line = True

                """If next question is not on same page as current question."""
            else:
                """Set end to 60 pixels above end of page"""
                end = len(page_array) - 60

                """While current line being searched does not contain black pixel"""
                while not black_line:
                    if 0 not in page_array[end]:
                        """If no black pixel in line, set end to line above"""
                        end -= 1
                    else:
                        """If black pixel in line, break loop"""
                        black_line = True

            """This error is raised if it is seperating the last question."""
        except IndexError:
            """Set end to 60 pixels above the end of the page."""
            end = len(page_array) - 60

            """While current line being searched does not contain black pixel"""
            while not black_line:
                if 0 not in page_array[end]:
                    """If no black pixel in line, set end to line above"""
                    end -= 1
                else:
                    """If black pixel in line, break loop"""
                    black_line = True

        """Create a new blank image object, the same size as the current question to be cropped."""
        new_img = Image.new("1", (len(page_array[0]), end-start+2))

        """Iterate through page array, within the bounds of the question."""
        for y in range(start, end+2):
            for x in range(len(page_array[1])):
                """Write the current pixel of the page to the new image."""
                new_img.putpixel((x, y-start), page_array[y][x])
        """Save the new image."""
        new_img.save(save_dir+"\\question_"+str(question_number+1)+".png")

        """Write progress to the progress file."""
        with open(progress_file, 'w') as f:
            f.write("Question "+str(question_number)+" saved.")
        print("Question "+str(question_number+1)+" saved.")


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
    """Iterate in range of pages to be converted"""
    for i in range(start-1, end):
        """Convert PDF to image using ImageMagick, as pure black and white."""
        params = [r"C:\Program Files (x86)\ImageMagick-7.0.7-Q16\magick.exe", pdf_path+"["+str(i)+"]", "-alpha", "off", png_path.replace(".png", "_"+str(i-start+2)+".png")]
        Popen(params, shell=True)
    """Delay for 6 seconds to allow program to convert images."""
    sleep(6)


def image_to_array(image_path, cutoff, template=False):
    """Convert image to array.

    Array created in form array[y][x] where y is rows and x is columns

    Parameters
    ----------
        image_path              -path to image to be converted
        cutoff                  -cutoff for pixel to be white
        template                -boolean as to whether image being converted is template

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
    """Open image to be converted"""
    image = Image.open(image_path)

    """
    Create blank array for converted image.
    Create temporary array to store x values of image.
    """
    converted_array = []
    temp_array = []

    """If image being converted is a template, set cutoff format to Greyscale"""
    if template:
        cutoff_to_compare = cutoff

        """Else if image being converted is in RGB form, set cutoff format to RGB"""
    elif type(image.getpixel((0, 0))) is tuple:
        cutoff_to_compare = (cutoff, cutoff, cutoff)

        """Else if image being converted is pure black and white, where white is a 0, set cutoff format to that."""
    elif image.getpixel((0, 0)) == 0:
        cutoff_to_compare = 0

        """Else if image being converted is pure black and white, where white is a 1, set cutoff format to that."""
    elif image.getpixel((0, 0)) == 1:
        cutoff_to_compare == 1

        """Final format it can be is RGB"""
    else:
        cutoff_to_compare = cutoff

    """Iterate through image."""
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            """Compare pixel values to cutoff format specified"""
            if image.getpixel((x, y)) == cutoff_to_compare:
                """If white add 1 to end of temp array."""
                temp_array.append(1)
            else:
                """If black add 0 to end of temp array."""
                temp_array.append(0)
        """Add temp array to end of converted array"""
        converted_array.append(temp_array)
        """Wipe temp array."""
        temp_array = []
    """Return converted array."""
    return converted_array


def find_line(s_array):
    """Search array for line of 0s, 400 wide and 3 down.

    Same as compare_array, except restricted to specific case
    Variables are the same, but only returns y value
    """
    """Set flag variables found and breaking to false."""
    found = False
    breaking = False
    """Iterate through 2D array to be searched."""
    for y in range(len(s_array)):
        for x in range(len(s_array[0])):
            """If a black pixel is found."""
            if s_array[y][x] == 0:
                """Set flags to True."""
                found = True
                breaking = True
                """Iterate through shape required for line condition"""
                for s_y in range(2):
                    for s_x in range(400):
                        """If the point in the array being compared isnt black, set found flag to False, causing the loop to end"""
                        if s_array[y+s_y][s_x+x] != 0:
                            found = False
                            break
                    if not found:
                        break
                """If the line is found, return the current value."""
                if found:
                    return y
            """Breaking flag causes loop to goto next y value to raise efficiency in the search."""
            if breaking:
                breaking = False
                break
    """If no line is found, return 0."""
    return 0


def find_whitespace(template_array):
    """Find the whitespace in the first line of a template array.

    Takes a template array in from template[y][x], returns position of first black pixel
    """
    """Set whitespace counter to 0"""
    template_whitespace = 0
    """Iterate through first line of array."""
    for x in range(len(template_array[0])):
        """If current pixel is black"""
        if template_array[0][x] == 0:
            """Set value of template_whitespace to current x value and end loop."""
            template_whitespace = x
            break
    """Output template_whitespace."""
    return template_whitespace


def init_template_questions():
    """Load template arrays into dictionary and return dictionary refering to them.

    Convert each template to array using image_to_array and store in dictionary.
    """
    templates_questions = {
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
    return templates_questions


def compare_array(search_array, template_array, y_start, x_end, searching_questions=False, searching_for=0, y_end=0):
    """Compare image to template and return position.

    Parameters
    ----------
        search_array        -2d array to search
        template_array      -2d array of template to search for
        y_start             -vertical value to start search from
        x_end               -horizontal value to end search at
        searching_questions -whether or not the numbers being searched for are questions
        searching_for       -How many templates are being searched for
        y_end               -vertical value to end search at

    Variables
    ---------
        found_spots         -array of spots in the file where the number is found
        template_whitespace -whitespace before template arrays first black pixel
        found               -flag set to true when template is found and when called the position is added to found_spots
        breaking            -flag set to true when all loops are to be ended

    Counter variables
    -----------------
        x                   -horizontal values
        y                   -vertical values
        s_x                 -searching horizontal values
        s_y                 -searching vertcal values

    """
    """If y_end is not specified, set y_end to the vertical length of the array to be searched"""
    if not y_end:
        y_end = len(search_array)

    """
    Set counter variables, found and break, to False.
    Found is set to true when the template is found within the array to be searched.
    Break is set to true when all the loops are to be ended.
    """
    found = False
    breaking = False

    """Create blank array for locations of templates found within the array to be searched."""
    found_spots = []
    """Set template_whitespace to the amount of whitespace in the top line of the template array."""
    template_whitespace = find_whitespace(template_array)
    """Iterate through array to be searched within the bounds specified."""
    for y in range(y_start, y_end):
        for x in range(x_end):
            """Start searching if there is enough room left in search_array for the template and if a black pixel is found."""
            if search_array[y][x] == 0 and len(search_array)-y >= len(template_array) and len(search_array[0])-x >= len(template_array) and x >= template_whitespace:
                """Set found flag to True, this will be set to false if the area is found not to contain the template."""
                found = True
                """Iterate through template_array"""
                for s_y in range(len(template_array)):
                    for s_x in range(len(template_array[0])):
                        """If the template_array pixel isnt the same as the search_array pixel in the corresponding spot relative to the start position of the search."""
                        if search_array[y+s_y][x-template_whitespace+s_x] != template_array[s_y][s_x]:
                            """Set found to false."""
                            found = False
                    if not found:
                        break
                """If the template array is in this position, add it's position to the array containing the found spots."""
                if found:
                    found_spots.append((x, y))
                """If searching for questions, only search until the first black pixel of each line."""
                if (searching_questions):
                    break
            """If searching_for is specified and the amount of spots found is equal to the amount being searched for, break the loops."""
            if (searching_for > 0 and len(found_spots) == searching_for):
                breaking = True
                break
        if breaking:
            break
    """Output spots that have been found."""
    return found_spots


def main():
    """Combine the other modules to perform the full program.

    Imported modules
    ---------------
        os
        image_handling

    Inputs
    ------
        question_path
        answers_path

    Outputs
    -------
        Extracted answers
        Seperated questions

    Constants
    ---------
        progress_file
        temp_path
        page_start
        page_end

    Variables
    ---------
        found_questions
        question_amount
    """
    """Set location for progress to be output to."""
    progress_file = "progress.txt"

    """Set location to save temporary files"""
    temp_path = "temp"

    """Read parameters from text file."""
    with open("parameters.txt", 'r') as f:
        year = f.readline().strip()
        question_path = f.readline().replace("//", "////").strip()
        answers_path = f.readline().replace("//", "////").strip()

    """Set location to save the paper."""
    save_path = "Papers\\"+str(year)

    """Output current progress to progress file."""
    with open(progress_file, 'w') as f:
        f.write("parameters loaded")
    print("Parameters loaded.")

    """Create folder to store paper in."""
    os.makedirs(save_path)

    """Create array containing found questions."""
    found_questions = find_questions(question_path, temp_path+"\\page.png", progress_file)
    """Set question amount to the length of the array containing the questions found."""
    question_amount = len(found_questions)

    """Seperate and save questions in specified save folder."""
    seperate_questions(found_questions, save_path, progress_file, temp_path)

    """Find and save answers."""
    find_answers(answers_path, save_path+"\\answers.png", question_amount, temp_path+"\\answers.png", progress_file)

    """Output progress to progress file."""
    with open(progress_file, "w") as f:
        f.write("done")
    print("Done")


if __name__ == "__main__":
    """Executes if module is called directly"""
    main()
