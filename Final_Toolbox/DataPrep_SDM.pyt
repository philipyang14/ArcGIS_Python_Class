import time

import arcpy
import os
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import time

base_dir = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Final_Toolbox"
arcpy.env.overwriteOutput = True

''' 
Philip Yang
Final toolbox project
NRS 528

This toolbox takes one csv file of habitat occurrence data (Marissa Nuttall, NOAA FGB NMS) and intersects it with a 
5 by 5 m bathymetry mosaic tif (FGB NMS, USGS, mosaicked by Philip) and creates a new raster that possesses cells with 
the most common habitat value from the point shapefile. Then, a new raster is built from that in-between raster where any 
habitat values of "Coralline algae" are assigned a new field value of 1 and the other two values (Deep reef and soft bottom)
are assigned a value of 0. This is to create a final output raster that contains the occurrence data of coralline algae 
from this dataset in a raster format that overlaps with the 5 by 5 bathymetry mosaic.


'''

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file). Python Toolbox XYTable to Point to Intersect with ArcGIS Shapefile to New GRID Shapefile"""
        self.label = "Processing Data for Habitat Distribution Modelling"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ProcessCSV_ToShapefile, Intersect_PointToRaster]


class ProcessCSV_ToShapefile(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "XY to Point Tool"
        self.description = "Takes csv with XY coordinate columns and converts to a shapefile of points"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_folder = arcpy.Parameter(name="input_folder",
                                     displayName="Input folder with csv files",
                                     datatype="DEFolder",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        input_folder.value = os.path.join(base_dir, "GoM_occurrence_data")  # This is a default value that can be over-ridden in the toolbox
        params.append(input_folder)

        output_folder = arcpy.Parameter(name="output_folder",
                                        displayName="Output folder",
                                        datatype="DEFolder",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Output",  # Input|Output
                                        )
        output_folder.value = os.path.join(base_dir, "temporary_files")  # This is a default value that can be over-ridden in the toolbox
        params.append(output_folder)

        output_points = arcpy.Parameter(name="output_points",
                                        displayName="Output shapefile",
                                        datatype="DEFeatureClass",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Output",  # Input|Output
                                        )
        output_points.value = os.path.join(base_dir, "temporary_files", "NWGOM18_CC_final_XYTableToPoint.shp")  # This is a default value that can be over-ridden in the toolbox
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

        in_folder = parameters[0].valueAsText
        temp_folder = parameters[1].valueAsText
        out_feature_class = parameters[2].valueAsText

        # Create output folder
        if not os.path.exists(temp_folder):
            os.mkdir(temp_folder)

        print("\nProcessing CSV files in folder:", in_folder)
        print("Files should show up in:", temp_folder)

        # Initialize an empty list to store DataFrame objects
        dfs = []

        # Iterate over CSV files in the folder
        for csv_file in glob.glob(os.path.join(in_folder, "*.csv")):
            print("\n",os.path.basename(csv_file))
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file, low_memory=False)

            # Check if "Major Habitat" column exists - only a problem with the Nuttall dataset
            if "Major Habitat" and "Level 6: Macrohabitat" and "Level 7: Habitat" in df.columns:
                # Rename "Major Habitat" column to "Habitat"
                df.rename(columns={"Major Habitat": "Habitat"}, inplace=True)
                df.drop(columns={"Level 6: Macrohabitat"}, inplace=True) # Find the other columns named 'habitat' that we don't want and drop them
                df.drop(columns={"Level 7: Habitat"}, inplace=True)
            else: print("\nNo column called 'Major Habitat' in the CSV file:", csv_file)
            print(df)

            # Create a new DataFrame with selected columns
            selected_df = pd.DataFrame()

            # Rename selected columns and add to the new DataFrame
            for col in df.columns:
                if "latitude" in col.lower():
                    selected_df["Latitude"] = df[col]
                elif "longitude" in col.lower():
                    selected_df["Longitude"] = df[col]
                elif "depth" in col.lower():
                    selected_df["DepthInMeters"] = df[col]
                elif "habitat" in col.lower():
                    selected_df["Habitat"] = df[col]


            # # Keep only the first four selected columns
            selected_df = selected_df.iloc[:, :4]
            print(selected_df)

            # Add the source filename as a new column filled with the filename
            selected_df['source_file'] = os.path.splitext(os.path.basename(csv_file))[0]

            # Add the DataFrame to the list
            dfs.append(selected_df)

        # Concatenate all DataFrames in the list along the rows (axis=0)
        concatenated_df = pd.concat(dfs, ignore_index=True)
        print(concatenated_df)

        # Write the concatenated DataFrame to a new CSV file
        occurrence_all_csv = os.path.join(temp_folder, "occurrence_all.csv")
        concatenated_df.to_csv(occurrence_all_csv, index=False)
        print("CSV files have been processed and concatenated successfully!")

        # See the unique values in habitat:
        df = pd.read_csv(occurrence_all_csv)
        column_name = "Habitat"
        value_counts = df[column_name].value_counts()
        print("\nThe unique values in the dataset are:","\n",value_counts, "\nWe want to standardize them")

        # Recode Habitat column to standardize the data
        recoding_codes = {
            "Coralline Algae": ["Coralline Algae",
                                 "Algal Nodules",
                                 "Coralline algae",
                                 "Coralline Algal Reef",
                                 "Coralline Algae Reef",
                                 "Corraline Algae",
                                 "Coralline Aglae",
                                 "Algal nodules",
                                 "Algal Nodules "],
            "Soft Bottom": ["Soft Bottom",
                             "Soft Substrate",
                             "Soft bottom",
                             "Soft Bottom ",
                             "soft bottom"],
            "Deep Reef": ["Deep Reef",
                          "Deep Reef ",
                           "Deep reef",
                           "Deep Coral",
                           "Deep Reefs",],
            "Reef": ["Reef",
                     "Coral Reef",
                     "Coral Community",
                     "Coral Reef "]
        }
        values_to_drop = ["Brine Seep", "Mud Volcano"]

        # Load the DataFrame from the "occurrence_all.csv" file
        occurrence_all_csv = os.path.join(temp_folder, "occurrence_all.csv")
        df = pd.read_csv(occurrence_all_csv)

        # Drop rows with values we are not interested in
        mask = df['Habitat'].isin(values_to_drop)
        df = df[~mask]
        # Drop rows where either latitude or longitude has no value
        df.dropna(subset=['Latitude', 'Longitude'], inplace=True)

        # Recode the "Habitat" column based on the provided codes
        for new_value, old_values in recoding_codes.items():
            for old_value in old_values:
                df.loc[df['Habitat'].str.lower() == old_value.lower(), 'Habitat'] = new_value
        print(df)
        column_names = ["Habitat", "Latitude", "Longitude", "DepthInMeters"]
        value_counts = df[column_names[0]].value_counts()
        print(value_counts)
        df = df.dropna(subset=['Habitat'])

        # Deal with DepthInMeters not being a float
        # Convert non-numeric values to NaN
        df[column_names[3]] = pd.to_numeric(df[column_names[3]], errors='coerce')
        print(df.info())
        df[column_names[3]] = df[column_names[3]].astype(float)
        # print(df.info())

        # Check if any value in the column is not negative
        if (df['DepthInMeters'] >= 0).any():
            # Print a message indicating that not all values are negative
            print("\nWarning: Some values in 'DepthInMeters' column are not negative. Processing...")
            # Modify values to make them negative
            df.loc[df['DepthInMeters'] >= 0, 'DepthInMeters'] *= -1

        # Test to check that they were all converted
        if (df['DepthInMeters'] < 0).any():
            print("...All values in 'DepthInMeters' column are now negative.")

        print("\nThe order of the integers for x axis of habitats should follow this left to right: ",
              df['Habitat'].unique(), "Could not figure out for hours why PyCharm and PLT don't like categories here, "
                                      "but if the order is correct it seems Reef and Deep Reef depth ranges are not different")
        # Convert 'Habitat' column to categorical data type
        df['Habitat'] = df['Habitat'].astype('category')
        # Replace 'DepthInMeters' and 'Habitat' with actual column names from your DataFrame
        sns.boxplot(x=df['Habitat'], y='DepthInMeters', data=df)
        plt.title("LEFT TO RIGHT SHOULD BE:" "'Soft Bottom' 'Deep Reef 'Coralline Algae' 'Reef'")
        plt.xlabel('Habitat')
        plt.ylabel('Depth in Meters')
        # Add figure caption
        fig_caption = (
            "Figure 1: Boxplot of Depth in Meters by Habitat. The order of categories from 0 to 3 corresponds to "
            "the unique values: ['Soft Bottom' 'Deep Reef' 'Coralline Algae' 'Reef']")
        plt.text(0.5, -0.1, fig_caption, ha='center', fontsize=10, transform=plt.gcf().transFigure)
        plt.show()
        print("\n")

        # Check if any column contains NaN values
        for colname in column_names:
            if df[colname].isna().any():
                print(f"The column '{colname}' contains NaN values.")
            else:
                print(f"The column '{colname}' does not contain NaN values.")

        # Save the cleaned DataFrame to a new CSV file
        occurrence_all_clean_csv = os.path.join(temp_folder, "occurrence_all_clean.csv")
        df.to_csv(occurrence_all_clean_csv, index=False)

        print(f"\nCleaned DataFrame saved to {occurrence_all_clean_csv}")

        # Now we are ready to create a XY Point Shapefile!
        print("\nMaking Point Shapefile...")
        # Define the tool variables
        in_table = os.path.join(temp_folder, "occurrence_all_clean.csv")
        x_field = "Longitude"
        y_field = "Latitude"
        z_field = ""
        coordinate_system = arcpy.SpatialReference(4326) # WGS 1984

        arcpy.management.XYTableToPoint(in_table,
                                        out_feature_class,
                                        x_field,
                                        y_field,
                                        z_field,
                                        coordinate_system)

        if arcpy.Exists(out_feature_class):
            arcpy.AddMessage(" Point Shapefile Created!")
        else: arcpy.AddMessage("Point Shapefile Not Created :`(")

        return


# This code block allows you to run your code in a test-mode within PyCharm, i.e. you do not have to open the tool in
# ArcMap. This works best for a "single tool" within the Toolbox.
# def main():
#     tool = ProcessCSV_ToShapefile()
#     tool.execute(tool.getParameterInfo(), None)
#
# if __name__ == '__main__':
#     main()

class Intersect_PointToRaster(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Intersect Point Shapefile with Grid"
        self.description = "Create a fishnet grid based on a bathymetry mosaic and habitat occurrence points"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_points = arcpy.Parameter(name="input_points",
                                     displayName="Input points",
                                     datatype="DEShapeFile",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        input_points.value = os.path.join(base_dir, "temporary_files", "NWGOM18_CC_final_XYTableToPoint.shp")  # This is a default value that can be over-ridden in the toolbox
        params.append(input_points)

        habitat_field = arcpy.Parameter(name="habitat_field",
                                        displayName="Habitat field",
                                        datatype="GPString",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Output",  # Input|Output
                                        )
        habitat_field.value = "Habitat"  # This is a default value that can be over-ridden in the toolbox
        params.append(habitat_field)

        input_raster = arcpy.Parameter(name="input_raster",
                                        displayName="Input raster",
                                        datatype="GPRasterLayer",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        input_raster.value = os.path.join(base_dir, "fgb_bathy_mosaic", "fgb_mosaic_bathy_mercator.tif")  # This is a default value that can be over-ridden in the toolbox
        params.append(input_raster)

        output_folder = arcpy.Parameter(name="output_folder",
                                        displayName="Output folder",
                                        datatype="DEFolder",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        output_folder.value = os.path.join(base_dir, "temporary_files") # This is a default value that can be over-ridden in the toolbox
        params.append(output_folder)

        habitat_name = arcpy.Parameter(name="habitat_name",
                                        displayName="Habitat name",
                                        datatype="GPString",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Output",  # Input|Output
                                        )
        habitat_name.value = "FGB_Fishnet"  # This is a default value that can be over-ridden in the toolbox
        params.append(habitat_name)

        output_raster = arcpy.Parameter(name="output_raster",
                                        displayName="Output raster",
                                        datatype="GPRasterLayer",
                                        parameterType="Derived",  # Required|Optional|Derived
                                        direction="Output",  # Input|Output
                                        )
        output_raster.value = os.path.join(base_dir, "temporary_files", "habitat_raster.tif")  # This is a default value that can be over-ridden in the toolbox
        params.append(output_raster)

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

        point_shapefile = parameters[0].valueAsText
        habitat_field = parameters[1].valueAsText
        raster_file = parameters[2].valueAsText
        output_folder = parameters[3].valueAsText
        output_name = parameters[4].valueAsText
        output_raster = parameters[5].valueAsText

        # Create a file geodatabase becauase the fishnet shapefile will be > 2gb
        def create_file_geodatabase(output_folder, geodatabase_name):
            '''Create a file geodatabase'''
            geodatabase_path = arcpy.CreateFileGDB_management(output_folder, geodatabase_name)
            print(f"\nFile geodatabase created at: {geodatabase_path}")

        # Use function:
        output_folder = output_folder
        geodatabase_name = "habitat_occurrence_fgb.gdb"
        create_file_geodatabase(output_folder, geodatabase_name)

        def describe_raster(raster_file):
            '''Describe the raster file for creating a fishnet grid'''
            desc = arcpy.Describe(raster_file)
            extent = desc.extent
            xmin, ymin, xmax, ymax = extent.XMin, extent.YMin, extent.XMax, extent.YMax
            cell_width, cell_height = desc.meanCellWidth, desc.meanCellHeight

            # Return the values according to your specified format
            return {
                'XMin': xmin,
                'XMax': xmax,
                'YMin': ymin,
                'YMax': ymax,
                'CellWidth': cell_width,
                'CellHeight': cell_height
            }

        # Run function:
        raster_info = describe_raster(raster_file)
        print("\nRaster extent information:", raster_info)

        def create_fishnet(output_folder, geodatabase_name, output_name, raster_info):
            '''Create a fishnet identical to the raster extent'''
            xmin, ymin = raster_info['XMin'], raster_info['YMin']
            xmax, ymax = raster_info['XMax'], raster_info['YMax']
            cell_width, cell_height = raster_info['CellWidth'], raster_info['CellHeight']

            out_feature_class = os.path.join(output_folder, geodatabase_name, output_name)
            # Set the origin of the fishnet
            origin_coord = str(xmin) + " " + str(ymin)  # Left bottom of our point data
            y_axis_coord = str(xmin) + " " + str(ymin + 1)  # This sets the orientation on the y-axis, so we head north
            cell_width = cell_width
            cell_height = cell_height
            number_rows = ""  # Leave blank, as we have set cellSize
            number_columns = ""  # Leave blank, as we have set cellSize
            oppositeCorner = str(xmax) + " " + str(ymax)  # i.e. max x and max y coordinate
            labels = "NO_LABELS"
            templateExtent = "#"  # No need to use, as we have set yAxisCoordinate and oppositeCorner
            geometryType = "POLYGON"  # Create a polygon, could be POLYLINE

            arcpy.management.CreateFishnet(out_feature_class,
                                           origin_coord,
                                           y_axis_coord,
                                           cell_width,
                                           cell_height,
                                           number_rows,
                                           number_columns,
                                           oppositeCorner,
                                           labels,
                                           templateExtent,
                                           geometryType)

        print("Creating fishnet in", geodatabase_name, "...")
        start_time = time.time()
        create_fishnet(output_folder, geodatabase_name, output_name, raster_info)
        print("Fishnet created! It took ", time.time() - start_time, "seconds to make.")

        return

# This code block allows you to run your code in a test-mode within PyCharm, i.e. you do not have to open the tool in
# ArcMap. This works best for a "single tool" within the Toolbox.
def main():
    tool = Intersect_PointToRaster()
    tool.execute(tool.getParameterInfo(), None)

if __name__ == '__main__':
    main()