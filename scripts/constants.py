# Path
INPUT_DIR_PATH = '../datasets/landsat8'
OUTPUT_RASTER_DIR_PATH = '../results/raster'
OUTPUT_CSV_DIR_PATH = '../results/csv'
MODEL_PATH = '../models/best-model-5.joblib'

# List Data
PROCESSING_DATA = ['Raster_LC08_20131101.tif', 'Raster_LC08_20140901.tif', 'Raster_LC08_20150616.tif', 
                   'Raster_LC08_20160501.tif', 'Raster_LC08_20170605.tif', 'Raster_LC08_20180928.tif', 
                   'Raster_LC08_20191001.tif', 'Raster_LC08_20200613.tif', 'Raster_LC08_20210819.tif', 
                   'Raster_LC08_20220822.tif']

# Class mapping
CLASS_MAPPING = {
    'no_data': 0,
    'perkebunan': 1,
    'pertanian': 2,
    'pemukiman': 3,
    'rerumputan': 4,
    'awan': 5,
    'badan air': 6
}