"""Compare an image to a template and return position of template within image.

imported modules:
    PIL.Image           -Opens and handles images
    subprocess.Popen    -Executes commands on command prompt


included funtions:
    pdf_to_image        -Convert a specified amount of pages from a pdf to an image and save them in specified location
    image_to_array      -Convert an image to an array and return it
    find_line           -Return position of 400 by 3 line within file
    find_whitespace     -Return amount of whitespace in first line of array before first black pixel
    compare_array       -Return position of one array within another
"""

from subprocess import Popen
from PIL import Image


def pdf_to_image(pdf_path, png_path, start, end):
    """Convert PDF to JPG.

    parameters:
        pdf_path    -path to PDF file to convert to jpg
        png_path    -path to save PNG file
        start       -page number to start conversion at
        end         -page number to end conversion at

    counter_variables:
        i
    """
    for i in range(start-1, end):
        params = ["C:\Program Files (x86)\ImageMagick-7.0.7-Q16\magick.exe", pdf_path+"["+str(i)+"]", "-alpha", "off", png_path.replace(".png", "_"+str(i-start+2)+".png")]
        Popen(params, shell=True)


def image_to_array(image_path, cutoff):
    """Convert image to array.

    Array created in form array[y][x] where y is rows and x is columns

    parameters:
        image_path              -path to image to be converted
        cutoff                  -cutoff for pixel to be white

    variables:
        converted_array         -array of converted image
        temp_array              -temporary array to store x values in
        image                   -image object to create array from
        cutoff_to_compare       -comparison that changes based on format of image

    counting variables:
        x                       -horizontal pixels
        y                       -vertical pixels
    """
    image = Image.open(image_path)

    converted_array = []
    temp_array = []

    if type(image.getpixel((0, 0))) is tuple:
        cutoff_to_compare = (cutoff, cutoff, cutoff)
    elif image.getpixel((0, 0)) == 0:
        cutoff_to_compare = 1
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
    """Search array for line of 0s, 400 wide and 3 down."""
    found = False
    breaking = False
    for y in range(len(s_array)):
        for x in range(len(s_array[0])):
            if s_array[y][x] == 0:
                found = True
                breaking = True
                for s_y in range(3):
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
    """Find the whitespace in the first line of a template array."""
    template_whitespace = 0
    for x in range(len(template_array[0])):
        if template_array[0][x] == 0:
            template_whitespace = x+1
            break
    return template_whitespace - 1


def compare_array(search_array, template_array, y_start, x_end):
    """Compare image to template and return position.

    parameters:
        search_array        -2d array to search
        template_array      -2d array of template to search for
        y_start             -vertical value to start search from
        x_end               -horizontal value to end search at

    variables:
        found_spots         -array of spots in the file where the number is found
        template_whitespace -whitespace before template arrays first black pixel

    counter variables:
        x                   -horizontal values
        y                   -vertical values
        s_x                 -searching horizontal values
        s_y                 -searching vertcal values

    flags:
        found               -set to true when template is found and when called the position is added to found_spots

    arrays in form [y][x] where:
        x                   -horizontal distance from top left of image
        y                   -vertical distance from top left of image

    template_array          -has no excess whitespace, ie black pixel in every line, where a 0 is black, 1 is white
    search_array            -same as above bar excess whitespace
    """
    found = False
    found_spots = []
    template_whitespace = find_whitespace(template_array)

    for y in range(y_start, len(search_array)):
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
                break
    return found_spots
