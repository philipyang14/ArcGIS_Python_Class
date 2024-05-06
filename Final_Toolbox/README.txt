# ArcGIS_Python_Class
NRS 528, Spring Semester 2024

This toolbox was created by Philip Yang for NRS 528 Spring 2024 course at the University of Rhode Island taught by Andrew Davies, PhD. 

In it, (Tool 1: ProcessCSV_ToShapefile) csv files (using four habitat location files as examples from Flower Garden Banks National Marine Sanctuary) are processed and cleaned to 
contain the correct data and concatenated and then converted to points using XYTabletoPoint tool. Then, (Tool 2: ExtractMultiRasterValues) the spatial analyst tool Extract Multi Values to Points tool is used to 
take the depth values from a raster (using a 50 m bathymetry grid for Flower Garden Banks) and appended to the attribute table as a new field in the points shapefile. Tools 3 (Habitat_DataCleaning) and 4 (DeleteFolder) 
deal with cleaning the point shapefile to only keep values within the mesophotic depth range and remove points that were not assigned values from the raster (-9999) and then delete temporary files created. 

The end output folder will have a (1) a clean csv file and (2) a clean point shapefile of habitat occurrences from photo analysis in Flower Garden Banks. This shapefile can now be used for spatial thinning and habitat
suitability models for mesophotic coralline algae and/or reefs. Running each tool separately avoids errors.