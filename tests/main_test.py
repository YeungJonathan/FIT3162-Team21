import sys
import os
import openpyxl
sys.path.append(os.path.abspath('./'))
import io
from main import menu
from unittest.mock import patch
from unittest.mock import Mock
import unittest
import builtins

'''
This test file is used to test the CLI correctness
Model and observation reliability is not tested in this class.
Make sure you are in root directory when running this test
To run the test:
    python main_test.py
'''
class TestCLI(unittest.TestCase):

    assertReturnString = "# --------------------------------------------------------------------\n"
    assertReturnString += ("#                      MAIN MENU                                      \n")
    assertReturnString+= ("# --------------------------------------------------------------------\n")
    assertReturnString+= "Note: this program can be run via command line by typing 'python3 main.py <observations>'. \n"
    assertReturnString+= "\nHello! Today we'll be processing OBSERVATIONS and displaying their corresponding RELIABILITY outcomes.\n"
    assertReturnString+= ("Has your observations data come pre-processed with raster files?\n")
    assertReturnString+= ("1. Yes\n")
    assertReturnString+= ("2. No\n")


    '''
    Function to test all correct user input (no wrong inputs)
    Input excel file includes a reliable observation taken from the VBA file.
    '''
    def test_CLI_correct_first_print(self):
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput  
        with unittest.mock.patch('builtins.input', side_effect=['1', './tests/testing_data_excel/testing_reliable.xlsx']):
            menu()
        sys.stdout = sys.__stdout__
        assertString = self.assertReturnString
        assertString += "What is the name of your observations file? Note: Accepted formats: xlsx/xls\n\n"
        assertString += " Agile Antechinus was seen at -38.35598 144.96925\n"
        assertString += " The observation IS reliable\n"
        assertString += " Prediction percentages [0.97730358 0.00852486 0.01417156]\n"
        self.assertEqual(capturedOutput.getvalue(), assertString)


    '''
    Function to test 1 wrong user input. 
    Second user input is wrong -- Path of the input file should be correct
    Expected Output: Program should prompt user input file path until path correct.
                     Should still be able to output reliable results as third input is a correct path
    Input excel file includes a reliable observation taken from the VBA file.
    '''
    def test_CLI_wrong_second_output(self):
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput  
        with unittest.mock.patch('builtins.input', side_effect=['1', '2', './tests/testing_data_excel/testing_reliable.xlsx']):
            menu()
        sys.stdout = sys.__stdout__
        assertString = self.assertReturnString
        assertString += "What is the name of your observations file? Note: Accepted formats: xlsx/xls\n"
        assertString += "Wrong input, please input the correct file path\n\n"
        assertString += " Agile Antechinus was seen at -38.35598 144.96925\n"
        assertString += " The observation IS reliable\n"
        assertString += " Prediction percentages [0.97730358 0.00852486 0.01417156]\n"
        self.assertEqual(capturedOutput.getvalue(), assertString)


    '''
    Function to test multiple wrong user input. 
    Second, third and forth user input is wrong -- Path of the input file should be correct
    Expected Output: Program should prompt user input file path until user input correct path.
                     Should still be able to output reliable results as third input is a correct path
    Input excel file includes a reliable observation taken from the VBA file.
    '''
    def test_CLI_multiple_wrong_output(self):
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput  
        with unittest.mock.patch('builtins.input', side_effect=['1', '2', 'Random Path','./tests/testing_data_excel/testing_reliable_wrong.xlsx', './tests/testing_data_excel/testing_reliable.xlsx']):
            menu()
        sys.stdout = sys.__stdout__
        assertString = self.assertReturnString
        assertString += "What is the name of your observations file? Note: Accepted formats: xlsx/xls\n"
        assertString += "Wrong input, please input the correct file path\n"
        assertString += "Wrong input, please input the correct file path\n"
        assertString += "Wrong input, please input the correct file path\n\n"
        assertString += " Agile Antechinus was seen at -38.35598 144.96925\n"
        assertString += " The observation IS reliable\n"
        assertString += " Prediction percentages [0.97730358 0.00852486 0.01417156]\n"
        self.assertEqual(capturedOutput.getvalue(), assertString)


    '''
    Function that simulates wrong user input on first input.
    First input must be 1 or 2 but we are testing values of 3
    Expected Output: Prints "Sorry. Invalid input. Valid options are: 1, 2".
    '''
    @patch('main.input', return_value='3')
    def test_CLI_wrong_first_input(self, input):
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput  
        menu()
        sys.stdout = sys.__stdout__
        assertString = self.assertReturnString
        assertString+= "Sorry. Invalid input. Valid options are: 1, 2\n"
        self.assertEqual(capturedOutput.getvalue(), assertString)


    '''
    Function that simulates user input "2" for first input.
    user input "2" in first arguement means that user has not preprocess the data
    This will then prompt user to input excel file path
    The input excel Path for this test should be correct
    Since we are testing whether it will ouput correctly if we input a correct path
    Expected Output: Predicts correctly.
    '''
    def testing_cli_2_correct_file(self):
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput  
        with unittest.mock.patch('builtins.input', side_effect=['2', './tests/testing_data_excel/testing_cli_2_correct.xlsx']):
            menu()
        sys.stdout = sys.__stdout__
        assertString = self.assertReturnString

        assertString += "Alright! Pre-processing the data now. NOTE: this may take a while. Please allow a few minutes.\n"
        assertString += "Output will be stored in preprocess_output.xlsx\n\n"
        assertString += " Agile Antechinus was seen at -38.35692 144.97151\n"
        assertString += " The observation IS reliable\n"
        assertString += " Prediction percentages [0.98567279 0.00762248 0.00670473]\n\n"

        assertString += " Agile Antechinus was seen at -38.35598 144.96925\n"
        assertString += " The observation IS reliable\n"
        assertString += " Prediction percentages [0.97730358 0.00852486 0.01417156]\n"

        self.assertEqual(capturedOutput.getvalue(), assertString)
        
    
    '''
    Function that simulates user input "2" for first input.
    User input "2" in first arguement means that user has not preprocess the data
    This will then prompt user to input excel file path
    The input excel Path for this test should be incorrect
    We will be testing incorrect path for this test case
    After inputting incorrect path, we will input correct path but wrong input file
    Since the input file does not have the neccessary fields, it will exit with code 0
    Expected Output: System exit with code (0).
    '''
    def testing_cli_2_wrong_path_wrong_file(self):
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput
        with unittest.mock.patch('builtins.input', side_effect=['2', './wrongPath', './tests/testing_data_excel/testing_cli_2_wrong.xlsx']):
            with self.assertRaises(SystemExit) as cm:
                menu()
            self.assertEqual(cm.exception.code, 0)

if __name__ == '__main__':
    unittest.main()
    