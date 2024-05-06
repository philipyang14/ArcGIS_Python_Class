# Philip Yang
# NRS 528
# Coding Challenge 8

# Requirements:
# Our coding challenge this week follows from the last exercise that we did in class during Week 8 where we worked with functions.
#
# Convert some of your earlier code into a function. The only rules are:
# 1) You must do more than one thing to your input to the function, and
# 2) the function must take two arguments or more.
# You must also, 3) provide a zip file of example data within your repo.
#
# Plan the task to take an hour or two, so use one of the simpler examples from our past classes.

# GOAL: Create function that prepares a projected shapefile from a csv for any future analysis
import arcpy, os, csv, shutil

########################################## Change base_dir here ########################################################
base_dir = r'C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Coding_Challenge_8_pfy'

# Input data
data_folder = r"raw_data_files\raw_data_files" # Oil platform shapefile not used in the data_files for this code, only the .csv
csv_data_file = "deep_sea_corals_shallowTo200m_GoM.csv"

# Ouput shapefile desired name
shapefile_name = "mesophotic_corals_GoM.shp"

################################################ END ###################################################################



############################################## Create function #########################################################
def prepare_shapefile_from_csv(base_dir, data_folder, csv_data_file, shapefile_name):
    # settings
    os.chdir(base_dir)
    arcpy.env.overwriteOutput = True
    keep_temp_files = False
    data_folder = data_folder

    # make directories
    temp_folder = "temporary_files"
    outputs = "output_files"

    if not os.path.exists(os.path.join(base_dir, temp_folder)):
            os.mkdir(os.path.join(base_dir, temp_folder))
    if not os.path.exists(os.path.join(base_dir, outputs)):
            os.mkdir(os.path.join(base_dir, outputs))

    print(f"\n Created temporary folder: {temp_folder} in {os.getcwd()}")
    print(f"\n Created output folder: {outputs} in {os.getcwd()}")

    # input and output file path:
    input_file_path = os.path.join(base_dir, data_folder, csv_data_file)
    output_file_path = os.path.join(base_dir, temp_folder, f"{csv_data_file}")

    # make shapefile from csv data
    with open(input_file_path, "r", newline="") as input_file:
        csv_reader = csv.reader(input_file)
        rows = [row for index, row in enumerate(csv_reader) if index != 1]  # Exclude the second row

    # Write to a new CSV file
    with open(output_file_path, "w", newline="") as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerows(rows)

    print("\n File saved successfully at:", output_file_path)

    # Process data into shapefile
    if os.path.exists(output_file_path):
        print(f"\n Processing {csv_data_file} into {shapefile_name}...")
        XY_start_time = time.time()
        # Inputs
        in_table = os.path.join(base_dir, temp_folder, csv_data_file)
        out_feature_class = os.path.join(base_dir, outputs, shapefile_name)
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

        print("\n...Shapefile created and it took", time.time() - XY_start_time, "seconds, to make the shapefile from the csv")
    else: print("input file does not exist")

    # Project shapefile into Equidistant Cylindrical (World)
    if os.path.exists(os.path.join(base_dir, outputs, shapefile_name)):

        print(f"\n Projecting the shapefile...")
        projection_start_time = time.time()
        in_dataset = os.path.join(base_dir, outputs, shapefile_name)
        out_dataset = os.path.join(base_dir, outputs, "projected_" + shapefile_name)
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
    else: print("Shapefile does not exist")

    if os.path.exists(os.path.join(base_dir, outputs, f"projected_{shapefile_name}")):
        print("\n...Shapefile projection complete after", time.time() - projection_start_time, "seconds")
    else: print("\n PROCESS NOT FINISHED")

    # Delete the temp directory
    os.chdir(base_dir)

    if keep_temp_files == False:
        print(f"\n Temporary folder being deleted and ")
        # arcpy.Delete_management(os.path.join(base_dir, temp_folder)) # this does not delete folder, only contents
        # os.rmdir(os.path.join(base_dir, temp_folder)) # this should still work
        shutil.rmtree(os.path.join(base_dir, temp_folder))  # favorite method that removes the entire dir tree

################################################### END ################################################################



################################################### Run function #######################################################
prepare_shapefile_from_csv(base_dir, data_folder, csv_data_file, shapefile_name)
