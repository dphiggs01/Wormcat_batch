# Sofware Provided by this container

| Docker Tag | WormCat     | WormCat Batch|
|------------|-------------|--------------|
| 1.0.1      | version 2.0 | v1.1.6       |

## About: WormCat Batch

[http://www.wormcat.com/](http://www.wormcat.com/)

**WormCat** is an R program for annotating and visualizing gene set enrichment data from C. elegans microarray, RNA seq or RNAi screen data.

**WormCat Batch** enables the batching of multiple calls to WormCat on your Desktop, Laptop, or HPC.

**WormCat** output provides:
* Scaled bubble charts with enrichment scores that meet a Bonferroni false discovery rate cut-off of 0.01 as SGV files (`rgs_fisher_cat1_apv.svg`). 
* The download directory also includes CSV files on the data used for the graph (e.g., `rgs_fisher_cat1_apv.csv`) (Note: "apv" stand for appropriate p-value). 
* The output also includes CSV files with categories that have at least one returned gene and p-value from Fisher's exact test (`rgs_fisher_cat1.csv`), 
* And the `rgs_and_category.csv` file returns the input gene list joined with the annotations providing descriptions for each gene in the list.

**WormCat Batch** provides two additional outputs:
1. An Excel summary of all WormCat runs `<YOUR INPUT NAME>.xlsx`
2. An interactive visualization of the annotated genes `sunburst.html`

<br>

---

**Note:** You do NOT need to download and install any software to run WormCat as it is available for use at [wormcat.com](http://wormcat.com). 

The reasons you may desire to execute your own instance of WormCat with Docker:

1. You desire to integrate WormCat into a Bioinformatics pipeline.
2. You have *many* gene sets to run against, and you do not want to manually run them through the WormCat website.
3. You would like to provide your own Annotation file or modify one of the provided Annotation files.
4. You want to experiment with RStudio with WormCat pre-installed and Execute arbitrary RScripts.

<br>

**Note:**  How to cite this work, [see the citation section](#citation).

<br>

<img src="https://www.umassmed.edu/contentassets/4edf0cb3ed5245c2883e9bd514462c72/wormcat-graphic-for-web-768x436.jpg" alt="Alt Text">

<br>
<br>

# Usage

The provided Docker image is compatible with [Singularity](https://sylabs.io/docs/) and is actively used in [NextFlow](https://www.nextflow.io/) Pipelines configured for an HPC.

<br>

#### There are three primary ways that **WormCat Batch** is Run

1. With an Excel file as Input
2. With a directory path to CSV files with Worm Base or Sequence Ids as Input
3. With either of the above as Input and a Path to an externally prepared Annotation file

#### Additionally 
4. WormCat batch can also be run as an R / RStudio container enabling the execution of arbitrary RScripts


### Local Execution

<br>

**1. Execution with an Excel file as Input**

You can download an Example Microsoft Excel file [Murphy_TS.xlsx](http://www.wormcat.com/static/download/Murphy_TS.xlsx) to confirm the required format. 

**Note:** _When creating your Excel, please follow the naming conventions to avoid processing errors._

**Excel file Naming Conventions:**
1. The Spreadsheet Name should **ONLY** be composed of Letters, Numbers, and Underscores (_) and has an extension .xlsx, .xlt, .xls
2. The individual Sheet Names (i.e., Tab names) within the spreadsheet should **ONLY** be composed of Letters, Numbers, and Underscores (_).
3. Each Sheet requires a column header which **MUST** be 'Sequence ID' or 'Wormbase ID' (The column header is case sensitive.)

* __<full_path_to_excel>__ path on the local machine that contains the Excel file to process.

<br>

```bash
docker run --rm -v <full_path_to_excel>:/usr/data danhumassmed/wormcat_batch:1.0.1 wormcat_cli --input-excel /usr/data/Murphy_TS.xlsx --output-path /usr/data/wormcat_out
```

<br>
<br>

**2. Execution with a directory path to CSV file with Worm Base or Sequence Ids as Input**

You can download an Example Directory of CSV files [Murphy_TS_csv.zip](https://github.com/dphiggs01/Wormcat_batch/raw/master/docker/wormcat_batch/Murphy_TS_csv.zip) to confirm the required format. 

* `unzip Murphy_TS_csv.zip`
* __<full_path_to_csv>__ path on the local machine that contains the extracted CSV directory.

<br>

```bash
docker run --rm -v <full_path_to_csv>:/usr/data danhumassmed/wormcat_batch:1.0.1 wormcat_cli --input-csv-path /usr/data/Murphy_TS_csv --output-path /usr/data/wormcat_out
```

<br>
<br>

**3. Execution with either of the above as Input and a Path to an externally prepared Annotation file**

You can download an Example Annotation file [whole_genome_v2_nov-11-2021.csv](http://www.wormcat.com/static/download/whole_genome_v2_nov-11-2021.csv) to confirm the required format. 

* __<full_path_to_excel>__ path on the local machine that contains the Excel and annotation file to process.

<br>

```bash
docker run --rm -v <full_path_to_excel>:/usr/data danhumassmed/wormcat_batch:1.0.1 wormcat_cli --input-excel /usr/data/Murphy_TS.xlsx --annotation-file /usr/data/whole_genome_v2_nov-11-2021.csv --output-path /usr/data/wormcat_out
```

<br>
<br>

**4. WormCat batch can also be run as an R / RStudio container enabling the execution of arbitrary RScripts**

Once the docker container is executed, full access to the Linux machine and RStudio is available at [http:/127.0.0.1:8787](http:/127.0.0.1:8787)

<br>

| Login    | Credentials |
|----------|-------------|
| User:    | rstudio     |
| Passord: | password    |

<br>

* __<full_path_to_output_dir>__ path on the local machine to place outputs from R / RStrudio execution.

<br>


```bash
docker run --rm -p 8787:8787 -e PASSWORD=password -v <full_path_to_output_dir>:/home/rstudio/projects danhumassmed/wormcat_batch:1.0.1
```

<br>
<br>

**Additional Options**

* See `cli_wormcat --help` for a complete list of avaiable commandline options
* See `cli_wormcat --version` to check the current version of WormCat batch

<br>

```bash
docker run --rm danhumassmed/wormcat_batch:1.0.1 wormcat_cli --help
docker run --rm danhumassmed/wormcat_batch:1.0.1 wormcat_cli --version
```

<br>

* Execute R Commands
* This command returns the available (internal) Annotation files that WormCat can use for establishing enrichment.
* **Note:** *Add a mount point and execute any RScript*

```bash
docker run --rm danhumassmed/wormcat_batch:1.0.1 R -q -e "library('wormcat');get_available_annotation_files()"
```
<br>
<br>

**Convenience Script for execution with CSV files**

1. You can download the script [wormcat_batch_csv.sh](https://github.com/dphiggs01/Wormcat_batch/raw/master/docker/wormcat_batch/wormcat_batch_csv.sh) to simplify the execution of wormcat batch with CSV files. 
2. After download, change permission on the file to make it executable `$chmod +x wormcat_batch_csv.sh`

```bash
#!/bin/bash

# Note: Place this script in the executable PATH and ensure Docker is installed and running

# This script simplifies the execution of WormCat Batch by allowing the user to provide a single path to the CSV files. 
# The script automatically determines the output directory based on that path.

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
```

Example usage

Note: Replace _DIR_W_CSV_FILES_ with actual directory

```bash
wormcat_batch_csv.sh ./DIR_W_CSV_FILES
```

# <a name="citation"></a>Citation

#### If you use WormCat in a published work please cite:

> **WormCat**: an online tool for annotation and visualization of Caenorhabditis elegans genome-scale data
>
> Amy D Holdorf, Daniel P Higgins, Anne C. Hart, Peter R Boag, Gregory Pazour, Albertha J. M. Walhout, Amy Karol Walker
>
> [GENETICS February 1, 2020 vol. 214 no. 2 279-294;](https://academic.oup.com/genetics/article/214/2/279/5930455?login=false)



