from osgeo import gdal
import numpy as np
import rasterio
import rasterio.features
import rasterio.warp

def open_raster_file(filePath):
    dataset = gdal.Open(filePath, gdal.GA_ReadOnly)
    if not dataset:
        raise Exception("Error opening dataset")
    return dataset

def get_raster_general_information(filePath):
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
    # get raster data into numpy array
    dataset = open_raster_file(filePath)

    myarray = np.array(dataset.GetRasterBand(1).ReadAsArray())
    print('raster data matrix: ',myarray,'\n')




def get_raster_geolocation(filePath):
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
        print('location bottom right: ',dataset.transform * (dataset.height, dataset.width), '\n')


if __name__ == "__main__":
    filePath = './vegtype3_4/vegtype3_4'
    get_raster_general_information(filePath)
    get_raster_data_matrix(filePath)
    get_raster_geolocation(filePath)