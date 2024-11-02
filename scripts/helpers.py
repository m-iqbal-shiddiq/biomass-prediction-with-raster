import joblib
import numpy as np
import pandas as pd
import rasterio

from sklearn.preprocessing import StandardScaler

def load_model(input_path: str):
    return joblib.load(input_path)

def read_raster(file_path):
    with rasterio.open(file_path) as src:
        raster_data = src.read()
        profile = src.profile
        nodata = src.nodata
    return raster_data, profile, nodata

def write_raster(file_path, raster_data, profile, nodata_value):
    profile.update(dtype=rasterio.uint16 if nodata_value > 255 else rasterio.uint8, count=raster_data.shape[0], nodata=nodata_value)
    with rasterio.open(file_path, 'w', **profile) as dst:
        dst.write(raster_data)
        
def min_max_scale(data):
    data_min = np.min(data)
    data_max = np.max(data)
    
    if data_max - data_min == 0:
        return np.zeros(data.shape)
    
    scaled_data = (data - data_min) / (data_max - data_min)
    return scaled_data
        
def predict_raster(model, raster_data, nodata_value, class_mapping):
    
    raster_data = raster_data[:7, :, :]
    
    n_bands, height, width = raster_data.shape
    reshaped_data = raster_data.reshape(n_bands, height * width).T

    valid_mask = np.all(reshaped_data != nodata_value, axis=1)
    valid_data = reshaped_data[valid_mask]
    
    scaled_data = min_max_scale(valid_data)

    feature_names = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
    df_valid = pd.DataFrame(scaled_data, columns=feature_names)

    predicted_classes = model.predict(df_valid)
    
    # unique, counts = np.unique(predicted_classes, return_counts=True)
    # label_counts = dict(zip(unique, counts))
    # print(label_counts)
    
    predicted_labels = np.array([class_mapping[pred] for pred in predicted_classes])

    predicted_raster = np.full((height, width), nodata_value, dtype=np.uint16)
    predicted_raster.flat[valid_mask] = predicted_labels
    
    return predicted_raster