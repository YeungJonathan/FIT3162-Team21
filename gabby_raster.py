from osgeo import gdal
from osgeo import osr
from osgeo import ogr
from pyproj import Proj, transform
import pandas as pd
import numpy as np
import rasterio
import rasterio.features
import rasterio.warp

def changeCoordinateSystem(point):
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init='epsg:3111')
    x2,y2 = transform(inProj,outProj,point[0],point[1])

    return (x2, y2)

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

# dataset = gdal.Open('../raster/SummerPre1750Landsat75_300_900m/SummerPre1750Landsat75_300_900m')
# band = dataset.GetRasterBand(1)
#
# cols = dataset.RasterXSize
# rows = dataset.RasterYSize
#
# t = dataset.GetGeoTransform()
#
# xOrigin_summer = t[0]
# yOrigin_summer = t[3]
# pixelWidth_summer = t[1]
# pixelHeight_summer = -t[5]
#
# summer = band.ReadAsArray(0, 0, cols, rows)

# --------------------------------------------------------------------
#      4. SUMMER 2
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      5. RAINFALL JULY
# --------------------------------------------------------------------

# dataset = gdal.Open('../raster/sept2014JulRainfall/sept2014JulRainfall')
# band = dataset.GetRasterBand(1)
#
# cols = dataset.RasterXSize
# rows = dataset.RasterYSize
#
# t = dataset.GetGeoTransform()
#
# xOrigin_rain7 = t[0]
# yOrigin_rain7 = t[3]
# pixelWidth_rain7 = t[1]
# pixelHeight_rain7 = -t[5]
#
# rain7 = band.ReadAsArray(0, 0, cols, rows)

# --------------------------------------------------------------------
#      6. RAINFALL JAN
# --------------------------------------------------------------------

# dataset = gdal.Open('../raster/sept2014JulRainfall/sept2014JulRainfall')
# band = dataset.GetRasterBand(1)
#
# cols = dataset.RasterXSize
# rows = dataset.RasterYSize
#
# t = dataset.GetGeoTransform()
#
# xOrigin_rain1 = t[0]
# yOrigin_rain1 = t[3]
# pixelWidth_rain1 = t[1]
# pixelHeight_rain1 = -t[5]
#
# rain1 = band.ReadAsArray(0, 0, cols, rows)

# --------------------------------------------------------------------
#      7. MINTEMP JUL
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      8. MAXTEMP JAN
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      9. RADIOMETRICS 1
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      10. RADIOMETRICS 2
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      11. PROTECTION INDEX
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      12. VERTICAL DISTANCE
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      13. LAND COVER
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      14. IBRA HEX
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      15. HYDRA
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      16. ECO REGION 1
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      17. ECO REGION 2
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      18. HEATING
# --------------------------------------------------------------------

# --------------------------------------------------------------------
#      19. STREAMS
# --------------------------------------------------------------------

input = pd.read_excel('input_observations.xlsx') # input data (observations)
df = input[['COMMON_NME','LONGITUDEDD_NUM', 'LATITUDEDD_NUM']]
species = input['COMMON_NME']
lat = input['LATITUDEDD_NUM']
long = input['LONGITUDEDD_NUM']


#processRaster('./raster/wetness_index_saga_sept2012/wetness_index_saga_sept2012', point)

print("SPECIES".ljust(25), " LAT".ljust(15), " LONG".ljust(10), " VEG".ljust(5),
      " WETNESS".ljust(5), " SUMMER".ljust(10), " RAINFALL".ljust(6))
for idx, val in enumerate(species):
    #print(species[idx], lat[idx], long[idx])
    point = changeCoordinateSystem((long[idx], lat[idx]))

    print(species[idx].ljust(25), ' ', str(lat[idx]).ljust(10),' ', str(long[idx]).ljust(10), ' ' ,
          str(calculateRaster(point, yOrigin, xOrigin, veg, pixelWidth, pixelHeight)).ljust(3), ' ',
          str(calculateRaster(point, yOrigin_wet, xOrigin_wet, wet, pixelWidth_wet, pixelHeight_wet)).ljust(3), ' ',
          # str(calculateRaster(point, yOrigin_summer, xOrigin_summer, summer, pixelWidth_summer, pixelHeight_summer)).ljust(10), ' ',
          # str(calculateRaster(point, yOrigin_rain7, xOrigin_rain7, rain7, pixelWidth_rain7,
          #                     pixelHeight_rain7)).ljust(6), ' ',
          # str(calculateRaster(point, yOrigin_rain1, xOrigin_rain1, rain1, pixelWidth_rain1,
          #                     pixelHeight_rain1)).ljust(6), ' '
          )