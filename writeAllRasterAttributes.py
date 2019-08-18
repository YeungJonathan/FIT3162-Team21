import xlsxwriter
from raster_attribute import getMinMaxAverage


workbook = xlsxwriter.Workbook('./VBA_Raster_Info.xlsx', {'nan_inf_to_errors': True})
worksheet = workbook.add_worksheet()

# add header
worksheet.write('A1', "FILE")
worksheet.write('B1', "MIN")
worksheet.write('C1', "MAX")
worksheet.write('D1', "Average")

dataArray = []
dataArray.append('./raster/vegtype3_4/vegtype3_4')
dataArray.append('./raster/wetness_index_saga_sept2012/wetness_index_saga_sept2012')
dataArray.append('./raster/SummerPre1750Landsat75_300_900m/SummerPre1750Landsat75_300_900m')
dataArray.append('./raster/SummerLandsat75_300_900m/SummerLandsat75_300_900m')
dataArray.append('./raster/sept2014JulRainfall/sept2014JulRainfall')
dataArray.append('./raster/sept2014JulMinTemp/sept2014JulMinTemp')
dataArray.append('./raster/sept2014JanMaxTemp/sept2014JanMaxTemp')
dataArray.append('./raster/Radiometrics_2014_th/Radiometrics_2014_th')
dataArray.append('./raster/Radiometrics_2014_k/Radiometrics_2014_k')
dataArray.append('./raster/ProtectionIndex/ProtectionIndex')
dataArray.append('./raster/log_vertical_distance_saline_wetlands_sept2012/log_vertical_distance_saline_wetlands_sept2012')
dataArray.append('./raster/land_cov_use3/land_cov_use3')
dataArray.append('./raster/ProtectionIndex/ProtectionIndex')
dataArray.append('./raster/ibra_hex/ibra_hex')
dataArray.append('./raster/ProtectionIndex/ProtectionIndex')
dataArray.append('./raster/hydro500xwi/hydro500xwi')
dataArray.append('./raster/ProtectionIndex/ProtectionIndex')
dataArray.append('./raster/ecoregion1750/ecoregion1750')
dataArray.append('./raster/ecoregion2014/ecoregion2014')
dataArray.append('./raster/Anisotrophic_Heating_Ruggedness/Anisotrophic_Heating_Ruggedness')
dataArray.append('./raster/75m_dem_streams_burned_sept2012/75m_dem_streams_burned_sept2012')

# # get all data info and write into file
row = 1
for filePath in dataArray:
    minNum, maxNum, average = getMinMaxAverage(filePath);
    fileName = filePath.split('/')[3]
    worksheet.write(row, 0, fileName)
    worksheet.write(row, 1, minNum)
    worksheet.write(row, 2, maxNum)
    worksheet.write(row, 3, average)
    row += 1


workbook.close()


