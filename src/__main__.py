import re
from datetime import datetime
from pathlib import Path
import os
import shutil, os

input_path = '../data/data_in/'
output_path = '../data/data_out/'

file_name = "2020-11-03.txt"
file_date = file_name.strip(".txt")  # TODO: use for h2 timestamp


def parse_all_files(input_path, output_path):
    file_list = os.listdir(input_path)
    for file in file_list:
        path_to_input_file = input_path + file

        # read file while skipping non-text files
        file_name = os.path.basename(file)
        if is_textfile(file_name):
            html_lines = go_through_lines(path_to_input_file)
        else:
            continue

        # create html file
        file_name = os.path.basename(file)
        print('file_name is:', file_name)
        path_to_output_file = output_path + file_name[:-4] + ".html"
        Path(path_to_output_file).touch()  # create output file


        # write to output file
        with open(path_to_output_file, 'w') as file_handle:
            file_handle.writelines("%s\n" % line for line in html_lines)
            file_handle.close()

def is_textfile(filename):
    # check if .txt file
    print("filename =",filename)
    textfile_ending = filename[-4:]
    regex_textfile = re.compile('\.txt')
    match_textfile = regex_textfile.match(textfile_ending)
    print("textfile_ending =",textfile_ending)
    print("match_textfile = ",match_textfile)
    if match_textfile != None:
        return True
    else:
        return False

# TODO: read each line and save to object or maybe file
def go_through_lines(path):
    altered_lines = []
    file_name = os.path.basename(path)
    first_line = parse_basic_tags(file_name.strip(".txt"))  # file_name.strip(".txt")
    altered_lines.append(first_line)

    try:
        with open(path) as input_file:

            # regex declarations
            regex_date_jp = re.compile('\d\d\d\d-\d\d-\d\d')
            regex_time_and_date_de = re.compile('\d\d:\d\d \d\d\/\d\d\/\d\d\d\d')  # hh:mm dd/mm/yyyy
            regex_image = re.compile('\[\[(.+)\]\]')  # [path-to-image]

            regex_link = re.compile('\[(.+)|(.+)\]\(([^ ]+?)( "(.+)")?\)')  # [TEXT](linked-path)
            regex_bold_text = re.compile('\*\*')  # **TEXT**
            regex_italics_text = re.compile('\*')  # *TEXT*

            # after-checks for paragraph tags
            regex_h2 = re.compile('<h2>(.+)</h2>')
            regex_h3 = re.compile('<h3>(.+)</h3>')

            '''
            simple_regex = [
            {'opening_tag':'<b>','closing_tag':'</b>','pattern':re.compile('(.+)\*\*(.+)\*\*(.+)')},
            {'opening_tag': '<i>', 'closing_tag': '</i>', 'pattern': re.compile('\*(.+)\*')},
            {'opening_tag': '<h2>', 'closing_tag': '</h3>', 'pattern': re.compile('<h2>(.+)</h2>')},
            {'opening_tag': '<i>', 'closing_tag': '</i>', 'pattern': re.compile('<h3>(.+)</h3>')}
            ]

            special_regex = [
            {'opening_html':"<img src='",'link_start_signs':'[[','link_close_sign':']]','closing_html':"' style='max-width:40%' />"},
            ]
            html_text += "<img src='" + local_path_to_image + "' style='max-width:40%' />"
            '''

            # switches to handle multiple lines
            within_paragraph = False
            within_bold_format = False
            within_italics_format = False

            for line in input_file.readlines():

                line = line.strip()  # delete leading and trailing spaces

                # for each regex pattern : check text for pattern

                # single line formats
                date_jp_match = regex_date_jp.match(line)
                if date_jp_match != None:
                    date = str(date_jp_match.group())
                    date_time_object = datetime.strptime(date, '%Y-%m-%d')
                    japanese_date = datetime.strftime(date_time_object, '%Y-%m-%d')
                    line = "<h2>" + japanese_date + "</h2>"
                    # no need to check line further:
                    continue

                time_date_de_match = regex_time_and_date_de.match(line)
                if time_date_de_match != None:
                    date_time_object = datetime.strptime(line, '%H:%M %d/%m/%Y')
                    time_only = datetime.strftime(date_time_object, '%H:%M')
                    line = "<h3>" + time_only + "</h3>"
                    # no need to check line further:
                    continue

                image_match = regex_image.findall(line)
                if image_match != None:
                    # create 'data' directory for images
                    try:
                        data_path = output_path + 'data'
                        os.mkdir(data_path, 0o0775)
                    except(FileExistsError):
                        print("Directory 'data' exists already. Skipping directory creation.")

                    path_to_image = str(image_match.group())
                    path_to_image = path_to_image[2:-2]
                    local_path_to_image = 'data/' + path_to_image  # TODO: exclude 'https' img links
                    line = "<img src='" + local_path_to_image + "' style='max-width:40%' />"

                    # copy image file to output path
                    file = input_path + path_to_image
                    shutil.copy(file, output_path + 'data')

                    # no need to check line further:
                    continue


                link_match = regex_link.findall(line)
                # TODO: make into While loop
                if link_match != None:
                    
                    # pattern is [TEXT](linked-path)

                    regex_linked_text = re.compile('\[(.+)\]')  # [TEXT]
                    regex_link_itself = re.compile('\(([^ ]+?)( "(.+)")?\)')  # (linked-path)

                    # save the text before a '[' sign
                    text_with_link = line.split('[')
                    text_before_first_link = text_with_link.pop(0)
                    html_line = text_before_first_link

                    # get the linked text
                    rest_of_text = ''
                    for cut_part in text_with_link:
                        rest_of_text += cut_part

                    linked_text_match = regex_linked_text.match(rest_of_text)
                    linked_text = str(linked_text_match.group())

                    link_itself_match = regex_link_itself.match(rest_of_text)
                    link_itself = str(link_itself_match.group())

                    # TODO: put together html linked_text and link_itself
                    html_line += ''

                    # cut out the text that's already been processed
                    rest_of_text = ''
                    temp_rest_of_text = line.split(text_before_first_link)
                    for part in temp_rest_of_text: rest_of_text += part
                    temp_rest_of_text = line.split(link_match)
                    for part in rest_of_text: rest_of_text += part
                    line = rest_of_text


                # multi-line formats


                #   While: pattern matches
                #       switch handle: False -> True, True -> False
                #       split line in parts (before and after pattern-match)
                #       change markdown to html
                #   repeat with remaining text until False


                # save formatted line
                altered_lines.append(line)

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

    except UnicodeDecodeError:
        print("UnicodeDecodeError for Windows Systems")

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

