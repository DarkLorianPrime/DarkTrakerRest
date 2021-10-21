def isEmail(email):
    email = email.split('@')
    if len(email) > 0:
        return True
    return False
