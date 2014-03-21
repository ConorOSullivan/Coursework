__author__ = 'conorosullivan'

'''
In this file, I implement my own K-nearest neighbors
algorithm.
'''



#Begin questions 2 and 3

import pandas as pd
import numpy as np
import sklearn.preprocessing
from sklearn_pandas import DataFrameMapper
import datetime
import scipy.spatial.distance as ssd
import scipy
kaggle_data = pd.DataFrame.from_csv("BioResponseKaggleTrain.csv",index_col=None)
train = kaggle_data[:3375]
test = kaggle_data[3375:]
train_features = train[train.columns[1:len(train.columns)]].astype(float)
test_features = test[test.columns[1:len(test.columns)]].astype(float)

def knn(k, data, queryPoint, trainvals):
    classList = []
    index = 0
    for element in data:
        getLabel = trainvals[index][0]
        dist = distance(queryPoint, element)
        classList.append((dist, getLabel))
        index += 1
    knaibz = sorted(classList)[:k] # list of tuples (distance, label)
    labelDict = {}
    for d, label in knaibz:
        if label not in labelDict.keys():
            labelDict[label] = 1
        else:
            labelDict[label] += 1
    return max(labelDict, key=labelDict.get)


def distance(point1, point2):
    return sum((point1-point2)**2)**0.5


def main(test_features, train_features, test, rescale=True):
    predictions = []
    if rescale:
        scaler2 = sklearn.preprocessing.StandardScaler().fit(test_features.values)
        testFeatureValues = scaler2.transform(test_features.values)
        scaler = sklearn.preprocessing.StandardScaler().fit(train_features.values)
        trainFeatureValues = scaler.transform(train_features.values)
    else:
        trainFeatureValues = train_features.values
        testFeatureValues = test_features.values
    trainingvals = train.values
    hh = 0
    for example in testFeatureValues:
        predictions.append(knn(1, trainFeatureValues, example, trainingvals))
        hh += 1
        print str(376-hh)+" to go"

    num_wrong = (predictions != test[test.columns[0]].values).sum()
    num_exs = float(len(test[test.columns[0]].values))
    score = float((num_exs-num_wrong)/num_exs)
    print 'Test set accuracy: %f' %score
    return score
print main(test_features, train_features, test)


##Begin question 4

from sklearn import cross_validation
import sklearn.neighbors
import pandas as pd
import numpy as np
wine = pd.DataFrame.from_csv("wineHeaders.csv",index_col=None)
wine_features = wine[wine.columns[1:len(wine.columns)]].astype(float)
wine_targets = wine[wine.columns[0]].astype(float)
kfold = cross_validation.KFold(len(wine_features), n_folds=5,shuffle=True)
kfoldDict = {}


for numNeighbors in range(1, 15)[::2]:
    neighb = sklearn.neighbors.KNeighborsClassifier(n_neighbors=numNeighbors)
    print "k-fold for "+str(numNeighbors)+" neighbors"
    result = [neighb.fit(np.array(wine_features)[train], np.array(wine_targets)[train]).score(np.array(wine_features)[test], np.array(wine_targets)[test]) for train, test in kfold]
    print result
    kfoldDict[numNeighbors] = sum(result)**0.5

print "The number of neighbors that produced the highest average accuracy on test data is: "+str(max(kfoldDict, key=kfoldDict.get))
