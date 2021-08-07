import random
from datetime import datetime

variable = None
vb = None
otp = None

def get_variable():
    return variable

def create_new_ref_number():
    global variable
    variable = str(random.randint(1000000, 9999999))
    return variable

def dt():
    global vb
    vb = datetime.today().strftime('%Y-%m-%d')
    return vb

def otplogin():
    global otp
    otp = str(random.randint(111111, 999999))
    return otp

