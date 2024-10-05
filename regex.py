
import re


test_str = ("45 pww 354  ",
            "23 tt 4334  ",
            "24y67764  ")

#matches = re.finditer(regex, test_str, re.MULTILINE)

for i in test_str:
    i = i.replace(" ", "")
    if(True):
        print("Valid ")
    else:
        print("Invalid ")