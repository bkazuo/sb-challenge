from random import randint
from datetime import datetime
import random
import time

def createHash():
    return ''.join(random.choice('0123456789abcdef') for i in range(24))

def createRandomNumber(size=11):
    return ''.join(random.choice('0123456789') for i in range(size))

def createRandomString(size=6):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(size))

def createRandomFloat(max_price = 400):
    return round(random.uniform(10, max_price),2)

def createRandomIntBetween(max_number = 10):
    return randint(0, max_number)

def createPositiveInt(max_number = 10):
    return randint(1, max_number)

def checkIfRepresentsFloat(value):
    if value == None:
        return False
        pass

    try: 
        float(value)
        return True
    except ValueError:
        return False

def createRandomEmail():
    return createRandomString() + '@' + createRandomString(4) + '.com.br'

def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end):
    prop = random.random()
    return datetime.strptime(strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop), '%m/%d/%Y %I:%M %p')