from osgeo import gdal
import numpy as np
import rasterio
import rasterio.features
import rasterio.warp

'''
This is the file used for first generation raster file filtering
Meaning that this file will no longer be used
Only used for first generation.
Preprocessing should be done with files in the balancing_dataset directory
'''
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


def get_raster_general_information(filePath):
    '''
    Function that gets the general information of the raster file
    :params:
        filePath: the path of the raster file
    '''
    dataset = open_raster_file(filePath)

    # general information of the raster datasets
    print()
    print("Size is {} x {} x {}".format(dataset.RasterXSize,
                                        dataset.RasterYSize,
                                        dataset.RasterCount))
    print("Projection is {}".format(dataset.GetProjection()))
    geotransform = dataset.GetGeoTransform()
    if geotransform:
        print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
        print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
    print()
   
    
def get_raster_data_matrix(filePath):
    '''
    Function that gets the raster file matrix values
    :params:
        filePath: the path of the raster file
    '''
    # get raster data into numpy array
    dataset = open_raster_file(filePath)

    raster_array = np.array(dataset.GetRasterBand(1).ReadAsArray())
    print('raster data matrix: ',raster_array,'\n')
    return raster_array


def get_raster_geolocation(filePath):
    '''
    function that finds the corner gelocations of the raster file
    :params:
        filePath: the path of the raster file
    '''
    # print geolocation of datas
    with rasterio.open(filePath) as dataset:
        # Read the dataset's valid data mask as a ndarray.
        mask = dataset.dataset_mask()

        # Extract feature shapes and values from the array.
        for geom, val in rasterio.features.shapes(
                mask, transform=dataset.transform):

            # Transform shapes from the dataset's own coordinate
            # reference system to CRS84 (EPSG:4326).
            geom = rasterio.warp.transform_geom(
                dataset.crs, 'EPSG:4326', geom, precision=6)

            # Print GeoJSON shapes to stdout.
            print('geometric locations when raster data of type: ',geom , '\n')

        band = dataset.read(1)
        print('raster data four corner boundary: ',dataset.bounds, '\n')
        print('location top left: ', dataset.transform * (0,0), '\n')
        print('location bottom left: ', dataset.transform * (0,dataset.width), '\n')
        print('location top right: ', dataset.transform * (dataset.height,0), '\n')
        print('location bottom right: ',dataset.transform * (dataset.height, dataset.width), '\n')
        returnMap = {}
        returnMap['top_left'] = dataset.transform * (0,0)
        returnMap['bottom_left'] = dataset.transform * (0,dataset.width)
        returnMap['top_right'] = dataset.transform * (dataset.height,0)
        returnMap['bottom_right'] = dataset.transform * (dataset.height, dataset.width)
        return returnMap, dataset.height, dataset.width


def get_location_information(data_height, data_width, four_corners, raster_array, latitude, longitude):
    '''
    Function that gets the value from the matrix for a particular lat and long
    :params:
        data_height: height of the matrix
        data_width: width of the matrix
        four_corners: map of the values for the four corners
        raster_array: the matrix of raster data
        latitude: the latitude that we are finding
        longitude: the longitude that we are finding 
    :return:
        (err, Value)
        err: whether an error occured based on the range of the lat and long
        value: 
            1. err is True, value is the err message
            2. err is False, value is the corresponding value in the matrix
    '''
    if latitude < four_corners['top_left'][0] or latitude > four_corners['top_right'][0]:
        return True, "Latitude out of range"
    elif longitude > four_corners['top_left'][1] or longitude < four_corners['bottom_left'][1]:
        return True, "Longitude out of range"
    else:
        lat_increment_value = (four_corners['top_right'][0] - four_corners['top_left'][0]) / data_width
        long_decrease_value = (four_corners['top_left'][1] - four_corners['bottom_left'][1]) / data_height
        
        lat_increment_count = round((latitude - four_corners['top_left'][0]) / lat_increment_value)
        long_increment_count = round((four_corners['top_left'][1] - longitude) / long_decrease_value)
        value = raster_array[long_increment_count, lat_increment_count]

        return False, value
        

if __name__ == "__main__":
    filePath = './vegtype3_4/vegtype3_4'
    latitude = 2400000
    longitude = 2400000

    get_raster_general_information(filePath)
    raster_array = get_raster_data_matrix(filePath)
    four_corners, data_height, data_width = get_raster_geolocation(filePath)
   
    err, value = get_location_information(data_height, data_width, four_corners, raster_array,latitude, longitude)
    if err:
        raise Exception(value)
    else:
        print('Values at Lat -> {0}, Long -> {1} is {2}'.format(latitude, longitude, value)) 
