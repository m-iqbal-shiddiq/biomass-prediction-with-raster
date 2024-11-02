import joblib
import numpy as np

from helpers import load_model
from helpers import read_raster, write_raster, predict_raster

def predict(input_path:str, output_path: str, model_path: str, class_mapping: dict):
    
    model = load_model(model_path)
    
    raster_data, profile, nodata_value = read_raster(input_path)
    predicted_raster = predict_raster(model, raster_data, nodata_value, class_mapping)
  
    combined_raster = np.vstack([raster_data, predicted_raster[np.newaxis, :, :]])
    profile.update(count=combined_raster.shape[0])
    write_raster(output_path, combined_raster, profile, nodata_value)