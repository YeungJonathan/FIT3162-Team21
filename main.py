import pandas as pd
import numpy as np

#read excel file
test = pd.read_excel (r'VBA_data.xls')

#print first 5 rows of excel
print(test.head())