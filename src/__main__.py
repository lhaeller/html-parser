import re
from datetime import datetime
from pathlib import Path
import os

# TODO: read TXT file
# TODO: read all TXT files in folder "data_in"

# TODO: add variables "input_path" and "output_path" instead
path_to_test_file = "../data/data_in/2020-11-03.txt"  # to be replaced
path_to_output_file = '../data/data_out/new.txt'  # to be replaced
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
    with open(path) as input_file:
        print("")
        print("O U T P U T  L I N E S")
        print("_______________________")
        line_count = 0
        for line in input_file.readlines():
            line = line.strip()
            print(line_count, replace_tags(line))
            line_count += 1
            altered_lines.append(line)
        print("_______________________")

    return altered_lines


# TODO: define parse rules (.TXT to .HTML)
def replace_tags(single_line):
    # regex declarations
    time_and_date = re.compile('\d\d:\d\d \d\d\/\d\d\/\d\d\d\d')  # hh:mm dd/mm/yyyy

    # executing checks
    time_date_match = time_and_date.match(single_line)
    if time_date_match != None:
        # line = "10:22 03/11/2020"
        date_time_object = datetime.strptime(single_line, '%H:%M %d/%m/%Y')
        time_only = datetime.strftime(date_time_object, '%H:%M')

        # print("time_only=",time_only)
        formatted_string = "<h3>" + time_only + "</h3>"
        return formatted_string
    else:
        return single_line


parse_all_files(input_path, output_path)

# templates below this line

''' regex template 1
current_regex = re.compile('z00[a-zA-Z0-9][A-Za-z][A-Za-z][A-Za-z][A-Za-z]$')
dfs = dfs.replace(regex=current_regex, value="unknown")
'''

''' regex template 2
class Foo():
    _rex = re.compile("\d+")
    def bar(self, string):
         m = _rex.match(string)
         if m != None:
             doStuff()
'''
''' time formatting
datetimeObj = datetime.strftime(dt_obj, '%H:%M %d/%m/%Y')
'''
