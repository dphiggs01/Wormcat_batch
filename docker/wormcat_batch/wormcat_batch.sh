#!/bin/bash

# Simplify the execution of WormCat Batch by accepting a path to the CSV files and deriving the output directory from the path

if [ "$#"=="1" ]; then
	mount_dir=$(dirname "$1")
   if [ "$mount_dir"=="." ]; then
      mount_dir=$(readlink -f $mount_dir )
   fi
	input_csv_dir=$(basename "$1")
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

