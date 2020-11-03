

# TODO: read TXT file
# TODO: read all TXT files in folder "data_in"

path_to_test_file = "../data/data_in/2020-11-03.txt"

# TODO: read each line and save to object

with open(path_to_test_file) as test_file:
    print("")
    print("- - - - - - - - - - - - ")
    print("U S I N G   readlines()-san")
    line_count = 0
    for line in test_file.readlines():
        # if not "\n" in line:
        print(line_count, line.strip())
        line_count += 1

# TODO: define parse rules (.TXT to .HTML)
