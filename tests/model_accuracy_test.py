import pickle
import sys
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import unittest
import numpy as np
from sklearn.model_selection import train_test_split

'''
Class that tests the model Accuracy
Our team has decided that model accuracy should be above 90%
Hence, we are checking whether all models using the testing data acheived 90% or above accuracy rate
'''
class TestModelAccuracy(unittest.TestCase):

    '''
    Function that generate the accuracy to the testing data for each species.
    First preprocess the corresponding testing file
    Run the testing data in the model
    Generate score using pickle
    '''
    def generateAccuracy(self, excelFile, model):
        df = pd.read_excel(excelFile)

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


        features = df[df.columns[1:len(df.columns)]]
        y = df['RELIABILITY']
        X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.20)

        # build the classifier
        clf = RandomForestClassifier(n_estimators=200, max_depth=5)

        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        # print accuracy and feature importance
        score = metrics.accuracy_score(y_test, y_pred)
        return score * 100

    '''
    Function that tests the agile antechinus model accuracy
    Want to make sure accuracy above 90%
    '''
    def test_agile_antechinus_accuracy(self):
        agile_antechinus = pickle.load(open("./models/agile_model.pkl", 'rb'))
        self.assertGreaterEqual(self.generateAccuracy('./balancing_dataset/excel_files/combined_data/combined_agile_antechinus.xlsx', agile_antechinus), 90)

    '''
    Function that tests the beard heath model accuracy
    Want to make sure accuracy above 90%
    '''    
    def test_beard_heath_accuracy(self):
        beard_heath = pickle.load(open("./models/beard_heath_model.pkl", 'rb'))
        self.assertGreaterEqual(self.generateAccuracy('./balancing_dataset/excel_files/combined_data/combined_beard_heath.xlsx', beard_heath), 90)

    '''
    Function that tests the brown tree creeper accuracy model accuracy
    Want to make sure accuracy above 90%
    '''
    def test_brown_tree_creeper_accuracy(self):
        brown_treecreeper = pickle.load(open("./models/brown_treecreeper_model.pkl", 'rb'))
        self.assertGreaterEqual(self.generateAccuracy('./balancing_dataset/excel_files/combined_data/combined_brown_treecrepper.xlsx', brown_treecreeper), 90)
        
    '''
    Function that tests the small triggerplant model accuracy
    Want to make sure accuracy above 90%
    '''
    def test_small_triggerplant_accuracy(self):
        small_triggerplant = pickle.load(open("./models/small_triggerplant.pkl", 'rb'))
        self.assertGreaterEqual(self.generateAccuracy('./balancing_dataset/excel_files/combined_data/combined_small_triggerplant.xlsx', small_triggerplant), 90)

    '''
    Function that tests the southern brown tree frog model accuracy
    Want to make sure accuracy above 90%
    '''
    def test_southern_brown_tree_frog_accuracy(self):
        southern_brown_tree_frog = pickle.load(open("./models/southern_brown_tree_frog.pkl", 'rb'))
        self.assertGreaterEqual(self.generateAccuracy('./balancing_dataset/excel_files/combined_data/combined_southern_brown_tree_frog.xlsx', southern_brown_tree_frog), 90)
    
    '''
    Function that tests the white browed treecreeper accuracy model accuracy
    Want to make sure accuracy above 90%
    '''
    def test_white_browed_treecreeper_accuracy(self):
        white_browed_treecreeper = pickle.load(open("./models/white_browed_treecreeper.pkl", 'rb'))
        self.assertGreaterEqual(self.generateAccuracy('./balancing_dataset/excel_files/combined_data/combined_white_browed_treecreeper.xlsx',white_browed_treecreeper), 90 )

if __name__ == '__main__':
    unittest.main()
    