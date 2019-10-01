import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
from process_observation_data import writeToFile
import pickle

""" 
Main Menu: Get's user input and executes the selected option. 
The question the user will be asked is "has your observations data come pre-processed".

"""
def menu():
    #generate_model('sample_output.xlsx', './combined_data/combined_white_browed_treecreeper.xlsx', "white_browed_treecreeper.pkl")

    print("# --------------------------------------------------------------------")
    print("#                      MAIN MENU                                      ")
    print("# --------------------------------------------------------------------")
    print("Note: this program can be run via command line by typing 'python3 main.py <observations>'. ")
    print("\nHello! Today we'll be processing OBSERVATIONS and displaying their corresponding RELIABILITY outcomes.")
    print("Has your observations data come pre-processed? ")
    print("1. Yes")
    print("2. No")
    data_preprocessed = input("Enter response: ")

    if data_preprocessed == "1":
        print("What is the name of your observations file? Note: Accepted formats: xlsx/xls")
        file_name = input("File name: ")

        # note for the demo input: testing.xlsx
        test(file_name)

    elif data_preprocessed == "2":
        print("Alright! Pre-processing the data now. NOTE: this may take a while. Please allow a few minutes.")
        print("Input file will be sample_input.xlsx, output will be sample_output.xlsx")
        writeToFile("sample_input.xlsx", "sample_output.xlsx")

    else:

        print("Sorry. Invalid input. Valid options are: 1, 2")


def test(input_file):
    input = pd.read_excel(input_file)

    del input['TAXON_ID']
    del input['COMMON_NME']
    del input['CDE_TYPE']
    del input['RECORD_TYPE']

    input[input == np.inf] = np.nan
    input.fillna(0, inplace=True)

    clf = pickle.load(open("./models/agile_model.pkl", 'rb'))

    print("Features importance", clf.feature_importances_)

    print("\nPrinting reliability outcomes for the input file now...")

    # print prediction
    for i in range(len(input)):
        predictions = clf.predict([input.loc[i, :]])
        predicted_probs = clf.predict_proba([input.loc[i, :]])

        if predicted_probs[0][0] > 0.70:
            print("\nFor row ", i, ". The observation IS reliable")
        else:
            print("\nFor row ", i, ". The observation IS NOT reliable")

        # print("\nFor row ", i, ". Overall reliability is: ", predictions)
        print("Prediction percentages", predicted_probs[0])


""" Sample Agile Antechinus model using the random foresting method"""
def generate_model(input_file, training_file, pickle_name):
    # Input observations, run raster data through them
    # writeToFile('input_observations.xlsx', 'testing.xlsx')

    print("Calculating reliability outcomes, please wait...")

    # output of input data after being raster'ed
    input = pd.read_excel(input_file)

    # VBA data- MODEL INFORMATION
    df = pd.read_excel(training_file)  # VBA (training data)

    # get rid of unneeded values (to improve accuracy of model)
    del df['COMMON_NME']
    del df['CDE_TYPE']
    del df['RECORD_TYPE']
    del df['RELIABILITY_TXT']
    del df['SV_RECORD_COUNT']

    del input['TAXON_ID']
    del input['COMMON_NME']
    del input['CDE_TYPE']
    del input['RECORD_TYPE']

    # replace text values to numerical (for model processing
    df.RELIABILITY.replace(['Acceptable', 'Unconfirmed', 'Unreliable', 'Confirmed', 'High reliability'],
                           [int(0), int(1), int(2), int(0), int(0)], inplace=True)

    # fill n/a values - all values need to be filled for model processing
    df[df == np.inf] = np.nan
    df.fillna(0, inplace=True)

    input[input == np.inf] = np.nan
    input.fillna(0, inplace=True)

    # x data - columns
    features = df[df.columns[1:len(df.columns)]]

    # y data - what we want to predict
    y = df['RELIABILITY']

    # split to train/test dataset
    # 80% training and 20% test
    X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.20)

    # build the classifier
    clf = RandomForestClassifier(n_estimators=200, max_depth=5)

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    pickle.dump(clf, open(pickle_name, 'wb'))

    # print accuracy and feature importance
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Features importance", clf.feature_importances_)
    print("Possible reliability outcomes are: ", y.unique())

    print("\nPrinting reliability outcomes for the input file now...")

    # print prediction
    for i in range(len(input)):
        # print(input.loc[i, :])
        predictions = clf.predict([input.loc[i, :]])
        predicted_probs = clf.predict_proba([input.loc[i, :]])

        if predicted_probs[0][0] > 0.70:
            print("\nFor row ", i, ". The observation IS reliable")
        else:
            print("\nFor row ", i, ". The observation IS NOT reliable")

       # print("\nFor row ", i, ". Overall reliability is: ", predictions)
        print("Prediction percentages", predicted_probs[0])

if __name__ == "__main__":
    menu()