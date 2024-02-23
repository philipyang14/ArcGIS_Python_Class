# Philip Yang
# NRS 528
# Coding Challenge 4

import arcpy
from arcpy import env
from arcpy.sa import *
import time

# Goal: use the XYTable to Point Tool and then the Kernel Density Tool to see where research efforts and discovery of mesophotic coral (defined as 30 m to 150 m depth) have occurred over the decades

# check the current workspace
arcpy.AddMessage("The passed-down current workspace is: %s" % arcpy.env.workspace)
arcpy.AddMessage("The passed-down scratch workspace is: %s" % arcpy.env.scratchWorkspace)

#### ANDY CHANGE TO DIRECT TO FOLDER "Coding_Challenge_4_pfy" #####
arcpy.env.workspace = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Coding_Challenge_4_pfy"
arcpy.env.scratchWorkspace = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Coding_Challenge_4_pfy"

arcpy.AddMessage("The new current workspace is: %s" % arcpy.env.workspace)
arcpy.AddMessage("The new scratch workspace is: %s" % arcpy.env.scratchWorkspace)

# allow overwriting of files
arcpy.env.overwriteOutput = True

#### Import mesophotic coral (MCE) NOAA csv data and turn into points using the XYTable to Point tool:

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


#### Use the Kernel Density Tool to see the density of MCE and where research has occurred in the Gulf of Mexico (GoM):

# set extent for the Kernel density analysis
arcpy.env.extent = arcpy.Extent(-97, 25, -85, 29)

# See how long it takes Kernel Density to run
KD_start_time = time.time()

# KernelDensity(in_features, population_field, {cell_size}, {search_radius}, {area_unit_scale_factor}, {out_cell_values}, {method}, {in_barriers}) from:
# https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/kernel-density.htm

# Inputs
in_features = "\MCE_points.shp"
population_field = "#" # use shape and name if z-values exist, default is None
cell_size = "#" # Wanted to use 10 m to relate it with highest bathymetry resolution for area (BOEM), but could not figure out syntax type: https://pro.arcgis.com/en/pro-app/3.1/tool-reference/tool-errors-and-warnings/001001-010000/tool-errors-and-warnings-00626-00650-000628.htm
search_radius = 1000 # 1 km radius
area_unit_scale_factor = "SQUARE_KILOMETERS"
out_cell_values = "DENSITIES" # Default. The output values represent the calculated density value per unit area for each cell.
method = "#" # default to planar
in_barriers = "#"

# Had to adjust some of the inputs because I was running ArcGIS 2.4
output_raster = "MCE_KernelDensity_GoM.tif"

outKernelDensity = KernelDensity(in_features, population_field, cell_size, search_radius, area_unit_scale_factor, out_cell_values, method) # running arcGIS 2.4 KD only allowed 2-7 args not 8

#### ANDY uncomment this to run on ArcGIS 3.2 and comment above
# outKernelDensity = KernelDensity(in_features, population_field, cell_size, search_radius, area_unit_scale_factor, out_cell_values, method, in_barriers)

# Save the output
# outKernelDensity.save("\MCE_KernelDensity_GoM.tif")

print("MCE kernel density calculated and saved")

print("It took", time.time() - KD_start_time, "seconds, to run the kernel density analysis")
