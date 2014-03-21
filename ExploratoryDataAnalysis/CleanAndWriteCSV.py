    #!/usr/bin/python
'''
In this assignment, I read in the JSON file included
in this directory and wrote it out to a CSV file.
'''



import argparse
import json
import math
import os
import sys
import csv



def parseArgument():
    """
	Code for parsing arguments
	"""
    parser = argparse.ArgumentParser(description='Parsing a file.')
    parser.add_argument('-f', required=True)

    parser.add_argument('-o', required=True)
    args = vars(parser.parse_args())
    return args


def parseFile(filename):
    """
	This would load the json file
	"""
    json_data = open(filename, "r")
    data = json.load(json_data)
    json_data.close()
    return data

maclist = [] #creating list of mac addresses that I'll loop through later

def getallmacs(data, f):
    for record in data[0]["Data"]:
        for router in record["Quantities"]:
            if router["Name"][0:4] == "gyro" or router["Name"][0:4] == "mfie" or router["Name"][0:3] == "acc": #making sure I don't pick up unwanted recordings
                continue
            else:
                maclist.append(router["Name"])
    macset = set(maclist)
    maclist2 = list(macset)
    maclist3 = sorted(maclist2)
    return maclist3


def createmacdict(record):#needs to be passed quantities list from recording
    tempdict = {}
    if record["Quantities"][0]["Name"][0:4] == "gyro" or record["Quantities"][0]["Name"][0:4] == "mfie" or record["Quantities"][0]["Name"][0:3] == "acc":
        return
    else:
        tempdict['Source'] = record['Source']
        tempdict['Room'] = record['Properties'][0]['Value']
        tempdict['Time'] = record['MTime']
        for router in record["Quantities"]:
            tempdict[router["Name"]] = int(router["Number"])*1.0
    return tempdict


def createdictionarylist(data):
    dictionarylist=[]
    for recording in data[0]["Data"]:
        dictionarylist.append(createmacdict(recording))
    return dictionarylist


def main():
    args = parseArgument()
    filename = args['f']
    print filename
    totaldata = parseFile(filename)
    ### your code here
    outputfile = args['o']
    f = open(outputfile, "wb")
    maclist = getallmacs(totaldata, f)#here I have the ordered list of unique MAC addresses
    fns = ['Source','Room','Time']+maclist
    writer3 = csv.DictWriter(f, fns, restval="NA") #set default value equal to NA
    writer3.writer.writerow(writer3.fieldnames) #write first line
    dictionarylist = filter(None, createdictionarylist(totaldata)) #remove 'None's from the list of dictionaries that were produced as a result of 'return statements
    for dictionary in dictionarylist:
        writer3.writerow(dictionary) #use each dictionary to write each row
    f.close()

main()
