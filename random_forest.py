import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
from extract_environmental_variables import writeToFile

# Input observations, run raster data through them
# writeToFile('input_observations.xlsx', 'testing.xlsx')

# output of input data after being raster'ed
input = pd.read_excel('testing.xlsx')

# VBA data- MODEL INFORMATION
df = pd.read_excel('VBA_Raster.xlsx') # VBA (training data)

# get rid of unneeded values (to improve accuracy of model)
del df['RELIABILITY']
del df['COMMON_NME']
del df['RELIABILITY_TXT']
del df['SV_RECORD_COUNT']
del df['WETNESS']
del df['PROTECTION_INDEX']

# del df['RECORD_TYPE']

taxon_id = input['TAXON_ID']

del input['TAXON_ID']
del input['COMMON_NME']
del input['WETNESS']
del input['PROTECTION_INDEX']

# del input['RECORD_TYPE']

# get only agile antechinus values
# df = df[df['TAXON_ID'] == 11028]

# turn string values to numbers
df.CDE_TYPE.replace(['FLORA', 'FAUNA'],
                       [0, 1], inplace=True)

input.CDE_TYPE.replace(['FLORA', 'FAUNA'],
                       [0, 1], inplace=True)

df.RECORD_TYPE.replace(['Seen', 'Observation', 'Captured and released', 'Heard', '#NUM!', 'Identified from hair or scats',
                        'Observation with supporting evidence', 'Indirect evidence', 'Museum specimen', 'Pers. Comm.',
                        'Monitored species', 'Captured', 'Literature'],
                       [0, 1,2,3,4,5,6,7,8,9,10,11,12], inplace=True)

input.RECORD_TYPE.replace(['Seen', 'Observation', 'Captured and released', 'Heard', '#NUM!', 'Identified from hair or scats',
                           'Observation with supporting evidence', 'Indirect evidence', 'Museum specimen', 'Pers. Comm.',
                           'Monitored species', 'Captured', 'Literature'],
                       [0, 1,2,3,4,5,6,7,8,9,10,11,12], inplace=True)

# fill na values with mean
df[df==np.inf]=np.nan
df.fillna(df.mean(), inplace=True)

input[input==np.inf]=np.nan
input.fillna(input.mean(), inplace=True)

#x data - columns
features = df[df.columns[1:len(df.columns)]]

#y data - what we want to predict
y=df['TAXON_ID']
print("calculating observation result...")
# split to train/test dataset
X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.05) # 70% training and 30% test
#build the classifier
clf = RandomForestClassifier(n_estimators=200)

clf.fit(X_train,y_train)
y_pred=clf.predict(X_test)

# print accuracy and feature importance
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Features importance", clf.feature_importances_)

# print prediction
for i in range(len(input)):
   # print(input.loc[i, :])
   print("Observer thought species was:", taxon_id[i], " Predicted species is: ", clf.predict([input.loc[i,:]]))

#
# # print(df)