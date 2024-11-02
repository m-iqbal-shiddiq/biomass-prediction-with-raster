import os
from constants import CLASS_MAPPING, INPUT_DIR_PATH, MODEL_PATH, OUTPUT_RASTER_DIR_PATH, OUTPUT_CSV_DIR_PATH, PROCESSING_DATA
from extract_data_raster import extract
from predict_raster import predict

for year in os.listdir(INPUT_DIR_PATH):
    if year.startswith('.'):
        continue
    
    print(f'---------- {year} ----------')
    
    if not os.path.exists(os.path.join(OUTPUT_RASTER_DIR_PATH, year)):
        os.makedirs(os.path.join(OUTPUT_RASTER_DIR_PATH, year))
        
    if not os.path.exists(os.path.join(OUTPUT_CSV_DIR_PATH, year)):
        os.makedirs(os.path.join(OUTPUT_CSV_DIR_PATH, year))
        
    
    for raster in os.listdir(os.path.join(INPUT_DIR_PATH, year)):
        if not raster.endswith('.tif'):
            continue
        
        if raster not in PROCESSING_DATA:
            continue
        
        print(f'Predicting raster {raster}...')
        
        try:
            predict(
                input_path=os.path.join(INPUT_DIR_PATH, year, raster),
                output_path=os.path.join(OUTPUT_RASTER_DIR_PATH, year, raster),
                model_path=MODEL_PATH,
                class_mapping=CLASS_MAPPING,
            )

            extract(
                input_path=os.path.join(OUTPUT_RASTER_DIR_PATH, year, raster),
                output_path=os.path.join(OUTPUT_CSV_DIR_PATH, year, raster.replace('.tif', '.csv')),
            )
        except Exception as e:
            print(f'{year}/{raster} failed')
            print(f'Error: {e}')
            continue
        