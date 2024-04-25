import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Python Toolbox XYTable to Point to Intersect with ArcGIS Shapefile to New GRID Shapefile"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ProcessCSV_ToShapefile]


class ProcessCSV_ToShapefile(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "XY to Point Tool"
        self.description = "Takes csv with XY coordinate columns and converts to a shapefile of points"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_csv = arcpy.Parameter(name="input_csv",
                                     displayName="Input csv",
                                     datatype="DETable",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        input_csv.value = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Final_Toolboxes\GoM_occurrence_data\NWGOM18_CC_final.csv"  # This is a default value that can be over-ridden in the toolbox
        params.append(input_csv)

        output_points = arcpy.Parameter(name="output_points",
                                        displayName="Output shapefile",
                                        datatype="DEFeatureClass",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Output",  # Input|Output
                                        )
        output_points.value = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Final_Toolboxes\temporary_files\NWGOM18_CC_final_XYTableToPoint.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_points)

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        import os
        base_dir = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Final_Toolboxes"
        if not os.path.exists(os.path.join(base_dir, "temporary_files")):
            os.mkdir(os.path.join(base_dir, "temporary_files"))

        arcpy.env.workspace = base_dir

        in_table = parameters[0].valueAsText
        out_feature_class = parameters[1].valueAsText
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

        return





# This code block allows you to run your code in a test-mode within PyCharm, i.e. you do not have to open the tool in
# ArcMap. This works best for a "single tool" within the Toolbox.
def main():
    tool = ProcessCSV_ToShapefile()
    tool.execute(tool.getParameterInfo(), None)

if __name__ == '__main__':
    main()