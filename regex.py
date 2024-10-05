#Only used for testing the regular expression not used in the main project
import re
regex = (r"^(0[1-9]|[1-7][0-9]|8[01])((\s?[a-zA-Z]\s?)(\d{4,5})|(\s?[a-zA-Z]{2}\s?)(\d{3,4})|(\s?[a-zA-Z]{3}\s?)(\d{2,"
         r"3}))$")

test_str = ("45 pww 354  ",
            "23 tt 4334  ",
            "24y67764  ")

#matches = re.finditer(regex, test_str, re.MULTILINE)

for i in test_str:
            
    i = i.replace(" ", "")
            
    if re.match(regex, i):
        print("Valid ")
    else:
        print("Invalid ")
    
        
