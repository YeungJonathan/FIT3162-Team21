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
    x1,y1 = point[0],point[1]
    x2,y2 = transform(inProj,outProj,x1,y1)

    return (x2, y2)

def calculateRaster(point, yOri, xOri, type, pixw, pixh):
    col = int((point[0] - xOri) / pixw)
    row = int((yOri - point[1]) / pixh)

    return type[row][col]

# --------------------------------------------------------------------
#      VEG
# --------------------------------------------------------------------
dataset = gdal.Open('./raster/vegtype3_4/vegtype3_4')
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
#      WETNESS
# --------------------------------------------------------------------

dataset = gdal.Open('./raster/wetness_index_saga_sept2012/wetness_index_saga_sept2012')
band = dataset.GetRasterBand(1)

cols = dataset.RasterXSize
rows = dataset.RasterYSize

t = dataset.GetGeoTransform()

xOrigin_wet = t[0]
yOrigin_wet = t[3]
pixelWidth_wet = t[1]
pixelHeight_wet = -t[5]

wet = band.ReadAsArray(0, 0, cols, rows)

input = pd.read_excel('input_observations.xlsx') # input data (observations)
df = input[['COMMON_NME','LONGITUDEDD_NUM', 'LATITUDEDD_NUM']]
species = input['COMMON_NME']
lat = input['LATITUDEDD_NUM']
long = input['LONGITUDEDD_NUM']

#processRaster('./raster/wetness_index_saga_sept2012/wetness_index_saga_sept2012', point)

print("SPECIES".ljust(25), " LAT".ljust(15), " LONG".ljust(10), " VEG".ljust(5), " WETNESS".ljust(5))
for idx, val in enumerate(species):
    #print(species[idx], lat[idx], long[idx])
    point = changeCoordinateSystem((long[idx], lat[idx]))

    print(species[idx].ljust(25), ' ', str(lat[idx]).ljust(10),' ', str(long[idx]).ljust(10), ' ' ,
          str(calculateRaster(point, yOrigin, xOrigin, veg, pixelWidth, pixelHeight)).ljust(3), ' ',
          str(calculateRaster(point, yOrigin_wet, xOrigin_wet, wet, pixelWidth_wet, pixelHeight_wet)).ljust(3), ' ')