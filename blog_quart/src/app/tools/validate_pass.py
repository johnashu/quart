import re

def validate(password: bytes) -> str:     
    password = str(password) 
    print(password)
    if len(password) < 8:
        return "Make sure your password is at least 8 letters"
    elif not re.search('[0-9]', password) :
        return "Make sure your password has a number in it"
    elif not re.search('[A-Z]', password): 
        return "Make sure your password has a capital letter in it"
    elif not re.search('[@#!$%^&*-]', password): 
        return "Make sure your password has a special character @#!$%^&*-"
    return 'True'

# p = 'default123ABC%$#'
# print(validate(p))

# p = 'default123ABC'
# print(validate(p))