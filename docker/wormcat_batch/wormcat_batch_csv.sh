#!/bin/bash

# Note: Place this script in the executable PATH and ensure Docker is installed and running

# This script simplifies the execution of WormCat Batch by allowing user to provide a single path to the CSV files. 
# the script automatically determines the output directory based on that path.

if [ "$#"=="1" ]; then
   full_path=$(realpath "$1")
	mount_dir=$(dirname "$full_path")
 	input_csv_dir=$(basename "$full_path")
else
   echo "Usage: wormcat_batch.sh <full-path-to-csv-directory>"
   exit 1
fi


if [ ! -d "$mount_dir" ]; then
    echo "The mount directory does not exists: $mount_dir"
    exit 1
fi

if [ ! -d "${mount_dir}/${input_csv_dir}" ]; then
    echo "The input_csv directory does exists: $input_csv_dir"
    exit 1
fi


output_dir="wormcat_out"

echo "Running wormcat_batch at ${mount_dir} and cvs path ${input_csv_dir}"
docker run --rm -v ${mount_dir}:/usr/data danhumassmed/wormcat_batch:1.0.1 wormcat_cli \
      --input-csv-path /usr/data/${input_csv_dir} \
      --output-path /usr/data/${output_dir} \
      --clean-temp False
echo "The results can be found here:  ${mount_dir}/${output_dir}"

