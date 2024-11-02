import rasterio
import numpy as np
import pandas as pd

def extract(input_path: str, output_path: str):
    
    with rasterio.open(input_path) as src:
        bands = []
        for i in range(1, 9):
            band = src.read(i)
            bands.append(band)

        bands_array = np.stack(bands, axis=0)
        bands_array = np.transpose(bands_array, (1, 2, 0)) 

        height, width, _ = bands_array.shape
        lats = np.zeros((height, width))
        lons = np.zeros((height, width))

        for row in range(height):
            for col in range(width):
                lon, lat = src.xy(row, col)
                lats[row, col] = lat
                lons[row, col] = lon
    
    flat_lats = lats.flatten()
    flat_lons = lons.flatten()
    flat_bands = bands_array.reshape(-1, 8)
    
    data = {
        'latitude': flat_lats,
        'longitude': flat_lons,
        'band1': flat_bands[:, 0],
        'band2': flat_bands[:, 1],
        'band3': flat_bands[:, 2],
        'band4': flat_bands[:, 3],
        'band5': flat_bands[:, 4],
        'band6': flat_bands[:, 5],
        'band7': flat_bands[:, 6],
        'class': flat_bands[:, 7]
    }
    
    df = pd.DataFrame(data)
    df = df.loc[df['class'] != 65535].reset_index(drop=True)
    df.to_csv(output_path, index=False)