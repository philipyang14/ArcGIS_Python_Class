
#####
# Step 1 - Zonal stats and extracting values to points
#####

# Raster processing in arcpy is very similar to working with shapefiles and other feature classes. In this example, we
# conduct some zonal statistics and undertake point value extraction from a raster.

# Using Step_1_Data.zip, extract the zonal values for the shapefile: Biogeography_Made_Up.shp, and the sst_mean.tif
# raster.
import arcpy, os, glob
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
base_dir = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Class_10_Rasters\Step_1_Data"
arcpy.env.workspace = base_dir
arcpy.gp.ZonalStatisticsAsTable_sa("Biogeography_Made_Up.shp", "Area", "sst_mean.tif", "sst_mean_zones.dbf", "DATA", "ALL")


# Pulling values from a raster using a point shapefile is also pretty easy, this time, we use the Extract Values tool.
arcpy.gp.ExtractValuesToPoints_sa("Great_Whites.shp", "sst_mean.tif", "Great_Whites_Extract.shp", "NONE", "VALUE_ONLY")

# Task 1 -  Using a for loop, process all three *.tif files for SST (mean, min and max), you will need to edit the code from lines 11-15 above.
# HInt: ZonalStats... is sensitive to file name output, you may need to use something that shortens the output table name:
# e.g. file_name = raster[:6] + "_out.dbf"

os.chdir(base_dir)
# Case-insensitive globbing function
tif_files = glob.glob('*.tif')

# Print the list of .tif files
print(tif_files)

def process_tifs(tif_files):
    for tif in tif_files:
        file_name = tif[:6] + "_out.dbf"
        arcpy.gp.ZonalStatisticsAsTable_sa("Biogeography_Made_Up.shp", "Area", tif, file_name, "DATA", "ALL")
        print(tif, "Zonal statistics calculated")

process_tifs(tif_files)

# Task 2 - I want you to run the tool above on the rasters provided (mean, min and max). Think about how you will do this,
# maybe search online about extracting multiple values to points, is here a different tool available to the above that
# allows for multiple inputs?

# https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/extract-multi-values-to-points.htm

in_point_features = "Great_Whites.shp"
in_rasters = tif_files
bilinear_interpolate_values =""

arcpy.ListRasters() # this is another way to make a list of rasters

arcpy.sa.ExtractMultiValuesToPoints(in_point_features, in_rasters, bilinear_interpolate_values)
print("\nDone multi values to points")