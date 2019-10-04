import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
from process_observation_data import writeToFile
import pickle

"""
Models: they are already generated, we are simply loading them in from memory
"""
agile_antechinus = pickle.load(open("./models/agile_model.pkl", 'rb'))
beard_heath = pickle.load(open("./models/beard_heath_model.pkl", 'rb'))
brown_treecreeper = pickle.load(open("./models/brown_treecreeper_model.pkl", 'rb'))
small_triggerplant = pickle.load(open("./models/small_triggerplant.pkl", 'rb'))
southern_brown_tree_frog = pickle.load(open("./models/southern_brown_tree_frog.pkl", 'rb'))
white_browed_treecreeper = pickle.load(open("./models/white_browed_treecreeper.pkl", 'rb'))

""" 
Main Menu: Get's user input and executes the selected option. 
The question the user will be asked is "has your observations data come pre-processed".
This means:
- does the observation file contain corresponding environmental variables that are tied to a location
- or in other words, has the observation file been processed through the raster function

For instance a file where a row contains SPECIES | LONG | LAT, and no corresponding environmental variables
tied to the long/lat location would NOT be considered pre-processed. 

Whereas a file where a row contains SPECIES | LONG | LAT | WETNESS | RAINFALL | HEAT would be considered
pre-processed as variables such as wetness/rainfall/heat are environmental variables, signifying that the
file HAS been run through the raster function.
"""
def menu():
    #generate_model('sample_output.xlsx', './combined_data/combined_white_browed_treecreeper.xlsx', "white_browed_treecreeper.pkl")

    # Main Menu: asks if observation file comes pre-processed
    print("# --------------------------------------------------------------------")
    print("#                      MAIN MENU                                      ")
    print("# --------------------------------------------------------------------")
    print("Note: this program can be run via command line by typing 'python3 main.py <observations>'. ")
    print("\nHello! Today we'll be processing OBSERVATIONS and displaying their corresponding RELIABILITY outcomes.")
    print("Has your observations data come pre-processed? ")
    print("1. Yes")
    print("2. No")

    # user enters their response
    data_preprocessed = input("Enter response: ")

    # YES: the excel file is pre-processed, environmental variables are tied to a location
    if data_preprocessed == "1":
        print("What is the name of your observations file? Note: Accepted formats: xlsx/xls")
        file_name = input("File name: ")

        # note for the demo input: testing.xlsx
        # get reliability outcomes for observation file
        get_reliability(file_name)

    # NO: the excel file is NOT pre-processed, environmentla variables are not tied to a location
    elif data_preprocessed == "2":
        print("Alright! Pre-processing the data now. NOTE: this may take a while. Please allow a few minutes.")
        print("Input file will be sample_input.xlsx, output will be sample_output.xlsx")
        writeToFile("sample_input.xlsx", "sample_output.xlsx")

    # invalid response by the user
    else:

        print("Sorry. Invalid input. Valid options are: 1, 2")


"""
Outputs the reliability for each observation in a file. For each species observation, it will be run through the
appropriate model. For instance if the observation is for the species "Red Kangaroo", then the observation will be 
processed through the Red Kangaroo model. We want to see how reliable an observation is, in the context of the species.

@param input_file, a file containing a list of observations. i.e it was claimed the species "x", was seen at this 
                   long/lat location
"""
def get_reliability(input_file):

    # reads input file
    input = pd.read_excel(input_file)

    # gets rid of unnecessary columns
    del input['CDE_TYPE']
    del input['RECORD_TYPE']

    # fills in missing data
    input[input == np.inf] = np.nan
    input.fillna(0, inplace=True)

    #print("Features importance", clf.feature_importances_)

    # iterates through each row in the excel file
    for i in range(len(input)):
        # reads species name, as well as long/lat location
        species = input.iloc[i, 1]
        lat = input.iloc[i, 3]
        long = input.iloc[i, 4]

        # the likelihood of an observation being reliable
        predicted_probs = None

        # runs observation through appropriate species model
        # for instance if the observation is for the species "Agile Antechinus", then the observation will be processed
        # through the Agile Antechinus model
        if species == "Agile Antechinus":
            predicted_probs = agile_antechinus.predict_proba([input.iloc[i, 2:]])
        elif species == "Common Beard-heath":
            predicted_probs = beard_heath.predict_proba([input.iloc[i, 2:]])
        elif species == "Small Triggerplant":
            predicted_probs = small_triggerplant.predict_proba([input.iloc[i, 2:]])
        elif species == "Southern Brown Tree Frog":
            predicted_probs = southern_brown_tree_frog.predict_proba([input.iloc[i, 2:]])
        elif species == "Brown Treecreeper":
            predicted_probs = brown_treecreeper.predict_proba([input.iloc[i, 2:]])
        elif species == "White-browed Treecreeper":
            predicted_probs = white_browed_treecreeper.predict_proba([input.iloc[i, 2:]])

        # For instance, the Frog was seen at -38.123, 144.1293
        print("\n",species, "was seen at", lat, long)

        # if a species at a given location is predicted to be reliable x% of the time
        if predicted_probs[0][0] > 0.70:
            print(" The observation IS reliable")
        else:
            print(" The observation IS NOT reliable")

        # How the decision tree was split
        print(" Prediction percentages", predicted_probs[0])


""" 
Generates a model for a particular species. The model will be stored in a 'pkl' file.
@param input_file, observations file. Each row for a given observation will be given a reliability rating. This param 
       isn't really needed for the generation of the model, but is a good visualisation tool
@param training file, contains information about a particular species. We will be using this information in order to
       train our file
@param pickle_name, the name that our model will be called. We are storing the model locally, so that we do not need to
       regenerate the model everytime.
"""
def generate_model(input_file, training_file, pickle_name):
    # Input observations, run raster data through them
    # writeToFile('input_observations.xlsx', 'testing.xlsx')

    print("Generating model, please wait...")

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
    #print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    #print("Features importance", clf.feature_importances_)
    #print("Possible reliability outcomes are: ", y.unique())

    print("Finished generating model!!")
if __name__ == "__main__":
    menu()