# TODO: merge double code and possibly integrate checks right here or export them
# TODO: catch double-occurences of embedded special formats within a line
def parse_basic_tags(single_line):
    # return string
    clean_single_line = single_line.strip()  # delete leading and trailing spaces
    formatted_string = clean_single_line  # default

    # regex declarations
    date_jp = re.compile('\d\d\d\d-\d\d-\d\d')
    time_and_date_de = re.compile('\d\d:\d\d \d\d\/\d\d\/\d\d\d\d')  # hh:mm dd/mm/yyyy
    image = re.compile('\[\[(.+)\]\]')  # [path-to-image]
    link = re.compile('\[(.+)\]\(([^ ]+?)( "(.+)")?\)')  # [TEXT](linked-path)
    bold_text = re.compile('(.+)\*\*(.+)\*\*(.+)') # **TEXT**
    italics_text = re.compile('\*(.+)\*') # *TEXT*

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

    # images are parsed before links because of similar patterns
    image_match = image.match(clean_single_line)
    if image_match != None:
        formatted_string = build_html_for_images(clean_single_line)

    link_match = link.findall(formatted_string)
    if link_match != None:
        formatted_string = build_html_for_link(formatted_string)

    bold_match = bold_text.match(formatted_string)
    if bold_match != None:
        formatted_string = build_html_for_special_formats(formatted_string)

    italics_match = italics_text.match(formatted_string)
    if italics_match != None:
        formatted_string = build_html_for_special_formats(formatted_string)

    # output line
    return formatted_string

def build_html_for_special_formats(text):
    # regex declarations
    regex_bold = re.compile('(.+)\*\*(.+)\*\*(.+)') # **TEXT**
    regex_italics = re.compile('(.+)\*(.+)\*(.+)')  # *TEXT*

    # control switch
    found_bold = False
    active_text = text

    # objective
    html_text = ''

    bold_match = regex_bold.match(active_text)
    if bold_match != None:
        # control status update
        found_bold = True

        # splitting text in its parts
        active_text = active_text.split('**')

        # everything before the **
        text_before_bold = active_text[0]

        # bold text itself
        active_text.pop(0)
        bold_text = active_text[0]

        # everything after the **
        active_text.pop(0)
        text_after_bold = active_text[0]

        print("bold matching completed")

        html_text = text_before_bold + "<b>" + bold_text + "</b>" + text_after_bold

    if found_bold:
        active_text = html_text

    italics_match = regex_italics.match(active_text)
    if italics_match != None:
        # splitting text in its parts
        active_text = active_text.split('*')

        # everything before the *
        text_before_italics = active_text[0]

        # bold text itself
        active_text.pop(0)
        italics_text = active_text[0]

        # everything after the *
        active_text.pop(0)
        text_after_italics = active_text[0]

        print("italics matching completed")

        html_text = text_before_italics + "<i>" + italics_text + "</i>" + text_after_italics

    return html_text


def build_html_for_images(text):
    # regex declaration
    regex_image = re.compile('\[\[(.+)\]\]')  # [path-to-image]

    # objective
    html_text = ''

    image_match = regex_image.match(text)
    if image_match != None:
        print("image_match =", image_match.group())

        # create 'data' directory for images
        try:
            data_path = output_path + 'data'
            os.mkdir(data_path, 0o0775)
        except(FileExistsError):
            print("Directory 'data' exists already. Skipping directory creation.")

        path_to_image = str(image_match.group())
        path_to_image = path_to_image[2:-2]
        local_path_to_image = 'data/' + path_to_image # TODO: exclude 'https' img links
        print("path_to_image = ",local_path_to_image)
        html_text += "<img src='" + local_path_to_image + "' style='max-width:40%' />"

        # TODO: make sure image gets copied to data_out
        # copy image file to output path
        file = input_path + path_to_image
        shutil.copy(file, output_path + 'data')

    return html_text


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

    # since there can be several links in a line
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
