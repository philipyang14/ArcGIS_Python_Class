# Step 0 - Warm up task

# Develop a small script that uses two datasets from RIGIS.org and undertake a geoprocessing routine on the
# data.

# This could be a spatial join, a buffer, an intersect, an extract by mask for example.
# there are no restrictions on the tool or dataset, and there is no answer file for this,
# so please do go forward with producing a simple script.

import os
import arcpy
arcpy.env.overwriteOutput = True

# near analysis on eelgrass to seeping underground storage tanks
base_directory = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Class_8_Functions"
os.chdir(base_directory)
aquatic_veg_dir = r"BIO_Submerged_Aquatic_Vegetation_2021_9037180976109638965\BIO_Submerged_Aquatic_Vegetation_2021.shp"
storage_tanks_dir = r"Leaking_Underground_Storage_Tanks_-6003799309786803486\Leaking_Underground_Storage_Tanks.shp"

# # See how long it takes for this process
s_time = time.time()

in_features = os.path.join(base_directory, aquatic_veg_dir)
near_features = os.path.join(base_directory, storage_tanks_dir)
search_radius = ""
location = "LOCATION"
angle = "ANGLE"
method = "GEODESIC"
field_names = ""
distance_unit = "Kilometers"

arcpy.analysis.Near(in_features,
                    near_features,
                    search_radius,
                    location,
                    angle,
                    method,
                    field_names,
                    distance_unit)

print("...Near analysis complete and it took", time.time() - s_time, "seconds to run and copy...")