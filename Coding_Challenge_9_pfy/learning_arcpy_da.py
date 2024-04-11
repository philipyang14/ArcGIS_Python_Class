"""
Philip Yang
NRS 528
Coding Challenge 9

In this coding challenge, your objective is to utilize the arcpy.da module to undertake some
basic partitioning of your dataset. In this coding challenge, I want you to work with the Forest Health Works dataset from
[RI GIS](https://www.rigis.org/datasets/ri-forest-health-works-project-points-all-invasives?geometry=-73.625%2C41.322%2C-69.307%2C42.040)
(I have provided this as a downloadable ZIP file in this repository).

Using the arcpy.da module (yes, there are other ways and better tools to do this),
I want you to extract all sites that have a photo of the invasive species (Field: PHOTO) into a new Shapefile,
and do some basic counts of the dataset. In summary, please addressing the following:

1) Count how many individual records have photos, and how many do not (2 numbers), print the results.

2) Count how many unique species there are in the dataset, print the result.

3) Generate two shapefiles, one with photos and the other without.
"""

import arcpy, os

################################################## EDIT BASE DIR HERE: #################################################
base_dir = r"C:\Users\Philip Yang\OneDrive - University of Rhode Island\NRS_528\ArcGIS_Python_Class\Coding_Challenge_9_pfy"

arcpy.env.workspace = base_dir
arcpy.env.overwriteOutput = True
########################################################################################################################


########################################################################################################################
input_shp = os.path.join(base_dir, "RI_Forest_Health_Works_Project_Points_All_Invasives\RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp")

fields = ['photo', 'Species', 'Site', 'FID']

expression_photo = arcpy.AddFieldDelimiters(input_shp, "photo") + " = 'y'"
expression_NOphoto = arcpy.AddFieldDelimiters(input_shp, "photo") + "<> 'y'"
########################################################################################################################


########################################################################################################################
# 1)
count_photo = 0
with arcpy.da.SearchCursor(input_shp, fields, expression_photo) as cursor:
    for row in cursor:
        # print(u'Photo = {0}, Site = {1}, Species = {2}, ID = {3}'.format(row[0], row[2], row[1], row[3]))
        count_photo = count_photo + 1
print(f"\n #1:\nNumber of samples with photos: {count_photo}")

count_NOphoto = 0
with arcpy.da.SearchCursor(input_shp, fields, expression_NOphoto) as cursor:
    for row in cursor:
        # print(u'Photo = {0}, Site = {1}, Species = {2}, ID = {3}'.format(row[0], row[2], row[1], row[3]))
        count_NOphoto = count_NOphoto + 1
print(f"Number of samples with NO photos: {count_NOphoto}")

# Turned above into a function
# def search_shapefile_and_count(input_shp, fields, expression, count):
#     with arcpy.da.SearchCursor(input_shp, fields, expression) as cursor:
#         for row in cursor:
#             # print(u'Photo = {0}, Site = {1}, Species = {2}, ID = {3}'.format(row[0], row[2], row[1], row[3]))
#             count = count + 1
#     print(f"\n Number of samples for {expression} is: {count}")
#
# count_photo = 0
# search_shapefile_and_count(input_shp, fields, expression_photo, count_photo)
# count_NOphoto = 0
# search_shapefile_and_count(input_shp, fields, expression_NOphoto, count_NOphoto)
########################################################################################################################


########################################################################################################################
# 2)
species_numbers = []
with arcpy.da.SearchCursor(input_shp, fields) as cursor:
    for row in cursor:
        if row[1] not in species_numbers:
            species_numbers.append(row[1])

print("\n #2: \nThe number of different species names is = " + str(len(species_numbers)))

species_count={}

for species in species_numbers:
    with arcpy.da.SearchCursor(input_shp, fields) as cursor:
        for row in cursor:
            if species == row[1]:
                if species not in species_count.keys():
                    species_count[species] = 1  # also: if not i in d
                elif species in species_count.keys():
                    species_count[species] = species_count[species] + 1

print(f"The amount of samples for each species is: \n", species_count)
########################################################################################################################


########################################################################################################################
# 3)
# Use this tool: https://pro.arcgis.com/en/pro-app/latest/tool-reference/conversion/feature-class-to-feature-class.htm

def split_feature_class(input_shp, outLocation, expression, outName):
    # Set local variables
    inFeatures = input_shp
    outLocation = outLocation
    outFeatureClass = outName
    expression = expression
    print("\n #3:\nRunning Split Feature Class")
    # Run FeatureClassToFeatureClass
    arcpy.conversion.FeatureClassToFeatureClass(inFeatures, outLocation,
                                                outFeatureClass, expression)
    print(f"Feature class for {expression} created in: \n", outLocation)


outName_photos = "PHOTOS_RI_Forest_Health_All_Invasives.shp"
split_feature_class(input_shp, base_dir, expression_photo, outName_photos)

outName_NO_photos ="NO_PHOTOS_RI_Forest_Health_All_Invasives.shp"
split_feature_class(input_shp, base_dir, expression_NOphoto, outName_NO_photos)
########################################################################################################################