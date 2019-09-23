import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
from extract_environmental_variables import writeToFile

def menu():
    print("# --------------------------------------------------------------------")
    print("#                      MAIN MENU                                      ")
    print("# --------------------------------------------------------------------")
    print("Note: in the future you can type 'python3 main.py <observations>' to directly get observation results")

    # Input observations, run raster data through them
    # writeToFile('input_observations.xlsx', 'testing.xlsx')

    # output of input data after being raster'ed
    input = pd.read_excel('testing.xlsx')

    # VBA data- MODEL INFORMATION
    df = pd.read_excel('./combined_data/combined_agile_antechinus.xlsx')  # VBA (training data)

    # get rid of unneeded values (to improve accuracy of model)

    del df['COMMON_NME']
    del df['CDE_TYPE']
    del df['RECORD_TYPE']
    del df['RELIABILITY_TXT']
    del df['SV_RECORD_COUNT']

    del input['COMMON_NME']
    del input['CDE_TYPE']
    del input['RECORD_TYPE']
    del input['RELIABILITY_TXT']
    del input['SV_RECORD_COUNT']

    print(df.columns)
    print(input.columns)

    # del input['RECORD_TYPE']

    # get only agile antechinus values
    # df = df[df['TAXON_ID'] == 11028]

    df.RELIABILITY.replace(['Acceptable', 'Unconfirmed', 'Unreliable', 'Confirmed', 'High reliability'],
                           [int(0), int(1), int(2), int(0), int(0)], inplace=True)
    # fill na values with mean
    df[df == np.inf] = np.nan
    df.fillna(0, inplace=True)

    input[input == np.inf] = np.nan
    input.fillna(0, inplace=True)

    # x data - columns
    features = df[df.columns[1:len(df.columns)]]

    # y data - what we want to predict
    y = df['RELIABILITY']
    print("calculating observation result...")
    # split to train/test dataset
    X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.20)  # 70% training and 30% test
    # build the classifier
    clf = RandomForestClassifier(n_estimators=200)

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    # print accuracy and feature importance
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Features importance", clf.feature_importances_)
    print("Possible species", y.unique())

    # print prediction
    for i in range(len(input)):
        # print(input.loc[i, :])
        predictions = clf.predict([input.loc[i, :]])
        predicted_probs = clf.predict_proba([input.loc[i, :]])

        print(" Predicted species is: ", predictions)
        print("Prediction percentages", predicted_probs)

if __name__ == "__main__":
    menu()