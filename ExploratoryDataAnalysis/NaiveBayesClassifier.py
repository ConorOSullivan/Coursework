'''
In this code, I take in all of the files from
the directory txt_sentoken and train a Naive Bayes
classifier on a selection of them. I take the remaining
files and run them through the classifier, keeping track
of if it is a successful prediction or not.
'''


import argparse
import re
import os
import csv
import random
import collections
import math


# Stop word list
stopWords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also',
             'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be',
             'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear',
             'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for',
             'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers',
             'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is',
             'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may',
             'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor',
             'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our',
             'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since',
             'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then',
             'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us',
             've', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
             'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet',
             'you', 'your']


def parseArgument():
    """
    Code for parsing arguments
    """
    parser = argparse.ArgumentParser(description='Parsing a file.')
    parser.add_argument('-d', nargs=1, required=True)
    args = vars(parser.parse_args())
    return args

def getFileContent(filename):
    """
    Retrieve file content
    """
    input_file = open(filename, 'r')
    text = input_file.read()
    text = re.sub(r'[^\w\s]|\d+', '', text)
    input_file.close()
    return text


def parseFile2(text, words_dic, sent):
    """
    Adds the words in the text to the dictionary
    """
    wordlist = text.split()  # split on spaces
    for word in wordlist:  # iterate over words
        # check if alphanumeric, if word length over 2 and word not one of the stopWords
        if word.isalnum() and len(word) >= 2 and word not in stopWords:
            # set value to 1 if not in dict, add 1 to value if in dict
            words_dic[sent][word] = words_dic[sent].get(word, 0) + 1

    return words_dic


def returnFileDict(text):
    '''
    This returns a dictionary of words and the count of each word for each file in the
    test set.
    '''
    dict = {}
    text = re.sub(r'[^\w\s]|\d+', '', text)
    textWords = text.split()
    for word in textWords:
        if word not in stopWords:
            dict[word] = textWords.count(word)
    return dict


def calculateProbability(fileDict, words_dic, vlength):
    p = 0
    word_total = sum(words_dic.values())
    for word in fileDict:
        if word in words_dic:
            p += fileDict[word]*math.log((words_dic[word]+1.0)/(word_total + vlength))
        if word not in words_dic:
            p += fileDict[word]*math.log((1.0/(word_total + vlength)))
    return p


def predictClass(fileDict, words_dic, vlength, docprob):
    p = []
    p.append(math.log(docprob['neg'])+calculateProbability(fileDict, words_dic['neg'], vlength))
    p.append(math.log(docprob['pos'])+calculateProbability(fileDict, words_dic['pos'], vlength))
    if p[0] == max(p):
        guess = 'neg'
    else:
        guess = 'pos'
    return guess

def printIterationOutput(lenlist, i, test, correctGuesses):
    '''
    This outputs the necessary information about length of the test set,
    number of current iterations, and number of correct guesses
    '''
    print "iteration %d" % (int(i)+1)
    print "num_pos_test_docs:%d" % len(test['pos'])
    print "num_pos_training_docs:%d" % (lenlist - len(test['pos']))
    print "num_pos_correct_docs:%d" % correctGuesses['pos']
    print "num_neg_test_docs:%d" % len(test['neg'])
    print "num_neg_training_docs:%d" % (lenlist - len(test['neg']))
    print "num_neg_correct_docs:%d" % correctGuesses['neg']
    accuracy = float((correctGuesses['neg'] + correctGuesses['pos']))/(len(test['pos'])+len(test['neg']))
    print "accuracy: {:.2%}".format(accuracy)
    return accuracy


def main():
    args = parseArgument()
    directory = args['d'][0]
    aveaccuracy = 0
    for i in range(0,3):
        words_dic = {}  # initializing words dictionary
        words_dic['neg'] = {}  # initializing subdictionaries
        words_dic['pos'] = {}
        test = {}
        for folder in os.listdir(directory):
            if folder == 'neg' or folder == 'pos':
                fileList = os.listdir("".join([directory+"/"+folder]))
                random.shuffle(fileList)
                train = fileList[:667]
                test[folder] = fileList[667:]
                for file in train:  # add neg words to dict
                    #print file
                    text = getFileContent("/".join([directory, folder, file]))  # get words in file
                    words_dic = parseFile2(text, words_dic, folder)  # add words to dict

        docprob = {}
        docprob['pos'] = .5
        docprob['neg'] = .5
        correctGuesses = {}
        correctGuesses['pos'] = 0
        correctGuesses['neg'] = 0
        lenlist = len(fileList)  # get length of total list in order to display len of test/training sets
        # get length of vocabulary
        vlength = float(len(dict(list(words_dic['pos'].items()) + list(words_dic['neg'].items()))))
        # go through neg and pos folders in test dictionary
        for folder in test:
            # go through each file in each dictionary
            for file in test[folder]:
                # get file's text
                text = getFileContent("/".join([directory, folder, file]))
                # create a dictionary out of that text
                fileDict = returnFileDict(text)
                # return a string that is the guess
                guess = predictClass(fileDict, words_dic, vlength, docprob)
                # if guess is the same as the test folder we're in, that's a correct guess
                if guess == folder:
                    correctGuesses[folder] += 1
        # store value of accuracy so we can make average after iterations
        accuracy = printIterationOutput(lenlist, i, test, correctGuesses)
        aveaccuracy += accuracy
    # compute average accuracy
    aveaccuracy /= float(i + 1)
    print "ave_accuracy: {:.2%}".format(aveaccuracy)


main()