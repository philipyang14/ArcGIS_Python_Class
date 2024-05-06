# Philip Yang
# NRS 528
# Coding Challenge 4
# Requirements:
# 1. Comment your code well.
# 2. Ensure that the code will run on my machine with only a single change to a single variable (i.e. a base folder location).


import arcpy
from arcpy.sa import *
import time

# Goal: use the XYTable to Point Tool and then the Kernel Density Tool to see where research efforts and discovery of
# mesophotic coral (defined as 30 m to 150 m depth) have occurred over the decades

############################## ANDY CHANGE TO DIRECT TO FOLDER "Coding_Challenge_4_pfy" ###############################

# Change to your base directory
base_dir = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Coding_Challenge_4_pfy"

arcpy.env.workspace = base_dir
arcpy.env.scratchWorkspace = base_dir

arcpy.AddMessage("The new current workspace is: %s" % arcpy.env.workspace)
arcpy.AddMessage("The new scratch workspace is: %s" % arcpy.env.scratchWorkspace)

# allow overwriting of files
arcpy.env.overwriteOutput = True

########################################################## END ########################################################



########## Import mesophotic coral (MCE) NOAA csv data and turn into points using the XYTable to Point tool:###########

# # See how long it takes XYPointToTable to run
XY_start_time = time.time()

# arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field, {z_field}, {coordinate_system})
# https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/xy-table-to-point.htm

# Inputs
in_table = "\mcePoints_filter.csv"
out_feature_class = "MCE_points"
x_field = "longitude"
y_field = "latitude"
z_field = "DepthInMeters"
coordinate_system = arcpy.SpatialReference(4326, 5714)

# Run tool
arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field, z_field, coordinate_system)

print("MCE location points created")

print("It took", time.time() - XY_start_time, "seconds, to make the MCE points from the table")

########################################################## END ########################################################



################### Use the Kernel Density Tool to see the density of MCE in the Gulf of Mexico (GoM):#################

# Set extent for the Kernel density analysis
arcpy.env.extent = arcpy.Extent(-97, 25, -85, 29)

# See how long it takes Kernel Density to run
KD_start_time = time.time()

# KernelDensity from: https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/kernel-density.htm

# Inputs
in_features = "\MCE_points.shp"
population_field = "#" # use shape and name if z-values exist, default is None
cell_size = "#"
search_radius = 1000 # 1 km radius
area_unit_scale_factor = "SQUARE_KILOMETERS"
out_cell_values = "DENSITIES" # Default. The output values represent the calculated density value per unit area for each cell.
method = "#" # default to planar
in_barriers = "#"

# Had to adjust some of the inputs because I was running ArcGIS 2.4
output_raster = "MCE_KernelDensity_GoM.tif"

outKernelDensity = KernelDensity(in_features, population_field, cell_size, search_radius, area_unit_scale_factor, out_cell_values, method)

# Save the output
# outKernelDensity.save("\MCE_KernelDensity_GoM.tif")

print("MCE kernel density calculated and saved")

print("It took", time.time() - KD_start_time, "seconds, to run the kernel density analysis")

########################################################## END ########################################################
