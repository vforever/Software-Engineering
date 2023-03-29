import re

def validate_email(email):
    regex = r"[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.edu\.cn"
    if re.fullmatch(regex, email):
        return True
    else:
        return False
    
def check_password(password):
    regex = r"[A-Za-z0-9!@#$%&_]{6,26}"
    if re.fullmatch(regex, password):
        return True
    else:
        return False