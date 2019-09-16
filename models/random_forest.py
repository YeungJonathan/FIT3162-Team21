import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split

# read file containing raster data
df = pd.read_excel('../VBA_Raster.xlsx')

# get rid of unneeded values (to improve accuracy of model)
del df['RELIABILITY']
del df['COMMON_NME']
del df['RELIABILITY_TXT']
del df['RECORD_TYPE']
del df['SV_RECORD_COUNT']
del df['WETNESS']
del df['PROTECTION_INDEX']

# get only agile antechinus values
# df = df[df['TAXON_ID'] == 11028]

# turn string values to numbers
df.CDE_TYPE.replace(['FLORA', 'FAUNA'],
                       [0, 1], inplace=True)


#x data - columns
features = df[df.columns[1:23]]

#y data - what we want to predict
y=df['TAXON_ID']
print("calculating observation result...")
# split to train/test dataset
X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.05) # 70% training and 30% test

#build the classifier
clf = RandomForestClassifier(n_estimators=200)

clf.fit(X_train,y_train)

y_pred=clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

print(clf.feature_importances_)

print(clf.predict([[142.72417,
                    -37.00972,
                    6,
                    2000.8466796875,
                    1933.11975097656,
                    28.6844997406006,
                    73.3154983520508,
                    28.6844997406006,
                    317.333099365234,
                    13.9718742370606,
                    0.102355808019638,
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