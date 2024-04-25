import arcpy

arcpy.env.workspace = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Final_Toolboxes\GoM_occurrence_data"

in_table = r"\NWGOM18_CC_final.csv"
out_feature_class = "NWGOM18_CC_final_XYTableToPoint.shp"
x_field = "LongitudeInDD"
y_field = "LatitudeInDD"
z_field = ""
coordinate_system = arcpy.SpatialReference(4326)

arcpy.management.XYTableToPoint(in_table,
                                out_feature_class,
                                x_field,
                                y_field,
                                z_field,
                                coordinate_system)

print("done!")