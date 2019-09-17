import numpy as np
import pandas as pd
import xlsxwriter
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest


vba = pd.read_excel('VBA_Raster.xlsx') # VBA (training data)
allLat = vba["LATITUDEDD_NUM"]
allLong = vba["LONGITUDEDD_NUM"]

maxLat = allLat.max()
minLat = allLat.min()

maxLong = allLong.max()
minLong = allLong.min()

speciesName = 'Agile Antechinus'
ufi = vba.loc[vba['COMMON_NME'] == speciesName]

dataList = []
longList = []
latList = []
taxonID = 0;

for index, row in ufi.iterrows():
    if taxonID == 0:
        taxonID = row['TAXON_ID']
    LONGITUDEDD_NUM = row['LONGITUDEDD_NUM']
    LATITUDEDD_NUM = row['LATITUDEDD_NUM']
    longList.append(LONGITUDEDD_NUM)
    latList.append(LATITUDEDD_NUM)
    dataList.append([LATITUDEDD_NUM, LONGITUDEDD_NUM])

rng = np.random.RandomState(42)

# # Generate some abnormal novel observations
lat_outliers = rng.uniform(low=minLat, high=maxLat, size=(100 , 1))
long_outliers = rng.uniform(low=minLong, high=maxLong, size=(100, 1))

outliers = []
for i in range(len(lat_outliers)):
    outliers.append((lat_outliers[i][0], long_outliers[i][0]))


# fit the model
clf = IsolationForest(behaviour='new', max_samples=6573,
                    n_estimators = 300,
                    random_state=rng, contamination='auto')

clf.fit(dataList)
# y_pred_outliers = clf.fit_predict(outliers)
y_pred_outliers = clf.predict(outliers)
y_predict_long = []
y_predict_lat = []
for index in range(len(y_pred_outliers)):
    if y_pred_outliers[index] == -1:
        y_predict_lat.append(outliers[index][0])
        y_predict_long.append(outliers[index][1])


print('lat', minLat, maxLat)
print('long', minLong, maxLong)

# plot the line, the samples, and the nearest vectors to the plane
xx, yy = np.meshgrid(np.linspace(minLat, maxLat, 50), np.linspace(minLong, maxLong, 50))
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.title("IsolationForest")
plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)


b1 = plt.scatter(latList, longList, c='white',
                 s=20, edgecolor='k')
c = plt.scatter(y_predict_lat, y_predict_long, c='red',
                s=20, edgecolor='k')
plt.axis('tight')
plt.xlim((minLat, maxLat))
plt.ylim((minLong, maxLong))
plt.legend([b1, c],
           ["training observations",
            "new regular observations", "new abnormal observations"],
           loc="upper left")
plt.show()








# workbook = xlsxwriter.Workbook('pseudo_absence_data.xlsx', {'nan_inf_to_errors': True})
# worksheet = workbook.add_worksheet()

# # VBA_data we want
# worksheet.write('A1', 'TAXON_ID')
# worksheet.write('B1', 'COMMON_NME')
# worksheet.write('C1', 'RELIABILITY')
# worksheet.write('D1', 'RELIABILITY_TXT')
# worksheet.write('E1', 'LATITUDEDD_NUM')
# worksheet.write('F1', 'LONGITUDEDD_NUM')

# row = 1
# col = 0

# for index in range(len(y_predict_lat)):
#     current_lat = y_predict_lat[index]
#     current_long = y_predict_long[index]

#     worksheet.write(row, col, taxonID)
#     worksheet.write(row, col + 1, speciesName)
#     worksheet.write(row, col + 2, 'Unreliable')
#     worksheet.write(row, col + 3, 'Pseudo Absence')
#     worksheet.write(row, col + 4, current_lat)
#     worksheet.write(row, col + 5, current_long)
#     row += 1

# workbook.close()