# # # # # # # # # # # # # # # # # #
# Color Identifier Project
# Author: Saransh Kumar
# Dataset used: https://github.com/codebrainz/color-names/blob/master/output/colors.csv (Color Names)
# 
# To Dos:
#   • Add docstrings and comments
#   • Beautify manually
#   • Explore keyboard event controls 
# # # # # # # # # # # # # # # # # #

import argparse
import pandas
import cv2


def read_input_image(image_path):
    image = cv2.imread(image_path)
    image = resize_input_image(image)
    return image


def resize_input_image(image):
    h, w, _ = image.shape
    scale_down_factor_x = 1
    scale_down_factor_y = 1
    x_limit = 1500
    y_limit = 800
    if w > x_limit:
        scale_down_factor_x = round(x_limit / w, 2)
    if h > 800:
        scale_down_factor_y = round(y_limit / h, 2)

    scale_down_factor = min(scale_down_factor_x, scale_down_factor_y)
    image = cv2.resize(image, None, fx=scale_down_factor, fy=scale_down_factor, interpolation=cv2.INTER_AREA)
    return image


def get_color_names_list():
    column_names = ['color_code', 'Color_Name', 'hex', 'R', 'G', 'B']
    color_names_list = pandas.read_csv(
        'color-names.csv', names=column_names, header=None)
    return color_names_list


def callback_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global xpos, ypos, click_event, b, g, r
        click_event = True
        xpos = x
        ypos = y
        b, g, r = image[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


def find_color_name(color_names_list):
    minimum_distance = 10000
    color_name = ''

    for i in range(len(color_names_list)):
        distance = abs(r - color_names_list.loc[i, 'R'])
        distance += abs(g - color_names_list.loc[i, 'G'])
        distance += abs(b - color_names_list.loc[i, 'B'])

        if distance < minimum_distance:
            minimum_distance = distance
            color_name = color_names_list.loc[i, 'Color_Name']

    return color_name


def parse_image_path_from_args():
    parser = argparse.ArgumentParser(description="Find the color name at a clicked point on the image")
    parser.add_argument("-i", "--image", default='pexels-photo-347735.jpeg', help="image file path")
    args = parser.parse_args()
    return args.image


if __name__ == '__main__':

    image_path = parse_image_path_from_args()
    image = read_input_image(image_path)

    color_names_list = get_color_names_list()

    click_event = False

    cv2.namedWindow('Image', cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Image", callback_function)

    while True:

        cv2.imshow('Image', image)

        if click_event:

            cv2.rectangle(image, (20, 20), (1000, 60), (b, g, r), -1)

            text = find_color_name(color_names_list) + f" rgb({r}, {g}, {b})"
            cv2.putText(image, text, (50, 50), 2, 0.8,
                        (255, 255, 255), 1, cv2.LINE_AA)

            if r + g + b > 600:
                cv2.putText(image, text, (50, 50), 2, 0.8,
                            (0, 0, 0), 1, cv2.LINE_AA)

            click_event = False

        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
