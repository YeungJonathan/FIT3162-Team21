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

    assertReturnString = "\n# --------------------------------------------------------------------\n"
    assertReturnString += ("#                      MAIN MENU                                      \n")
    assertReturnString+= ("# --------------------------------------------------------------------\n")
    assertReturnString+= ("\nPlease select your choice:\n")
    assertReturnString+= ("1. Process observations (data is pre-processed)\n")
    assertReturnString+= ("2. Process observations (data is NOT pre-processed)\n")
    assertReturnString+= ("3. Generate/re-train a species model\n")
    assertReturnString+= ("4. Exit Program\n")


    '''
    Function to test all correct user input (no wrong inputs)
    Input excel file includes a reliable observation taken from the VBA file.
    '''
    def test_CLI_correct_first_print(self):
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput  
        with unittest.mock.patch('builtins.input', side_effect=['1', './tests/testing_data_excel/testing_reliable.xlsx', '4']):
            menu()
        sys.stdout = sys.__stdout__
        assertString = self.assertReturnString
        assertString += "What is the name of your observations file? Note: Accepted formats: xlsx/xls\n\n"
        assertString += " Agile Antechinus was seen at -38.35598 144.96925\n"
        assertString += " The observation IS reliable\n"
        assertString += " Prediction percentages [0.94261246 0.0196184  0.03776914]\n"
        assertString += self.assertReturnString
        self.assertEqual(capturedOutput.getvalue(), assertString)

    '''
    Function to test all correct user input with an excel file consiting of large amount of data
    Mainly testing how this program handles large amount of input data
    Input excel file includes a reliable observation taken from the VBA file.
    '''
    def test_CLI_correct_second_large_data(self):
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput  
        with unittest.mock.patch('builtins.input', side_effect=['2', './tests/testing_data_excel/test_cli_large_data.xlsx', '4']):
            menu()


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
        with unittest.mock.patch('builtins.input', side_effect=['1', '2', './tests/testing_data_excel/testing_reliable.xlsx','4']):
            menu()
        sys.stdout = sys.__stdout__
        assertString = self.assertReturnString
        assertString += "What is the name of your observations file? Note: Accepted formats: xlsx/xls\n"
        assertString += "Wrong input, please input the correct file path\n\n"
        assertString += " Agile Antechinus was seen at -38.35598 144.96925\n"
        assertString += " The observation IS reliable\n"
        assertString += " Prediction percentages [0.94261246 0.0196184  0.03776914]\n"
        assertString += self.assertReturnString

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
        with unittest.mock.patch('builtins.input', side_effect=['1', '2', 'Random Path','./tests/testing_data_excel/testing_reliable_wrong.xlsx', './tests/testing_data_excel/testing_reliable.xlsx', '4']):
            menu()
        sys.stdout = sys.__stdout__
        assertString = self.assertReturnString
        assertString += "What is the name of your observations file? Note: Accepted formats: xlsx/xls\n"
        assertString += "Wrong input, please input the correct file path\n"
        assertString += "Wrong input, please input the correct file path\n"
        assertString += "Wrong input, please input the correct file path\n\n"
        assertString += " Agile Antechinus was seen at -38.35598 144.96925\n"
        assertString += " The observation IS reliable\n"
        assertString += " Prediction percentages [0.94261246 0.0196184  0.03776914]\n"
        assertString += self.assertReturnString
        self.assertEqual(capturedOutput.getvalue(), assertString)


    '''
    Function that simulates model generation
    Generating Southern Brown Tree frog
    Makes sure that generating model works without any erro
    Expected Output: Prints "Sorry. Invalid input. Valid options are: 1, 2".
    '''
    def test_CLI_wrong_first_input(self):
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput  
        with unittest.mock.patch('builtins.input', side_effect=['3', '5','4']):
            menu()


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
        with unittest.mock.patch('builtins.input', side_effect=['2', './tests/testing_data_excel/testing_cli_2_correct.xlsx', '4']):
            menu()
        sys.stdout = sys.__stdout__
        assertString = self.assertReturnString

        assertString += "Alright! Pre-processing the data now. NOTE: this may take a while. Please allow a few minutes.\n"
        assertString += "Output will be stored in preprocess_output.xlsx\n\n"
        assertString += " Agile Antechinus was seen at -38.35692 144.97151\n"
        assertString += " The observation IS reliable\n"
        assertString += " Prediction percentages [0.95406991 0.01917657 0.02675352]\n\n"

        assertString += " Agile Antechinus was seen at -38.35598 144.96925\n"
        assertString += " The observation IS reliable\n"
        assertString += " Prediction percentages [0.94261246 0.0196184  0.03776914]\n"
        assertString += self.assertReturnString

        self.assertEqual(capturedOutput.getvalue(), assertString)
        
    
    '''
    Function that tests if we can quit
    Presses 4 and attempts to quit.
    Expected: Quit successfully.
    '''
    def testing_cli_2_wrong_path_wrong_file(self):
        capturedOutput = io.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput  
        with unittest.mock.patch('builtins.input', side_effect=['4']):
            menu()
        sys.stdout = sys.__stdout__
        assertString = self.assertReturnString

        self.assertEqual(capturedOutput.getvalue(), assertString)

if __name__ == '__main__':
    unittest.main()
    