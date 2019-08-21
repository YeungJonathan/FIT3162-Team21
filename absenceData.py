import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest


vba = pd.read_excel('VBA_Raster.xlsx') # VBA (training data)
ufi = vba.loc[vba['COMMON_NME'] == 'Agile Antechinus']

dataList = []
longList = []
latList = []
for index, row in ufi.iterrows():
    LONGITUDEDD_NUM = row['LONGITUDEDD_NUM']
    LATITUDEDD_NUM = row['LATITUDEDD_NUM']
    longList.append(LONGITUDEDD_NUM)
    latList.append(LATITUDEDD_NUM)
    dataList.append([LATITUDEDD_NUM, LONGITUDEDD_NUM])

rng = np.random.RandomState(42)

# # Generate some abnormal novel observations
X_outliers = rng.uniform(low=min(latList)-2, high=max(longList), size=( 400000 , 2))

# fit the model
clf = IsolationForest(behaviour='new', max_samples=6573,
                    n_estimators = 300,
                    random_state=rng, contamination='auto')

clf.fit(dataList)
# y_pred_outliers = clf.predict(X_outliers)
y_pred_outliers = clf.fit_predict(X_outliers)
y_predict_long = []
y_predict_lat = []
for index in range(len(y_pred_outliers)):
    if y_pred_outliers[index] == -1:
        y_predict_lat.append(X_outliers[index][0])
        y_predict_long.append(X_outliers[index][1])

# plot the line, the samples, and the nearest vectors to the plane
xx, yy = np.meshgrid(np.linspace(min(latList) - 2, max(latList)+2, 50), np.linspace(min(longList)-2, max(longList)+2, 50))
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.title("IsolationForest")
plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)


b1 = plt.scatter(latList, longList, c='white',
                 s=20, edgecolor='k')
c = plt.scatter(y_predict_lat, y_predict_long, c='red',
                s=20, edgecolor='k')
plt.axis('tight')
plt.xlim((min(latList)-2, max(latList)+2))
plt.ylim((min(longList)-2, max(longList)+2))
plt.legend([b1, c],
           ["training observations",
            "new regular observations", "new abnormal observations"],
           loc="upper left")
plt.show()