"""
Philip Yang
NRS 528
Midterm project
Created on 14 Mar 2024

Description:
    This script imports xy point data from NOAA's Deep Sea Coral and Sponge portal for the NW Gulf of Mexico (GoM) for
    coral locations found above 200 m (a proxy boundary for mesophotic coral).
    Then, it imports oil rig location data as a shape file from BOEM. Using the 'near' tool it calculates the distance
    of a mesophotic coral location to the closest oil rig in the GoM.
    At the end, it makes a plot of the distance frequency to help visualize the results. The Deepwater Horizon oil spill
    in 2010 caused damage to soft and hard-bottom substrates as far as 14 km away according to Fisher et al. 2016.
    This is a brief foray into the vulnerability of mesophotic corals to other oil spill events in the GoM.

Resources:
    Coral and Sponge portal: https://www.ncei.noaa.gov/maps/deep-sea-corals/mapSites.htm
    BOEM GoM data: https://www.data.boem.gov/Main/Mapping.aspx
    Reference: Fisher, C.R., P.A. Montagna, and T.T. Sutton. 2016. How did the Deepwater Horizon oil spill impact deep-sea ecosystems? Oceanography 29(3):182–195, https://doi.org/10.5670/oceanog.2016.82.
"""

import os
import arcpy
import csv
import shutil
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##################################################### Users Edit #####################################################
# Change directory here
base_dir = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Midterm_pfy"

os.chdir(base_dir)

arcpy.env.overwriteOutput = True

keep_temp_files = False
######################################################## End #########################################################



##################################################### DO NOT EDIT ####################################################
# Create a temporary file subfolder and delete it when not needed
temp_folder = "temporary_files"
outputs = "output_files"

if not os.path.exists(os.path.join(base_dir, temp_folder)):
       os.mkdir(os.path.join(base_dir, temp_folder))
if not os.path.exists(os.path.join(base_dir, outputs)):
       os.mkdir(os.path.join(base_dir, outputs))
print(f"Created temporary folder: {temp_folder} in {os.getcwd()}")
print(f"Created output folder: {outputs} in {os.getcwd()}")
######################################################## End #########################################################



################################### Clean csv file and save to temporary folder as copy ##############################
# Input and output file paths
data_file = "deep_sea_corals_shallowTo200m_GoM.csv"
input_file_path = os.path.join(base_dir, data_file)
output_file_path = os.path.join(base_dir, temp_folder, "mesophotic_corals_GoM.csv")

# Read the CSV file and remove the second row
with open(input_file_path, "r", newline="") as input_file:
    csv_reader = csv.reader(input_file)
    rows = [row for index, row in enumerate(csv_reader) if index != 1]  # Exclude the second row

# Write to a new CSV file
with open(output_file_path, "w", newline="") as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerows(rows)

print("File saved successfully at:", output_file_path)
######################################################## End #########################################################



############################## Import coral location data - XY table to point and project ############################
# Change dir to temp folder
os.chdir(os.path.join(base_dir, temp_folder))
arcpy.env.workspace = os.path.join(base_dir, temp_folder)
print(f"The new working directory is {os.getcwd()}\n")

# See how long it takes for this process
XY_start_time = time.time()

# Inputs
in_table = "\mesophotic_corals_GoM.csv"
out_feature_class = "mesophotic_corals_GoM"
x_field = "longitude"
y_field = "latitude"
z_field = "DepthInMeters"
coordinate_system = arcpy.SpatialReference(4326) # Equidistant Cylindrical World

# Run tool
arcpy.management.XYTableToPoint(in_table,
                                out_feature_class,
                                x_field,
                                y_field,
                                z_field,
                                coordinate_system)

print("...Mesophotic coral points created and it took", time.time() - XY_start_time, "seconds, to make the mesophotic points from the table...")

# Project mesophotic points into Equidistant Cylindrical (World)
project1_start_time = time.time()

in_dataset = "mesophotic_corals_GoM.shp"
out_dataset = "mesophotic_corals_GoM_equaldis.shp"
out_coor_system = arcpy.SpatialReference(54002)
transform_method = ""
in_coor_system = arcpy.SpatialReference(4326)
preserve_shape = ""
max_deviation = ""
vertical = ""

