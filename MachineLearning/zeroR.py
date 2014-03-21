__author__ = 'conorosullivan'

import sklearn.datasets
import argparse
import re
from random import choice

def csvRead(filename):
    '''
    Parses a csv
    '''
    csvDict = {}
    # filename = 'BioResponseKaggleTrain.csv'
    f = open(filename,'r')
    csvDict['feature_names'] = re.sub(r'\n', '', f.readline()).split(',')[1:]
    len(csvDict['feature_names'])
    csvDict['data'] = []
    csvDict['target'] = []
    for line in f:
        csvDict['data'].append(re.sub(r'\n', '', line[2:]).split(','))
        csvDict['target'].append(line[0])
    f.close()
    csvDict['target_names'] = list(set(csvDict['target']))
    csvDict['DESCR'] = filename
    return csvDict

def toyRead(filename):

    csvDict = sklearn.datasets.__getattribute__('load_'+filename)()
    if filename == 'digits':
        csvDict['feature_names'] = range(0, 64)
    if filename == 'boston':
        csvDict['target_names'] = list(set(csvDict['target']))
    return csvDict

def mlRead(filename):
    # this works for the small mldata.org set
    f = open(filename, "r")
    lines = f.readlines()
    csvDict = {}
    csvDict['data'] = []
    csvDict['target'] = []
    csvDict['feature_names'] = re.sub("\n", '', lines[12]).split(';')[1:]
    for line in lines[13:]:
        info = re.sub("\n", '', line).split(';')
        csvDict['data'].append(info[:-1])
        csvDict['target'].append(info[-1])
        # csvDict['data'].append(re.sub("\n", '', line).split(';')[:-1])
    f.close()
    csvDict['target_names'] = list(set(csvDict['target']))
    return csvDict

def mlRead2(filename):
    # this works for the huge MLdata.org set
    f = open(filename, "r")
    lines = f.readlines()
    csvDict = {}
    csvDict['data'] = []
    csvDict['target'] = []
    csvDict['feature_names'] = re.sub("\n", '', lines[0]).split(';')[1:]
    for line in lines[1:]:
        info = re.sub("\n", '', line).split(';')
        csvDict['data'].append(info[:-1])
        csvDict['target'].append(info[-1])
        # csvDict['data'].append(re.sub("\n", '', line).split(';')[:-1])
    f.close()
    csvDict['target_names'] = list(set(csvDict['target']))
    return csvDict

def output(dictionary):
    '''
    Prints out the information about a dictionary from the CSV
    '''
    numFeatures = len(dictionary['feature_names'])
    numExamples = len(dictionary['data'])
    infodict = {}
    infodict['# of examples'] = numExamples
    infodict['# of features'] = numFeatures
    infodict['Target Variables'] = dictionary['target_names']
    print infodict


def findAndReplace(dictionary, targetNames):

    # Takes a list of numbers and replaces those with the names of the targets

    targets = dictionary['target'].tolist()
    for n,i in enumerate(targets):
        for y in range(0, len(targetNames)):
            if i==y:
                targets[n] = targetNames[y]
    return targets

def zeroR(dictionary, type):

    # Returns most common element in targets list
    targetNames = dictionary['target_names']

    if type == 'csv' or type == 'mldata':
        targets = dictionary['target']
    elif type == 'toy':
        targets = findAndReplace(dictionary, targetNames)
    mostCommonList = [x for x in targetNames if all([targets.count(x) >= targets.count(y) for y in targetNames])]

    if len(mostCommonList) > 1:  # return random choice if there is a tie
        return choice(mostCommonList)
    else:
        return mostCommonList

#main program for zeroR
#takes arguments -f=['csv' | 'toy' | 'mldata'] dataset_name
# the f argument specifies which type of data set we are dealing with,
# and dataset_name names which dataset if toy or mldata and filename if csv
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_name")
    parser.add_argument("-f", type=str, required=True)
    args = parser.parse_args()
    mydataset = args.dataset_name
    print args.f
    type = args.f
    if args.f == 'csv':
        csvDict = csvRead(mydataset)
        output(csvDict)
        print "ZeroR class label: ", zeroR(csvDict, type)
    if args.f == 'toy':
        csvDict = toyRead(mydataset)
        output(csvDict)
        print "ZeroR class label: ", zeroR(csvDict, type)
    if args.f == 'mldata':
        if mydataset == 'wearable-accelerometers-activity.dat':
            csvDict = mlRead(mydataset)
        else:
            csvDict = mlRead2(mydataset)
        output(csvDict)
        print "ZeroR class label: ", zeroR(csvDict, type)



