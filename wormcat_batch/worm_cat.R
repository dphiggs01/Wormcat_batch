#!/usr/bin/env Rscript

suppressPackageStartupMessages(library("wormcat"))
suppressPackageStartupMessages(library("argparse"))

# create parser object
parser <- ArgumentParser()

parser$add_argument("-f", "--file", help = "File to be processed")

parser$add_argument("-t", "--title", default = "rgs", help = "Title for the graph")

parser$add_argument("-o", "--out_dir", default = "./worm_cat_output", help = "The output directory")

parser$add_argument("-a", "--annotation_file", default="physiology_nov-24-2018.csv", help="Provide the Annotation file {'straight_mmm-DD-YYYY.csv', 'physiology_mmm-DD-YYYY.csv'} [default]")

parser$add_argument("-i", "--input_type", default="Sequence ID", help = "Provide the Input type {'Sequence.ID', 'Wormbase.ID'} [default]")

parser$add_argument("-r", "--rm_dir", default=TRUE, help="Remove temp directory [default]")

parser$add_argument("-z", "--zip_files", default=TRUE, help="Create a zip file of the results directory [default]")

args <- parser$parse_args()

if (is.null(args$file)) {
  stop("At least one argument must be supplied (input file).n", call.= FALSE)
}

# con <- file("worm_cat_fun.log") # nolint
# sink(con, append = TRUE) # nolint
# sink(con, append = TRUE, type = "message") # nolint


#print(paste("worm_cat_fun", args$file, args$title, args$out_dir, args$rm_dir, args$annotation_file, args$input_type, args$zip_files)) # nolint

if (toupper(args$rm_dir) == "TRUE") {
    rm_dir <- TRUE
} else {
    rm_dir <- FALSE
}

if (toupper(args$zip_files) == "TRUE") {
    zip_files <- TRUE
} else {
    zip_files <- FALSE
}

worm_cat_fun(
    file_to_process = args$file,
    title = args$title,
    output_dir = args$out_dir,
    rm_dir = rm_dir,
    annotation_file = args$annotation_file,
    input_type = args$input_type,
    zip_files = zip_files
)