arcpy.management.Project(in_dataset,
                         out_dataset,
                         out_coor_system,
                         transform_method,
                         in_coor_system,
                         preserve_shape,
                         max_deviation,
                         vertical)

if os.path.exists(os.path.join(base_dir, temp_folder, "mesophotic_corals_GoM_equaldis.shp")):
    print("...Mesophotic projection complete after", time.time() - project1_start_time, "seconds...")

######################################################## End #########################################################



########################### Import oil rigs, project and run near tool with mesophotic points ########################
# Duplicate oil platform data into temporary folder
source_dir = os.path.join(base_dir, "oil_platforms_GoM")
dest_dir = os.path.join(base_dir, temp_folder)

for filename in glob.glob(os.path.join(source_dir, '*.*')):
                shutil.copy(filename, dest_dir)
                print(f"Copied {filename} to {dest_dir}")

# Project oil platforms into Equidistant Cylindrical (World) too
project2_start_time = time.time()

in_dataset = "\platform.shp"
out_dataset = "oil_platforms_GoM.shp"
out_coor_system = arcpy.SpatialReference(54002)
transform_method = "NAD_1927_To_WGS_1984_1"
in_coor_system = arcpy.SpatialReference(4267)
preserve_shape = ""
max_deviation = ""
vertical = ""

arcpy.management.Project(in_dataset,
                         out_dataset,
                         out_coor_system,
                         transform_method,
                         in_coor_system,
                         preserve_shape,
                         max_deviation,
                         vertical)

if os.path.exists(os.path.join(base_dir, temp_folder, "oil_platforms_GoM.shp")):
    print("...Oil platforms projection complete after" , time.time() - project2_start_time, "seconds...")

# Run near tool
os.chdir(os.path.join(base_dir, temp_folder))
arcpy.env.workspace = os.chdir(os.path.join(base_dir, temp_folder))
print(f"Working directory is: {os.getcwd()}")

# # See how long it takes for this process
near_start_time = time.time()

in_features = "mesophotic_corals_GoM_equaldis.shp"
near_features = "oil_platforms_GoM.shp"
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

# Copy output to outputs folder
shapeFileName = os.path.join(base_dir, temp_folder, "mesophotic_corals_GoM_equaldis.shp")
outFeature = os.path.join(base_dir, outputs, "mesophotic_corals_GoM_equaldis_near.shp")
arcpy.CopyFeatures_management(shapeFileName, outFeature)

if os.path.exists(os.path.join(base_dir, outputs, "mesophotic_corals_GoM_equaldis_near.shp")):
                print("...Near analysis complete and it took", time.time() - near_start_time, "seconds to run and copy...")
######################################################## End #########################################################



#################################### Make and save plot of distance frequency ########################################
input = os.path.join(base_dir, outputs, "mesophotic_corals_GoM_equaldis_near.shp")

meso_df = pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(input,["NEAR_DIST"]))

print(meso_df.head())

# Define bin edges
bin_edges = np.arange(0, 51, 5)

# Calculate mean distance
mean_distance = meso_df['NEAR_DIST'].mean()

# Plotting
plt.figure(figsize=(8, 6))
meso_df['NEAR_DIST'].plot.hist(bins=bin_edges, edgecolor='black', alpha=0.7)
plt.xlabel('Nearest distance (km)', fontsize = 16)
plt.ylabel('Count', fontsize = 16)
plt.title('Count of nearest distances of mesophotic coral locations to an oil rig, GoM')
plt.xticks(bin_edges)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.axvline(mean_distance, color='red', linestyle='--', label=f'Mean Distance: {mean_distance:.2f}')
plt.tight_layout()
plt.legend()
plt.savefig(os.path.join(base_dir, outputs, "mesophotic_coral_nearest_dis_to_oil_rig_GoM.png"))
plt.show()
######################################################## End #########################################################



############################################ Delete Management #######################################################
# Need to change out of temp folder directory or there will be an error to delete
os.chdir(base_dir)

if keep_temp_files == False:
    print(f" ...Temporary folder being deleted...")
    # arcpy.Delete_management(os.path.join(base_dir, temp_folder)) # this does not delete folder, only contents
    # os.rmdir(os.path.join(base_dir, temp_folder)) # this should still work
    shutil.rmtree(os.path.join(base_dir, temp_folder)) # favorite method that removes the entire dir tree
######################################################################################################################