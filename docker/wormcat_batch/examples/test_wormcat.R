# This is a simple script to test the Wormcat functions
# 1. get_available_annotation_files()
# 2. worm_cat_fun()

library(wormcat)

# IMPORTANT Set working directory
##############################################
project_dir <- "/home/rstudio/examples"

print(sprintf("The Wormcat project directory is: %s", project_dir))
print("")
setwd(project_dir)

# Remove any objects in the Global Environment
rm(list = ls())

# Print the available Annotations files
annotation_files <- get_available_annotation_files()
print("Available Annotation files are:")
for (annotation_file in annotation_files) {
  print(sprintf(".  %s", annotation_file))
}

print("")

# Set Variables to call Wormcat
file_to_process <- "sams-1_up.csv"
title <- "sams-1 up"
output_dir <- "../projects/wormcat_out"
rm_dir <- FALSE
annotation_file <- "whole_genome_v2_nov-11-2021.csv"
input_type <- "Wormbase.ID"
zip_files <- FALSE

print("Input parameters to worm_cat_fun:")
print(sprintf(".  The file to process is %s", file_to_process))
print(sprintf(".  The report title prefix is %s", title))
print(sprintf(".  The output directory is %s", output_dir))
print(sprintf(".  The annotation file is %s", annotation_file))
print(sprintf(".  The input file contains %ss", input_type))
print("")

print("Output worm_cat_fun:")
# Call the Wormcat function
worm_cat_fun(file_to_process,
             title,
             output_dir,
             rm_dir,
             annotation_file,
             input_type,
             zip_files)


print("")
print("Test script complete!")
