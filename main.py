import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
from process_observation_data import writeToFile
import pickle
import sys

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

    while True:
        # Main Menu: asks if observation file comes pre-processed
        print("\n# --------------------------------------------------------------------")
        print("#                      MAIN MENU                                      ")
        print("# --------------------------------------------------------------------")
        print("\nPlease select your choice:")
        print("1. Process observations (data is pre-processed)")
        print("2. Process observations (data is NOT pre-processed)")
        print("3. Generate/re-train a species model")
        print("4. Exit Program")

        # user enters their response
        data_preprocessed = input("\nEnter response: ")

        # YES: the excel file is pre-processed, environmental variables are tied to a location
        if data_preprocessed == "1":
            print("What is the name of your observations file? Note: Accepted formats: xlsx/xls")
            file_name = input("File name (path): ")

            # note for the demo input: testing.xlsx
            # get reliability outcomes for observation file
            get_reliability(file_name)

        # NO: the excel file is NOT pre-processed, environmentla variables are not tied to a location
        elif data_preprocessed == "2":
            correctPath = False
            while not correctPath:
                try:
                    fileInput = input("File name (path): ")
                    a = pd.read_excel(fileInput)
                    correctPath = True
                except:
                    print("Wrong input, please input the correct file path");
            print("Alright! Pre-processing the data now. NOTE: this may take a while. Please allow a few minutes.")
            print("Output will be stored in preprocess_output.xlsx")
            try:
                writeToFile(fileInput, "preprocess_output.xlsx")
                get_reliability("preprocess_output.xlsx")
            except:
                print()
                print("Error parsing File")
                print("Please make sure that your input excel file consist of the below columns only:")
                print("TAXON_ID, COMMON_NAME, RELIABILITY(EMPTY), LATITUDEDD_NUM, LONGITUDEDD_NUM, RECORD_TYPE, PRIMARY_CDE")
                sys.exit(0)
        # GENERATE/Re-train model
        elif data_preprocessed == "3":
            path = "./balancing_dataset/excel_files/combined_data/"

            models = {
                "1": (path + "combined_agile_antechinus.xlsx", "agile_model.pkl"),
                "2": (path + "combined_beard_heath.xlsx", "beard_heath_model.pkl"),
                "3": (path + "combined_brown_treecrepper.xlsx", "brown_treecreeper_model.pkl"),
                "4": (path + "combined_small_triggerplant.xlsx", "small_triggerplant.pkl"),
                "5": (path + "combined_southern_brown_tree_frog.xlsx", "southern_brown_tree_frog.pkl"),
                "6": (path + "combined_white_browed_treecreeper.xlsx", "white_browed_treecreeper.pkl"),
            }
            print("\nWhich model do you want to generate?")
            print("1. Agile Antechinus")
            print("2. Common Beard-hearth")
            print("3. Brown Treecreeper")
            print("4. Small Triggerplant")
            print("5. Southern Brown Tree frog")
            print("6. White Browed Treecreeper")
            choice = input("Enter choice: ")

            generate_model(models[choice][0], models[choice][1])
        # exit program
        elif data_preprocessed == "4":
            break
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

    inputCorrect = False
    while not inputCorrect:
        try:
            # reads input file
            file = pd.read_excel(input_file)
            inputCorrect = True
        except:
            print("Wrong input, please input the correct file path")
            input_file = input("File name (path): ")

    # gets rid of unnecessary columns
    del file['CDE_TYPE']
    del file['RECORD_TYPE']

    # fills in missing data
    file[file == np.inf] = np.nan
    file.fillna(0, inplace=True)

    #print("Features importance", clf.feature_importances_)

    # iterates through each row in the excel file
    for i in range(len(file)):
        # reads species name, as well as long/lat location
        species = file.iloc[i, 1]
        lat = file.iloc[i, 3]
        long = file.iloc[i, 4]

        # the likelihood of an observation being reliable
        predicted_probs = None

        # runs observation through appropriate species model
        # for instance if the observation is for the species "Agile Antechinus", then the observation will be processed
        # through the Agile Antechinus model
        if species == "Agile Antechinus":
            predicted_probs = agile_antechinus.predict_proba([file.iloc[i, 2:]])
        elif species == "Common Beard-heath":
            predicted_probs = beard_heath.predict_proba([file.iloc[i, 2:]])
        elif species == "Small Triggerplant":
            predicted_probs = small_triggerplant.predict_proba([file.iloc[i, 2:]])
        elif species == "Southern Brown Tree Frog":
            predicted_probs = southern_brown_tree_frog.predict_proba([file.iloc[i, 2:]])
        elif species == "Brown Treecreeper":
            predicted_probs = brown_treecreeper.predict_proba([file.iloc[i, 2:]])
        elif species == "White-browed Treecreeper":
            predicted_probs = white_browed_treecreeper.predict_proba([file.iloc[i, 2:]])
        else:
            print("Sorry! No available data for ", species)
            continue

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
def generate_model(training_file, pickle_name):
    # Input observations, run raster data through them
    # writeToFile('input_observations.xlsx', 'testing.xlsx')

    print("Generating model, please wait...")

    # VBA data- MODEL INFORMATION
    df = pd.read_excel(training_file)  # VBA (training data)

    # get rid of unneeded values (to improve accuracy of model)
    del df['COMMON_NME']
    del df['CDE_TYPE']
    del df['RECORD_TYPE']
    del df['RELIABILITY_TXT']
    del df['SV_RECORD_COUNT']

    # replace text values to numerical (for model processing
    df.RELIABILITY.replace(['Acceptable', 'Unconfirmed', 'Unreliable', 'Confirmed', 'High reliability'],
                           [int(0), int(1), int(2), int(0), int(0)], inplace=True)

    # fill n/a values - all values need to be filled for model processing
    df[df == np.inf] = np.nan
    df.fillna(0, inplace=True)

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

    path = "./models/" + pickle_name
    pickle.dump(clf, open(path, 'wb'))

    # print accuracy and feature importance
    #print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    #print("Possible reliability outcomes are: ", y.unique())

    print("Finished generating model!! Your model is called ", pickle_name, ". Path to location of model generated: ", path)
if __name__ == "__main__":
    menu()