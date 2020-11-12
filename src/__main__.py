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


            # start paragraph
            h2_regex = re.compile('<h2>')
            h2_match = h2_regex.match(line)

            h3_regex = re.compile('<h3>')
            h3_match = h3_regex.match(line)

            if h2_match == None and h3_match == None:
                if within_paragraph == False:
                    line = '<p>' + line
                    within_paragraph = True

            # close paragraph
            if is_empty_line(line):
                if within_paragraph:
                    line = "</p>"  # close paragraph
                    within_paragraph = False
                print(line_count, line)

            altered_lines.append(line)

        print("_______________________")

    if within_paragraph:
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
    link = re.compile('\[(.+)\]\(([^ ]+?)( "(.+)")?\)')  # [TEXT](linked-path)

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

    # TODO: make sure images are parsed before links are

    link_match = link.findall(clean_single_line)
    if link_match != None:
        print("found a link in:",clean_single_line)
        formatted_string = build_html_for_link(clean_single_line)

    # output line
    return formatted_string

def build_html_for_link(text):
    # all regex for links
    regex_link = re.compile('\[(.+)\]\(([^ ]+?)( "(.+)")?\)') # [TEXT](linked-path)
    regex_linked_text = re.compile('\[(.+)\]')  # [TEXT]
    regex_link_itself = re.compile('\(([^ ]+?)( "(.+)")?\)')  # (linked-path)
    regex_final_text_for_link = re.compile('(.+)')  # TEXT
    regex_final_link_itself = re.compile('([^ ]+?)( "(.+)")?')  # linked-path

    # objective
    html_text = ''


    link_match = regex_link.match(text)
    link_findall = regex_link.findall(text)
    link_search = regex_link.search(text)

    print("")

    if link_findall != None:
        print("find_all = ",link_findall)

        # TODO: shorten after testing
        # get text before first link
        listed_links = text.split('[')
        text_before_first_link = listed_links.pop(0)
        print("text_before_first_link:", text_before_first_link)
        html_text += text_before_first_link # save piece #1

        for element in listed_links:
            print("")

            element = "[" + element
            print("e=",element)

            linked_text_match = regex_linked_text.match(element)

            link_part_cut = element.split(']')
            link_part_cut.pop(0)
            c = 0
            link_part = ''
            for part in link_part_cut:
                print(c,part)
                c += 1
                link_part += part

            link_itself_match = regex_link_itself.match(link_part)

            # TODO: save non-linked part
            text_inbetween = ''
            if link_itself_match != None:
                extra_text = link_part.split(str(link_itself_match.group()))
                extra_text.pop(0)
                for text in extra_text:
                    text_inbetween += text


            # TODO: set linked text and link itself together
            final_linked_text = ''
            final_link_itself = ''


            if linked_text_match != None:
                # print("linked_text_match = ", linked_text_match.group())
                final_linked_text = str(linked_text_match.group())
                final_linked_text = final_linked_text[1:-1]
                print("final_linked_text =",final_linked_text)


            if link_itself_match != None:
                # print("link_itself_match =", link_itself_match.group())
                final_link_itself = str(link_itself_match.group())
                final_link_itself = final_link_itself[1:-1]
                print("final_link_itself = ",final_link_itself)

            link_html = "<a href='"+final_link_itself+"' target='_blank'>"+final_linked_text+"</a>"
            html_text += link_html

            # adding the rest of the text
            html_text += text_inbetween

    print("html_text:")
    print(html_text)

    return html_text

# main.py
parse_all_files(input_path, output_path)

# for testing
# temp_text = "welp. [this is a link](www.escapemod.net). and there's more:  [this is another link](www.google.com)"
# build_html_for_link(temp_text)
