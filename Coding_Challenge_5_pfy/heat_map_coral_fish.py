# Philip Yang
# NRS 528
# Coding Challenge 5

# Description: creating heat maps for two species, one scleractinian coral (Montipora foliosa) and one reef associated fish (Pseudanthias squamipinnis)

import arcpy
import pandas as pd
# import os

# Code to create a single csv file
# KEEP COMMENTED OUT BECAUSE THE ORIGINAL CSV's DO NOT EXIST ANYMORE:

# # Specify the path to your desired working directory
# working_directory = "C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Coding_Challenge_5_pfy"
#
# # Use os.chdir() to change the current working directory
# os.chdir(working_directory)
#
# # Load Montipora_foliosa
# montipora_df = pd.read_csv("Montipora_foliosa.csv", usecols=["decimallongitude", "decimallatitude", "date_year", "scientificname", "depth"])
#
# # Load Pseudanthias_squamipinnis
# pseudanthias_df = pd.read_csv("Pseudanthias_squamipinnis.csv", usecols=["decimallongitude", "decimallatitude", "date_year", "scientificname", "depth"])
#
# # Concatenate
# concatenated_df = pd.concat([montipora_df, pseudanthias_df])
#
# # Save as a new CSV file
# concatenated_df.to_csv("Coral_and_Fish_distribution.csv", index=False)


# Set the workspace
# *************** Andy change to this path to where this folder is on your machine ********************
arcpy.env.workspace = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Coding_Challenge_5_pfy"
arcpy.env.overwriteOutput = True

# Load the concatenated CSV file
concatenated_df = pd.read_csv("Coral_and_Fish_distribution.csv")

# Separate data frames based on unique values in the "scientificname" column
foliosa_df = concatenated_df[concatenated_df['scientificname'] == 'Montipora foliosa']
squamipinnis_df = concatenated_df[concatenated_df['scientificname'] == 'Pseudanthias squamipinnis']

# Check the df's
# print(foliosa_df.head(-10))
# print(squamipinnis_df.head(-10))

# Save df as new csv's

foliosa_df.to_csv("Montipora_foliosa.csv", index=False, mode='w')
print("Coral saved as csv")
squamipinnis_df.to_csv("Pseudanthias_squamipinnis.csv", index=False,  mode='w')
print("Grouper (fish) saved as csv")

######################## HEAT MAP MONTIPORA ########################

# Convert Montipora_foliosa.csv to a shapefile.

in_Table = r"Montipora_foliosa.csv"
x_coords = "decimallongitude"
y_coords = "decimallatitude"
out_Layer = "Montipora"
saved_Layer = r"Montipora_Output.shp"

# Set the spatial reference
spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, "")

# Print the total rows
print(arcpy.GetCount_management(out_Layer))
# Save to a layer file
arcpy.CopyFeatures_management(lyr, saved_Layer)
if arcpy.Exists(saved_Layer):
    print("Created Montipora shape file!")

# Extract the Extent, i.e. XMin, XMax, YMin, YMax of the shapefile.

desc = arcpy.Describe(saved_Layer)
XMin = desc.extent.XMin
XMax = desc.extent.XMax
YMin = desc.extent.YMin
YMax = desc.extent.YMax

# Generate a fishnet for Montipora shp file

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

outFeatureClass = "Montipora_Fishnet.shp"  # Name of output fishnet

# Set the origin of the fishnet
originCoordinate = str(XMin) + " " + str(YMin)  # Left bottom of our point data
yAxisCoordinate = str(XMin) + " " + str(YMin + 1)  # This sets the orientation on the y-axis, so we head north
cellSizeWidth = "1" # use 1 degree? How to determine this? 1 degree is about 110 km near equator
cellSizeHeight = "1"
numRows = ""  # Leave blank, as we have set cellSize
numColumns = "" # Leave blank, as we have set cellSize
oppositeCorner = str(XMax) + " " + str(YMax)  # i.e. max x and max y coordinate
labels = "NO_LABELS"
templateExtent = "#"  # No need to use, as we have set yAxisCoordinate and oppositeCorner
geometryType = "POLYGON"  # Create a polygon, could be POLYLINE

arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                               cellSizeWidth, cellSizeHeight, numRows, numColumns,
                               oppositeCorner, labels, templateExtent, geometryType)

if arcpy.Exists(outFeatureClass):
    print("Created Montipora Fishnet file!")


# Spatial Join to join the fishnet to the observed points.

target_features="Montipora_Fishnet.shp"
join_features="Montipora_Output.shp"
out_feature_class="Montipora_HeatMap.shp"
join_operation="JOIN_ONE_TO_ONE"
join_type="KEEP_ALL"
field_mapping=""
match_option="INTERSECT"
search_radius=""
distance_field_name=""

arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                           join_operation, join_type, field_mapping, match_option,
                           search_radius, distance_field_name)

# Check that the heatmap is created and delete the intermediate files

if arcpy.Exists(out_feature_class):
    print("Created Montipora Heatmap file!")
    print("Deleting Montipora intermediate files")
    arcpy.Delete_management(target_features)
    arcpy.Delete_management(join_features)

######################## HEAT MAP PSEUDANTHIAS ########################

# Convert Pseudanthias_squamipinnis.csv to a shapefile.

in_Table = r"Pseudanthias_squamipinnis.csv"
x_coords = "decimallongitude"
y_coords = "decimallatitude"
out_Layer = "Pseudanthias"
saved_Layer = r"Pseudanthias_Output.shp"

# Set the spatial reference
spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, "")

# Print the total rows
print(arcpy.GetCount_management(out_Layer))
# Save to a layer file
arcpy.CopyFeatures_management(lyr, saved_Layer)
if arcpy.Exists(saved_Layer):
    print("Created Pseudanthias shape file!")

# Extract the Extent, i.e. XMin, XMax, YMin, YMax of the shapefile.

desc = arcpy.Describe(saved_Layer)
XMin = desc.extent.XMin
XMax = desc.extent.XMax
YMin = desc.extent.YMin
YMax = desc.extent.YMax

# Generate a fishnet

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

outFeatureClass = "Pseudanthias_Fishnet.shp"  # Name of output fishnet

# Set the origin of the fishnet
originCoordinate = str(XMin) + " " + str(YMin)  # Left bottom of our point data
yAxisCoordinate = str(XMin) + " " + str(YMin + 1)  # This sets the orientation on the y-axis, so we head north
cellSizeWidth = "1" # Use 1 degree? Try to figure out why we choose this - what is the basis? Want to see how many every 110 km?
cellSizeHeight = "1"
numRows = ""  # Leave blank, as we have set cellSize
numColumns = "" # Leave blank, as we have set cellSize
oppositeCorner = str(XMax) + " " + str(YMax)  # i.e. max x and max y coordinate
labels = "NO_LABELS"
templateExtent = "#"  # No need to use, as we have set yAxisCoordinate and oppositeCorner
geometryType = "POLYGON"  # Create a polygon, could be POLYLINE

arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                               cellSizeWidth, cellSizeHeight, numRows, numColumns,
                               oppositeCorner, labels, templateExtent, geometryType)

if arcpy.Exists(outFeatureClass):
    print("Created Pseudanthias Fishnet file!")


# Spatial Join to join the fishnet to the observed points.

target_features="Pseudanthias_Fishnet.shp"
join_features="Pseudanthias_Output.shp"
out_feature_class="Pseudanthias_HeatMap.shp"
join_operation="JOIN_ONE_TO_ONE"
join_type="KEEP_ALL"
field_mapping=""
match_option="INTERSECT"
search_radius=""
distance_field_name=""

arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                           join_operation, join_type, field_mapping, match_option,
                           search_radius, distance_field_name)

# Check that the heatmap is created and delete the intermediate files (e.g. species shapefile and fishnet).

if arcpy.Exists(out_feature_class):
    print("Created Pseudanthias Heatmap file successfully!")
    print("Deleting Pseudanthias intermediate files")
    arcpy.Delete_management(target_features)
    arcpy.Delete_management(join_features)
