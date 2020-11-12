import re
from datetime import datetime
from pathlib import Path
import os

input_path = '../data/data_in/'
output_path = '../data/data_out/'

file_name = "2020-11-03.txt"
file_date = file_name.strip(".txt")  # TODO: use for h2 timestamp


def parse_all_files(input_path, output_path):
    file_list = os.listdir(input_path)
    for file in file_list:
        path_to_input_file = input_path + file
        html_lines = go_through_lines(path_to_input_file)

        # to test if input is coming
        print("html lines:")
        for line in html_lines:
            print(line)

        file_name = os.path.basename(file)
        print('file_name is:', file_name)
        path_to_output_file = output_path + file_name + ".html"
        Path(path_to_output_file).touch()  # create output file

        # write to output file
        with open(path_to_output_file, 'w') as file_handle:
            file_handle.writelines("%s\n" % line for line in html_lines)
            file_handle.close()


# TODO: read each line and save to object or maybe file
def go_through_lines(path):
    altered_lines = []
    file_name = os.path.basename(path)
    first_line = parse_basic_tags(file_name.strip(".txt"))  # file_name.strip(".txt")
    altered_lines.append(first_line)

    with open(path) as input_file:
        # for testing
        print("")
        print("O U T P U T  L I N E S")
        print("_______________________")
        line_count = 0

        # switch to handle empty lines
        within_paragraph = False

        for line in input_file.readlines():

            # add basic tags
            print(line_count, parse_basic_tags(line))
            line_count += 1
            line = parse_basic_tags(line)


            # open paragraph
            # print("line is:",line)
            h2_regex = re.compile('<h2>')
            h2_match = h2_regex.match(line)
            # print('h2_match = ',h2_match)
            h3_regex = re.compile('<h3>')
            h3_match = h3_regex.match(line)
            # print('h3_match =', h3_match)
            if h2_match == None:
                if h3_match == None:
                    if within_paragraph == False:
                        line = '<p>' + line
                        within_paragraph = True

            # close paragraphs
            if is_empty_line(line):
                if within_paragraph == True:
                    line = "</p>"  # close paragraph
                    within_paragraph = False
                print(line_count, line)

            altered_lines.append(line)

        print("_______________________")

    if within_paragraph == True:
        line = "</p>" # close final paragraph
        altered_lines.append(line)

    return altered_lines


def is_empty_line(line):
    # remove spaces and see if string is empty
    if not line.strip():
        return True
    else:
        return False


# TODO: define parse rules (.TXT to .HTML)
def parse_basic_tags(single_line):
    # return string
    clean_single_line = single_line.strip()  # delete leading and trailing spaces
    formatted_string = clean_single_line  # default

    # regex declarations
    date_jp = re.compile('\d\d\d\d-\d\d-\d\d')
    time_and_date_de = re.compile('\d\d:\d\d \d\d\/\d\d\/\d\d\d\d')  # hh:mm dd/mm/yyyy

    # executing checks
    time_date_de_match = time_and_date_de.match(clean_single_line)
    if time_date_de_match != None:
        # line = "10:22 03/11/2020"
        date_time_object = datetime.strptime(clean_single_line, '%H:%M %d/%m/%Y')
        time_only = datetime.strftime(date_time_object, '%H:%M')
        # print("time_only=",time_only)
        formatted_string = "<h3>" + time_only + "</h3>"

    date_jp_match = date_jp.match(clean_single_line)
    if date_jp_match != None:
        date = str(date_jp_match.group())
        date_time_object = datetime.strptime(date, '%Y-%m-%d')
        japanese_date = datetime.strftime(date_time_object, '%Y-%m-%d')
        formatted_string = "<h2>" + japanese_date + "</h2>"

    # output line
    return formatted_string


parse_all_files(input_path, output_path)