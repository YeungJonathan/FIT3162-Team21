import numpy as np
import pandas as pd
import xlsxwriter
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from pseudo_absence_raster import findRaster

def generateAbsenceData(speciesName, outputFilePath):
    vba = pd.read_excel('VBA_Raster.xlsx') # VBA (training data)
    allLat = vba["LATITUDEDD_NUM"]
    allLong = vba["LONGITUDEDD_NUM"]

    maxLat = allLat.max()
    minLat = allLat.min()

    maxLong = allLong.max()
    minLong = allLong.min()

    ufi = vba.loc[vba['COMMON_NME'] == speciesName]
    numOfItem = len(ufi)
    dataList = []
    longList = []
    latList = []
    taxonID = 0;

    for index, row in ufi.iterrows():
        if taxonID == 0:
            taxonID = row['TAXON_ID']
        LONGITUDEDD_NUM = row['LONGITUDEDD_NUM']
        LATITUDEDD_NUM = row['LATITUDEDD_NUM']
        VEG_TYPE = row['VEG_TYPE']
        WETNESS = row['WETNESS']
        SUMMER_1 = row['SUMMER 1']
        SUMMER_2 = row['SUMMER 2']
        RAINFALL_JULY = row['RAINFALL_JULY']
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

        longList.append(LONGITUDEDD_NUM)
        latList.append(LATITUDEDD_NUM)
        dataList.append([LATITUDEDD_NUM, LONGITUDEDD_NUM, VEG_TYPE, WETNESS, SUMMER_1, SUMMER_2, RAINFALL_JULY, MIN_TEMP_JULY, RAINFALL_JAN, MAX_TEMP_JAN, RADIOMETRICS_TH
            , RADIOMETRICS_K, PROTECTION_INDEX, VERTICAL_DATA, LAND_COVER, IBRA_HEX, HYDRA, ECOREGION_1, ECOREGION_2, HEATING, STREAMS])

    rng = np.random.RandomState(42)

    # # Generate some abnormal novel observations
    lat_outliers = rng.uniform(low=minLat, high=maxLat, size=(10000 , 1))
    long_outliers = rng.uniform(low=minLong, high=maxLong, size=(10000, 1))

    outliers = []
    for i in range(len(lat_outliers)):
        currentPoint = findRaster(lat_outliers[i][0], long_outliers[i][0])
        outliers.append(currentPoint)

    # fit the model
    clf = IsolationForest(behaviour='new', max_samples=numOfItem,
                        n_estimators = 300,
                        random_state=rng, contamination='auto')

    clf.fit(dataList)
    y_pred_outliers = clf.predict(outliers)
    y_predict_long = []
    y_predict_lat = []
    for index in range(len(y_pred_outliers)):
        if y_pred_outliers[index] == -1:
            y_predict_lat.append(outliers[index][0])
            y_predict_long.append(outliers[index][1])

    # # plot the line, the samples, and the nearest vectors to the plane
    ## uncomment below for the graph
    #########################################################################################
    #########################################################################################
    # xx, yy = np.meshgrid(np.linspace(minLat, maxLat, 50), np.linspace(minLong, maxLong, 50))

    # plt.title("IsolationForest")


    # b1 = plt.scatter(latList, longList, c='white',
    #                  s=20, edgecolor='k')
    # c = plt.scatter(y_predict_lat, y_predict_long, c='red',
    #                 s=20, edgecolor='k')
    # plt.axis('tight')
    # plt.xlim((minLat, maxLat))
    # plt.ylim((minLong, maxLong))
    # plt.legend([b1, c],
    #            ["training observations",
    #             "new regular observations", "new abnormal observations"],
    #            loc="upper left")
    # plt.show()
    #########################################################################################
    #########################################################################################

    workbook = xlsxwriter.Workbook(outputFilePath, {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet()

    # VBA_data we want
    worksheet.write('A1', 'TAXON_ID')
    worksheet.write('B1', 'COMMON_NME')
    worksheet.write('C1', 'RELIABILITY')
    worksheet.write('D1', 'RELIABILITY_TXT')
    worksheet.write('E1', 'LATITUDEDD_NUM')
    worksheet.write('F1', 'LONGITUDEDD_NUM')

    worksheet.write('G1', 'VEG_TYPE')
    worksheet.write('H1', 'WETNESS')
    worksheet.write('I1', 'SUMMER 1')
    worksheet.write('J1', 'SUMMER 2')
    worksheet.write('K1', 'RAINFALL_JULY')
    worksheet.write('L1', 'MIN_TEMP_JULY')
    worksheet.write('M1', 'RAINFALL_JAN')
    worksheet.write('N1', 'MAX_TEMP_JAN')
    worksheet.write('O1', 'RADIOMETRICS_TH')
    worksheet.write('P1', 'RADIOMETRICS_K')
    worksheet.write('Q1', 'PROTECTION_INDEX')
    worksheet.write('R1', 'VERTICAL_DATA')
    worksheet.write('S1', 'LAND_COVER')
    worksheet.write('T1', 'IBRA_HEX')
    worksheet.write('U1', 'HYDRA')
    worksheet.write('V1', 'ECOREGION_1')
    worksheet.write('W1', 'ECOREGION_2')
    worksheet.write('X1', 'HEATING')
    worksheet.write('Y1', 'STREAMS')

    row = 1
    col = 0

    for index in range(len(y_pred_outliers)):
        if y_pred_outliers[index] == -1 and row < 6530:
            worksheet.write(row, col, taxonID)
            worksheet.write(row, col + 1, speciesName)
            worksheet.write(row, col + 2, 'Unreliable')
            worksheet.write(row, col + 3, 'Pseudo Absence')
            worksheet.write(row, col + 4, outliers[index][0])
            worksheet.write(row, col + 5, outliers[index][1])

            worksheet.write(row, col + 6, outliers[index][2])
            worksheet.write(row, col + 7, outliers[index][3])
            worksheet.write(row, col + 8, outliers[index][4])
            worksheet.write(row, col + 9, outliers[index][5])
            worksheet.write(row, col + 10, outliers[index][6])
            worksheet.write(row, col + 11, outliers[index][7])
            worksheet.write(row, col + 12, outliers[index][8])
            worksheet.write(row, col + 13, outliers[index][9])
            worksheet.write(row, col + 14, outliers[index][10])
            worksheet.write(row, col + 15, outliers[index][11])
            worksheet.write(row, col + 16, outliers[index][12])
            worksheet.write(row, col + 17, outliers[index][13])
            worksheet.write(row, col + 18, outliers[index][14])
            worksheet.write(row, col + 19, outliers[index][15])
            worksheet.write(row, col + 20, outliers[index][16])
            worksheet.write(row, col + 21, outliers[index][17])
            worksheet.write(row, col + 22, outliers[index][18])
            worksheet.write(row, col + 23, outliers[index][19])
            worksheet.write(row, col + 24, outliers[index][20])
            row += 1

    workbook.close()