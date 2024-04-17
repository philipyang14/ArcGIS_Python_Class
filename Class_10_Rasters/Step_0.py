
#####
# Step 0 - Practice tasks before we start.
#####

# Task a: Run the buffer tool on Step_0_Data.zip/RI_Forest_Health_Works_Project_Points_All_Invasives.shp, with a
# distance of 1 mile:

import arcpy
arcpy.env.overwriteOutput = True
base_dir = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Class_10_Rasters\Step_0_Data"

arcpy.env.workspace = base_dir

input_shp = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Class_10_Rasters\Step_0_Data\RI_Forest_Health_Works_Project_Points_All_Invasives.shp"

in_features = input_shp
out_feature_class = "RI_Forest_Health_Works_Project_Points_All_Invasives_Buff_1mi.shp"
buffer_distance_or_field = "1 Mile"
line_side = ""
line_end_type = ""
dissolve_option = ""
dissolve_field =""
method =""

arcpy.analysis.Buffer(in_features, out_feature_class, buffer_distance_or_field,
                      line_side, line_end_type, dissolve_option, dissolve_field, method)

# Task b: Dissolve your resulting buffer:
# dissolve_option = "ALL"
#
# arcpy.analysis.Buffer(in_features, out_feature_class, buffer_distance_or_field,
#                       line_side, line_end_type, dissolve_option, dissolve_field, method)

arcpy.Dissolve_management("RI_Forest_Health_Works_Project_Points_All_Invasives_Buff_1mi.shp", "RI_Forest_Health_Works_Project_Points_All_Invasives_Buff_dissolve.shp")

# Task c: On the original point file (RI_Forest_Health_Works_Project_Points_All_Invasives.shp), use a
# search cursor to print the "Owner" field within the attributes.
input_shp = input_shp
fields = ['Owner']
with arcpy.da.SearchCursor(input_shp, fields) as cursor:
    for row in cursor:
        print(u'Owner = {0}'.format(row[0]))
