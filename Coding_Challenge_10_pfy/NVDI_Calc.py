'''
Philip Yang
NRS 528
Coding Challenge 10

Task:

Our coding challenge this week that improves our practice with rasters from Week 10.

Task 1 - Use what you have learned to process the Landsat files provided, this time, you know you are interested in the
NVDI index which will use Bands 4 (red, aka vis) and 5 (near-infrared, aka nir) from the Landsat 8 imagery, see here for more
info about the bands: https://www.usgs.gov/faqs/what-are-band-designations-landsat-satellites. Data provided are monthly
(a couple are missing due to cloud coverage) during the year 2015 for the State of RI, and stored in the file Landsat_data_lfs.zip.

Before you start, here is a suggested workflow:

1) Extract the Landsat_data_lfs.zip file into a known location.
2) For each month provided, you want to calculate the NVDI, using the equation: nvdi = (nir - vis) / (nir + vis)
 https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index. Consider using the Raster Calculator Tool in ArcMap and using "Copy as Python Snippet" for the first calculation.

The only rule is, you should run your script once, and generate the NVDI for ALL MONTHS provided. As part of your code
submission, you should also provide a visualization document (e.g. an ArcMap layout in PDF format), showing the patterns for an area of RI that you find interesting.

'''


import arcpy
from arcpy.sa import *
import os
import glob

############################################# Change base directory here ###############################################
base_dir = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Coding_Challenge_10_pfy"
# NOTE SET BASE DIR TO WHERE THE DATA FOLDER IS

arcpy.env.overwriteOutput = True
arcpy.env.workspace = base_dir

########################################################################################################################


############################ Make a list of the directory with the month folders #######################################
data_folder = "Landsat_data_lfs"
month_list = os.listdir(os.path.join(base_dir, data_folder))
print("List of the months with the landsat data from 2015:", month_list)

# Want bands 4 and 5 for nvdi calculation
desired_landsat_bands = ["B4", "B5"]
########################################################################################################################


########################################## Create and run functions ####################################################
def collect_band_paths(base_dir, data_folder, month_list, desired_landsat_bands):
    # Initialize an empty dictionary to store the file names categorized by month
    month_band_files = {}

    # Loop through each month
    for month in month_list:
        # Initialize an empty list to hold file names for current month's processing
        process_band_list = []

        # Loop through each desired band
        for band in desired_landsat_bands:
            # Construct the pattern for glob to find all relevant .tif files
            pattern = os.path.join(base_dir, data_folder, month, f"*_{band}.tif")
            # Find all files that match this pattern
            band_files = glob.glob(pattern)
            # Retrieve only the file names, not the full paths
            file_names = [os.path.basename(file) for file in band_files]
            # Extend the temporary list with the found file names
            process_band_list.extend(file_names)

        # Store the list of file names in the dictionary under the month key
        month_band_files[month] = process_band_list

    return month_band_files

# Run function
month_band_files = collect_band_paths(base_dir, data_folder, month_list, desired_landsat_bands)
print(month_band_files)

def nvdi_calc(month_band_files, base_dir, data_folder):
    nvdi_output_folder = os.path.join(base_dir, "nvdi_outputs")
    if not os.path.exists(nvdi_output_folder):
        os.makedirs(nvdi_output_folder)

    arcpy.env.workspace = base_dir  # setting the workspace

    for month, file_list in month_band_files.items():
        try:
            print("\n",month, file_list)
            new_dir = os.path.join(base_dir, data_folder, month)
            arcpy.env.workspace = new_dir  # change the working directory for each month

            # Assuming file_list[0] is vis and file_list[1] is nir, this needs to be adjusted based on actual file ordering
            vis = Raster(file_list[0])
            nir = Raster(file_list[1])
            nvdi_expression = (nir - vis) / (nir + vis + 1e-10)

            nvdi_out_raster = nvdi_expression  # Directly using the expression as the result
            nvdi_out_raster.save(os.path.join(nvdi_output_folder, f"{month}_ndvi.tif"))

            if os.path.exists(os.path.join(nvdi_output_folder, f"{month}_ndvi.tif")):
                print(f"Processed {month} and saved to {nvdi_output_folder}")
            else:
                print(f"Error processing {month}")
        except Exception as e:
            print(f"Failed to process {month} due to: {str(e)}")

nvdi_calc(month_band_files, base_dir, data_folder)
########################################################################################################################