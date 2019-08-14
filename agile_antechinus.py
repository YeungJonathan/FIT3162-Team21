import pandas as pd
import numpy as np
from sklearn.datasets.species_distributions import construct_grids
import graphviz
from sklearn import datasets, tree
import matplotlib.pyplot as plt
import geopy.distance

# read excel files
vba = pd.read_excel('VBA_Raster.xlsx') # VBA (training data)

ufi = vba.loc[vba['COMMON_NME'] == "Agile Antechinus"]
print(ufi)