import pandas as pd
import numpy as np
from sklearn.datasets.species_distributions import construct_grids
import graphviz
from sklearn import datasets, tree
import matplotlib.pyplot as plt
import geopy.distance
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn import metrics
from sklearn.model_selection import train_test_split


df = pd.read_excel('../VBA_Raster.xlsx') # VBA

# get rid of string values (temporary)

del df['RELIABILITY']
del df['COMMON_NME']
del df['RELIABILITY_TXT']
del df['RECORD_TYPE']
del df['SV_RECORD_COUNT']

# get only agile antechinus values
# df = df[df['TAXON_ID'] == 11028]

df.CDE_TYPE.replace(['FLORA', 'FAUNA'],
                       [0, 1], inplace=True)


#x data
features = df[df.columns[1:23]]

#y data
y=df['TAXON_ID']
print(features)
# split to train/test dataset
X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.05) # 70% training and 30% test

#build the classifier
clf = RandomForestClassifier()

clf.fit(X_train,y_train)

y_pred=clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

print(clf.predict([[142.72417,
                    -37.00972,
                    6,
                    16.2590999603271,
                    2000.8466796875,
                    1933.11975097656,
                    28.6844997406006,
                    73.3154983520508,
                    28.6844997406006,
                    317.333099365234,
                    13.9718742370606,
                    0.102355808019638,
                    0.00100000004749745,
                    1.88199996948242,
                    6,
                    96,
                    0.0773999989032745,
                    35,
                    121,
                    0.000300000014249235,
                    231.800003051758, 0
                    ]]))

#
# print(df)