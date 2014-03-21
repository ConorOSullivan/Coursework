#!/usr/bin/env python

'''
This assignment involved me reading in some proper
and faulty contact information that would or would not
be picked up by my regular expressions, depending on
if they were valid or not.
'''

import re

def question1(str):
    return re.match(r'^[A-Za-z-]+,{1}\s{1}[A-Za-z]$', str)

def question2(str):
    return re.match(r'^[0-9]+(\s{1}[A-Za-z]+)+\.?$', str)

def question3(str):
    return re.match(r'^w{3}\.[A-Za-z0-9]+\.(com|org|net|mil|edu)$', str)

def question4(str):
    return re.match(r'^(([0-9]{4}-){3}[0-9]{4})|([0-9]{4}-[0-9]{6}-[0-9]{5})$', str)

def question5(str):
    return re.match(r'^((\d{3}-){2}\d{4})|(\(\d{3}\)\s\d{3}-?\d{4})|((\d{3})?-?\d{3}-?\d{4})|(\(\d{3}\)\d{3}-?\d{4})$', str)

def question6(str):
    return re.match(r'^(([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.)(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){2}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$', str)

def question7():
    numold = 0
    f = open('who.txt')
    lines = f.readlines()
    f.close()
    for line in lines:
        if re.search(r'old', line):
            numold += 1
    return "Ratio of entries listed as old: %f" % (float(numold)/len(lines))

def question8():
    f = open('who.txt')
    lines = f.readlines()
    f.close()
    a = []
    current=0
    for line in lines:
        if not re.match(r'^LOGIN', line) and not re.match(r'^\s+system', line) and not re.match(r'^\s+run', line):
            if re.match(r'^\w+', line): #if the line begins with a name, make the current name that name
                current = re.match(r'^\w+', line).group()
            if re.search(r'2013-08',line): #if the login took place in august, add the previously seen name to our names list
                a.append(current)
    return sorted(list(set(a))) #our unique sorted names
