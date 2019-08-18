from osgeo import gdal
import numpy as np
import rasterio
import rasterio.features
import rasterio.warp

def open_raster_file(filePath):
    '''
    Function used to open the raster_file
    :params:
        filePath: the path of the raster file
    '''
    dataset = gdal.Open(filePath, gdal.GA_ReadOnly)
    if not dataset:
        raise Exception("Error opening dataset")
    return dataset
   
    
def get_raster_data_matrix(filePath):
    '''
    Function that gets the raster file matrix values
    :params:
        filePath: the path of the raster file
    '''
    # get raster data into numpy array
    dataset = open_raster_file(filePath)

    raster_array = np.array(dataset.GetRasterBand(1).ReadAsArray())
    return raster_array


def getDetails(raster_array):
    minNum, maxNum = None, None
    allSum = 0
    count = 0
    for i in raster_array:
        for j in i:
            if j != -99:
                if minNum == None or maxNum == None:
                    minNum = j
                    maxNum = j
                else:
                    if j < minNum:
                        minNum = j
                    if j > maxNum:
                        maxNum = j
                allSum += j
                count += 1
    return minNum, maxNum, allSum / count
            

def getMinMaxAverage(filePath):
    raster_array = get_raster_data_matrix(filePath)
    minNum, maxNum, average = getDetails(raster_array)
    print(minNum, maxNum, average)
    return minNum, maxNum, average


# if __name__ == "__main__":
#     filePath = './vegtype3_4/vegtype3_4'
#     minNum, maxNum, average = getMinMaxAverage(filePath)
#     print(minNum, maxNum, average)
