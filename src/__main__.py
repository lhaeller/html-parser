

# TODO: read TXT file
# TODO: read all TXT files in folder "data_in"
txt_file = open("../data/data_in/2020-11-03.txt","r")
path_to_test_file = "../data/data_in/2020-11-03.txt"

print("")
print("- - - - - - - - - - - - ")
print("U S I N G  read()-san")
print(txt_file.read())

txt_file.close()

# TODO: read each line and save to object
with open(path_to_test_file) as test_file:
    print("")
    print("- - - - - - - - - - - - ")
    print("U S I N G  I T E R A T O R")
    for line in test_file:
        print(line)

with open(path_to_test_file) as test_file:
    print("")
    print("- - - - - - - - - - - - ")
    print("U S I N G   readlines()-san")
    for line in test_file.readlines():
        print(line)


# TODO: define parse rules (.TXT to .HTML)
