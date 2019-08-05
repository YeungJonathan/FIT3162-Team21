import pandas as pd
import numpy as np
import graphviz 
from sklearn import datasets, tree

# read excel files
vba = pd.read_excel('VBA_data.xls') # VBA (training data)
input = pd.read_excel('input_observations.xlsx') # input data (observations)

# predictors to build our tree model
scientific_display = input['SCIENTIFIC_DISPLAY_NME']
reliability = input['RELIABILITY']
latitude = input["LATITUDEDD_NUM"]
longitude = input["LONGITUDEDD_NUM"]

columns = ['SCIENTIFIC_DISPLAY_NME', 'RELIABILITY']
# reliability - 3 2 1
# scientific display name - 1 2 3 4 5 6
rows = [scientific_display, reliability]

print(columns)
print(input.head())

def missing_values_table(df):
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: 'Missing Values', 1: '% of Total Values'})
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
    print("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
                                                              "There are " + str(mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")
    return mis_val_table_ren_columns

print(missing_values_table(vba))