from osgeo import gdal
from pyproj import Proj, transform
import pandas as pd
import xlsxwriter

"""
Processes file to include raster data. For instance, the current file holds observations with locations that do NOT
contain information about the corresponding locations environmental variables. i.e, there is no information about the
associated wetness, dryness, vegetation of a location point. Afterwards, the file will contain such information

@param input_file, file that has the same parameters as the the original dataset file that DELWP provided to us
@param output_file, file that includes 19 environmental variables associated with each row
"""
def writeToFile(input_file, output_file):
    """
    Make a particular point be of the same coordinate system. In this instance we are converting a point using the
    coordinate system epsg:4326 to the coordinate system epsg:3111

    @param point, the point that we would like to convert (to a different coordinate system)
    """
    def changeCoordinateSystem(point):
        inProj = Proj(init='epsg:4326')
        outProj = Proj(init='epsg:3111')
        x2,y2 = transform(inProj,outProj,point[0],point[1])

        return (x2, y2)

    """
    Calculates information about the environmental variable associated at a particular location point.

    @param point, a (long/lat) location point.
    @param yOri, y origins of the raster file
    @param xOri, x origins of the raster file
    @param type, the environmental variable (raster type) being calculated. i.e this may be wetness, vegetation, ect.
    @param pixw, pixel width of the raster file
    @param pixh, pixel height of the raster file
    """
    def calculateRaster(point, yOri, xOri, type, pixw, pixh):
        col = int((point[0] - xOri) / pixw)
        row = int((yOri - point[1]) / pixh)

        return type[row][col]

    # --------------------------------------------------------------------
    #      1. VEG
    # --------------------------------------------------------------------
    dataset = gdal.Open('../raster/vegtype3_4/vegtype3_4')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin = t[0]
    yOrigin = t[3]
    pixelWidth = t[1]
    pixelHeight = -t[5]

    veg = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      2. WETNESS
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/wetness_index_saga_sept2012/wetness_index_saga_sept2012')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_wet = t[0]
    yOrigin_wet = t[3]
    pixelWidth_wet = t[1]
    pixelHeight_wet = -t[5]

    wet = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      3. SUMMER 1
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/SummerPre1750Landsat75_300_900m/SummerPre1750Landsat75_300_900m')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_summer = t[0]
    yOrigin_summer = t[3]
    pixelWidth_summer = t[1]
    pixelHeight_summer = -t[5]

    summer = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      4. SUMMER 2
    # --------------------------------------------------------------------
    dataset = gdal.Open('../raster/SummerLandsat75_300_900m/SummerLandsat75_300_900m')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_summer75 = t[0]
    yOrigin_summer75 = t[3]
    pixelWidth_summer75 = t[1]
    pixelHeight_summer75 = -t[5]

    summer75 = band.ReadAsArray(0, 0, cols, rows)
    # --------------------------------------------------------------------
    #      5. RAINFALL JULY
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/sept2014JulRainfall/sept2014JulRainfall')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_rain7 = t[0]
    yOrigin_rain7 = t[3]
    pixelWidth_rain7 = t[1]
    pixelHeight_rain7 = -t[5]

    rain7 = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      6. RAINFALL JAN
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/sept2014JulRainfall/sept2014JulRainfall')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_rain1 = t[0]
    yOrigin_rain1 = t[3]
    pixelWidth_rain1 = t[1]
    pixelHeight_rain1 = -t[5]

    rain1 = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      7. MINTEMP JUL
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/sept2014JulMinTemp/sept2014JulMinTemp')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_min7 = t[0]
    yOrigin_min7 = t[3]
    pixelWidth_min7 = t[1]
    pixelHeight_min7 = -t[5]

    min7 = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      8. MAXTEMP JAN
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/sept2014JanMaxTemp/sept2014JanMaxTemp')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_max1 = t[0]
    yOrigin_max1 = t[3]
    pixelWidth_max1 = t[1]
    pixelHeight_max1 = -t[5]

    max1 = band.ReadAsArray(0, 0, cols, rows)
    # --------------------------------------------------------------------
    #      9. RADIOMETRICS th
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/Radiometrics_2014_th/Radiometrics_2014_th')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_radioth = t[0]
    yOrigin_radioth = t[3]
    pixelWidth_radioth = t[1]
    pixelHeight_radioth = -t[5]

    radioth = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      10. RADIOMETRICS k
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/Radiometrics_2014_k/Radiometrics_2014_k')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_radiok = t[0]
    yOrigin_radiok = t[3]
    pixelWidth_radiok = t[1]
    pixelHeight_radiok = -t[5]

    radiok = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      11. PROTECTION INDEX
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/ProtectionIndex/ProtectionIndex')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_pi = t[0]
    yOrigin_pi = t[3]
    pixelWidth_pi = t[1]
    pixelHeight_pi = -t[5]

    pi = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      12. VERTICAL DISTANCE
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/log_vertical_distance_saline_wetlands_sept2012/log_vertical_distance_saline_wetlands_sept2012')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_vertical = t[0]
    yOrigin_vertical = t[3]
    pixelWidth_vertical = t[1]
    pixelHeight_vertical = -t[5]

    vertical = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      13. LAND COVER
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/land_cov_use3/land_cov_use3')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_land = t[0]
    yOrigin_land = t[3]
    pixelWidth_land = t[1]
    pixelHeight_land = -t[5]

    land = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      14. IBRA HEX
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/ibra_hex/ibra_hex')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_ibra = t[0]
    yOrigin_ibra = t[3]
    pixelWidth_ibra = t[1]
    pixelHeight_ibra = -t[5]

    ibra = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      15. HYDRA
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/hydro500xwi/hydro500xwi')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_hydra = t[0]
    yOrigin_hydra = t[3]
    pixelWidth_hydra = t[1]
    pixelHeight_hydra = -t[5]

    hydra = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      16. ECO REGION 1
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/ecoregion1750/ecoregion1750')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_eco1 = t[0]
    yOrigin_eco1 = t[3]
    pixelWidth_eco1 = t[1]
    pixelHeight_eco1 = -t[5]

    eco1 = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      17. ECO REGION 2
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/ecoregion2014/ecoregion2014')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_eco2 = t[0]
    yOrigin_eco2 = t[3]
    pixelWidth_eco2 = t[1]
    pixelHeight_eco2 = -t[5]

    eco2 = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #      18. HEATING
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/Anisotrophic_Heating_Ruggedness/Anisotrophic_Heating_Ruggedness')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_heat = t[0]
    yOrigin_heat = t[3]
    pixelWidth_heat = t[1]
    pixelHeight_heat = -t[5]

    heat = band.ReadAsArray(0, 0, cols, rows)


    # --------------------------------------------------------------------
    #      19. STREAMS
    # --------------------------------------------------------------------

    dataset = gdal.Open('../raster/75m_dem_streams_burned_sept2012/75m_dem_streams_burned_sept2012')
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    t = dataset.GetGeoTransform()

    xOrigin_streams = t[0]
    yOrigin_streams = t[3]
    pixelWidth_streams = t[1]
    pixelHeight_streams = -t[5]

    streams = band.ReadAsArray(0, 0, cols, rows)

    # --------------------------------------------------------------------
    #  WRITE INFORMATION TO EXCEL FILE
    # --------------------------------------------------------------------

    # information that we will retain
    input = pd.read_excel(input_file)   # input data (observations)
    df = input[['COMMON_NME','LONGITUDEDD_NUM', 'LATITUDEDD_NUM']]
    taxon_id = input['TAXON_ID']
    species = input['COMMON_NME']
    lat = input['LATITUDEDD_NUM']
    long = input['LONGITUDEDD_NUM']
    reliability = input['RELIABILITY']
    reliability_txt = input['RELIABILITY_TXT']
    record_type = input['RECORD_TYPE']
    sv_record_count = input['SV_RECORD_COUNT']
    cde = input['PRIMARY_CDE']

    # new excel sheet created
    workbook = xlsxwriter.Workbook(output_file, {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet()

    # VBA_data we want
    worksheet.write('A1', 'TAXON_ID')
    worksheet.write('B1', 'COMMON_NME')
    worksheet.write('C1', 'RELIABILITY')
    worksheet.write('D1', 'RELIABILITY_TXT')
    worksheet.write('E1', 'LATITUDEDD_NUM')
    worksheet.write('F1', 'LONGITUDEDD_NUM')
    worksheet.write('G1', 'RECORD_TYPE')
    worksheet.write('H1', 'SV_RECORD_COUNT')

    # raster data (environmental attributes)
    worksheet.write('I1', 'VEG_TYPE')
    worksheet.write('J1', 'WETNESS')
    worksheet.write('K1', 'SUMMER 1')
    worksheet.write('L1', 'SUMMER 2')
    worksheet.write('M1', 'RAINFALL_JULY')
    worksheet.write('N1', 'MIN_TEMP_JULY')
    worksheet.write('O1', 'RAINFALL_JAN')
    worksheet.write('P1', 'MAX_TEMP_JAN')
    worksheet.write('Q1', 'RADIOMETRICS_TH')
    worksheet.write('R1', 'RADIOMETRICS_K')
    worksheet.write('S1', 'PROTECTION_INDEX')
    worksheet.write('T1', 'VERTICAL_DATA')
    worksheet.write('U1', 'LAND_COVER')
    worksheet.write('V1', 'IBRA_HEX')
    worksheet.write('W1', 'HYDRA')
    worksheet.write('X1', 'ECOREGION_1')
    worksheet.write('Y1', 'ECOREGION_2')
    worksheet.write('Z1', 'HEATING')
    worksheet.write('AA1', 'STREAMS')
    worksheet.write('AB1', 'CDE_TYPE')

    row = 1     # starting row
    col = 0     # starting column

    # write information to excel file
    for idx, val in enumerate(species):
        # coordinate point that we want to pass through all the raster files/environmental attributes
        point = changeCoordinateSystem((long[idx], lat[idx]))

        # original data we are retaining (from dataset)
        worksheet.write(row, col, taxon_id[idx])
        worksheet.write(row, col + 1, species[idx])
        worksheet.write(row, col + 2, reliability[idx])
        worksheet.write(row, col + 3, reliability_txt[idx])
        worksheet.write(row, col + 4, lat[idx])
        worksheet.write(row, col + 5, long[idx])
        worksheet.write(row, col + 6, record_type[idx])
        worksheet.write(row, col + 7, sv_record_count[idx])

        # raster data
        worksheet.write(row, col + 8, calculateRaster(point, yOrigin, xOrigin, veg, pixelWidth, pixelHeight))
        worksheet.write(row, col + 9, calculateRaster(point, yOrigin_wet, xOrigin_wet, wet, pixelWidth_wet, pixelHeight_wet))
        worksheet.write(row, col + 10, calculateRaster(point, yOrigin_summer, xOrigin_summer, summer, pixelWidth_summer, pixelHeight_summer))
        worksheet.write(row, col + 11, calculateRaster(point, yOrigin_summer75, xOrigin_summer75, summer75, pixelWidth_summer75, pixelHeight_summer75))
        worksheet.write(row, col + 12, calculateRaster(point, yOrigin_rain7, xOrigin_rain7, rain7, pixelWidth_rain7, pixelHeight_rain7))
        worksheet.write(row, col + 13, calculateRaster(point, yOrigin_min7, xOrigin_min7, min7, pixelWidth_min7, pixelHeight_min7))
        worksheet.write(row, col + 14, calculateRaster(point, yOrigin_rain1, xOrigin_rain1, rain1, pixelWidth_rain1,
                                   pixelHeight_rain1))
        worksheet.write(row, col + 15, calculateRaster(point, yOrigin_max1, xOrigin_max1, max1, pixelWidth_max1,
                                   pixelHeight_max1))
        worksheet.write(row, col + 16, calculateRaster(point, yOrigin_radioth, xOrigin_radioth, radioth, pixelWidth_radioth,
                                   pixelHeight_radioth))
        worksheet.write(row, col + 17, calculateRaster(point, yOrigin_radiok, xOrigin_radiok, radiok, pixelWidth_radiok,
                                   pixelHeight_radiok))
        worksheet.write(row, col + 18, calculateRaster(point, yOrigin_pi, xOrigin_pi, pi, pixelWidth_pi,
                                   pixelHeight_pi))
        worksheet.write(row, col + 19, calculateRaster(point, yOrigin_vertical, xOrigin_vertical, vertical, pixelWidth_vertical,
                                   pixelHeight_vertical))
        worksheet.write(row, col + 20, calculateRaster(point, yOrigin_land, xOrigin_land, land, pixelWidth_land,
                                   pixelHeight_land))
        worksheet.write(row, col + 21, calculateRaster(point, yOrigin_ibra, xOrigin_ibra, ibra, pixelWidth_ibra,
                                   pixelHeight_ibra))
        worksheet.write(row, col + 22, calculateRaster(point, yOrigin_hydra, xOrigin_hydra, hydra, pixelWidth_hydra,
                                   pixelHeight_hydra))
        worksheet.write(row, col + 23, calculateRaster(point, yOrigin_eco1, xOrigin_eco1, eco1, pixelWidth_eco1,
                                   pixelHeight_eco1))
        worksheet.write(row, col + 24, calculateRaster(point, yOrigin_eco2, xOrigin_eco2, eco2, pixelWidth_eco2,
                                   pixelHeight_eco2))
        worksheet.write(row, col + 25, calculateRaster(point, yOrigin_heat, xOrigin_heat, heat, pixelWidth_heat,
                                   pixelHeight_heat))
        worksheet.write(row, col + 26, calculateRaster(point, yOrigin_streams, xOrigin_streams, streams, pixelWidth_streams,
                                   pixelHeight_streams))
        worksheet.write(row, col + 27, cde[idx])

        row += 1

        print("row", idx, "processed")      # let user know that a row has been processed


    workbook.close()    # close the workbook after writing to file

if __name__ == "__main__":
    writeToFile("../VBA_data.xls", '../TEST_RASTER_VBA.xls')