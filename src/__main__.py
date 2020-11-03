import re
from datetime import datetime

# TODO: read TXT file
# TODO: read all TXT files in folder "data_in"


path_to_test_file = "../data/data_in/2020-11-03.txt"
file_name = "2020-11-03.txt"
file_date = file_name.strip(".txt")  # TODO: use for h2 timestamp


# TODO: read each line and save to object
def go_through_lines(path):
    with open(path) as test_file:
        print("")
        print("- - - - - - - - - - - - ")
        print("U S I N G   readlines()-san")
        line_count = 0
        for line in test_file.readlines():
            line = line.strip()
            print(line_count, replace_tags(line))
            line_count += 1


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


go_through_lines(path_to_test_file)

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
