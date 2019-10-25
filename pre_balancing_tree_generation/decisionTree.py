import pandas as pd
import numpy as np
from sklearn.datasets.species_distributions import construct_grids
import graphviz
from sklearn import datasets, tree
import matplotlib.pyplot as plt
import geopy.distance


'''
This is the file used for pre-balanced tree generation
Meaning that this file will no longer be used
Only used for first generation.
'''

def generateTree(species):
    # read excel files
    vba = pd.read_excel('VBA_Raster.xlsx') # VBA (training data)

    ufi = vba.loc[vba['COMMON_NME'] == species]


    # data_list should be all infos
    # target_list should be reliability
    data_list = []
    target_list = [] 

    for index, row in ufi.iterrows():
        TAXON_ID = row['TAXON_ID']
        COMMON_NME = row['COMMON_NME']
        RELIABILITY = row['RELIABILITY']
        RELIABILITY_TXT = row['RELIABILITY_TXT']
        LONGITUDEDD_NUM = row['LONGITUDEDD_NUM']
        LATITUDEDD_NUM = row['LATITUDEDD_NUM']
        # RECORD_TYPE = row['RECORD_TYPE']
        SV_RECORD_COUNT = row['SV_RECORD_COUNT']
        VEG_TYPE = row['VEG_TYPE']
        WETNESS = row['WETNESS']
        SUMMER_1 = row['SUMMER 1']
        SUMMER_2 = row['SUMMER 2']
        RAINFALL_JULY= row['RAINFALL_JULY']
        MIN_TEMP_JULY = row['MIN_TEMP_JULY']
        RAINFALL_JAN = row['RAINFALL_JAN']
        MAX_TEMP_JAN = row['MAX_TEMP_JAN']
        RADIOMETRICS_TH = row['RADIOMETRICS_TH']
        RADIOMETRICS_K = row['RADIOMETRICS_K']
        PROTECTION_INDEX = row['PROTECTION_INDEX']
        VERTICAL_DATA = row['VERTICAL_DATA']
        LAND_COVER = row['LAND_COVER']
        IBRA_HEX = row['IBRA_HEX']
        HYDRA = row['HYDRA']
        ECOREGION_1 = row['ECOREGION_1']
        ECOREGION_2 = row['ECOREGION_2']
        HEATING = row['HEATING']
        STREAMS = row['STREAMS']


        data_list.append([LATITUDEDD_NUM, LONGITUDEDD_NUM, SV_RECORD_COUNT, VEG_TYPE,WETNESS, SUMMER_1, SUMMER_2, RAINFALL_JULY, MIN_TEMP_JULY, RAINFALL_JAN, MAX_TEMP_JAN, RADIOMETRICS_TH, RADIOMETRICS_K, PROTECTION_INDEX, VERTICAL_DATA, LAND_COVER, IBRA_HEX, HYDRA, ECOREGION_1, ECOREGION_2, HEATING, STREAMS])
        # data_list.append([LATITUDEDD_NUM, LONGITUDEDD_NUM, RECORD_TYPE, SV_RECORD_COUNT, VEG_TYPE,WETNESS, SUMMER_1, SUMMER_2, RAINFALL_JULY, MIN_TEMP_JULY, RAINFALL_JAN, MAX_TEMP_JAN, RADIOMETRICS_TH, RADIOMETRICS_K, PROTECTION_INDEX, VERTICAL_DATA, LAND_COVER, IBRA_HEX, HYDRA, ECOREGION_1, ECOREGION_2, HEATING, STREAMS])


        if RELIABILITY == "Acceptable":
            current_reliability = 3
        elif RELIABILITY == "Confirmed":
            current_reliability = 2
        elif RELIABILITY == "Unconfirmed":
            current_reliability = 1
        else:
            current_reliability = 0

        target_list.append(current_reliability);

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(data_list, target_list)
    tree.plot_tree(clf.fit(data_list, target_list)) 
    dot_data = tree.export_graphviz(clf, out_file=None, filled=True, rounded=True, special_characters=True)  
    graph = graphviz.Source(dot_data)
    renderPath = "./decision_tree_visualisation/" + species
    graph.render(renderPath)
