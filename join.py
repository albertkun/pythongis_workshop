import pandas as pd
import geopandas as gp
import math
from shapely.geometry import Point

# INPUT_DATA_FILE = "/Users/nikhilbhatia/Desktop/MDH/Long-Beach/20180909_Long Beach Arrests 2010-2017_streamlined_sample.csv"
# SHAPE_FILE = "/Users/nikhilbhatia/Desktop/MDH/Long-Beach/download/CouncilDistricts.shp"
# LATITUDE = "LAT_HOME"
# LONGITUDE = "LONG_HOME"

# FILL OUT THIS DATA FOR EACH DATA FILE
INPUT_DATA_FILE = "/Users/nikhilbhatia/Desktop/MDH/Orange-County/OC_2018_Clean_Geocoded.csv"
SHAPE_FILE = "/Users/nikhilbhatia/Desktop/MDH/Orange-County/Supervisorial_Districts_–_SCAG_Region/Supervisorial_Districts_–_SCAG_Region.shp"
LATITUDE = "Latitude"
LONGITUDE = "Longitude"
NEW_COLUMNS = [
    "DISTRICT",
]

OUTPUT_FILE = INPUT_DATA_FILE[:-4] + "_JOIN" + INPUT_DATA_FILE[-4:]

# Read data file into Geopandas
data = pd.read_csv(INPUT_DATA_FILE)
original_cols = list(data.columns)
data['geometry'] = data.apply(
    lambda z: Point(z[LONGITUDE], z[LATITUDE]) if not math.isnan(
        z[LATITUDE]) else Point(0.0, 0.0), axis=1)
data = gp.GeoDataFrame(data)

# Read shape file into Geopandas
polys = gp.GeoDataFrame.from_file(SHAPE_FILE)  # or geojson etc

# Ensure data formats the same
data.crs = polys.crs

# Run spatial join
result = gp.sjoin(data, polys, how="left")

# Write original columns plus new column to output file
final_cols = original_cols + NEW_COLUMNS
result = result[final_cols]
result = result.fillna("NA")
result.to_csv(OUTPUT_FILE)
