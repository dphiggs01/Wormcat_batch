# Sofware Provided

| Docker Tag | Wormcat     | Wormcat Batch|
|------------|-------------|--------------|
| 1.0.1      | version 2.0 | v1.0.8       |

## Wormcat Batch


[http://www.wormcat.com/](http://www.wormcat.com/)


Wormcat Batch enables the batching of multiple calls to Wormcat on your Desktop, Laptop, or HPC.

Wormcat is an R program that provides enrichment data from a nested annotation list with broad categories in Category 1 (Cat1) and more specific categories in Cat2 and Cat3. 

For example, sbp-1 is in Metabolism: lipid: transcriptional regulator. 

**Wormcat** output provides:
* scaled bubble charts with enrichment scores that meet a Bonferroni false discovery rate cut-off of 0.01 as SGV files (`rgs_fisher_cat1_apv.svg`). 
* The download directory also includes CSV files on the data used for the graph (e.g., `rgs_fisher_cat1_apv.csv`) (Note: "apv" stand for appropriate p-value). 
* The output also includes CSV files with categories that have at least one returned gene and p-value from Fisher's exact test (`rgs_fisher_cat1.csv`), 
* and the `rgs_and_category.csv` file returns the input gene list joined with the annotations providing descriptions for each gene in the list.

**Wormcat Batch** provides two additional outputs:
1. An Excel summary of all wormcat runs `<YOUR INPUT>.slsx`
2. An interactive visualization of the annotated genes `sunbustr.html`

<br>

---

**Note:** You do NOT need to download and install any software to run Wormcat as it is available for use at [wormcat.com](http://wormcat.com). 

The reasons you may desire to execute your own instance of Wormcat with Docker:

1. You desire to integrate Wormcat into a Bioinformatics pipeline.
2. You have *many* gene sets to run against, and you do not want to manually run them through the Wormcat website.
3. You would like to provide your own Annotation file or modify one of the provided Annotation files.
4. You want to experiment with RStudio with Wormcat pre-installed and Execute arbitrary RScripts.

<br>

<img src="https://www.umassmed.edu/contentassets/4edf0cb3ed5245c2883e9bd514462c72/wormcat-graphic-for-web-768x436.jpg" alt="Alt Text">

# Usage

The provided Docker image is compatible with [Singularity](https://sylabs.io/docs/) and is actively used in [NextFlow](https://www.nextflow.io/) Pipelines configured for an HPC.

<br>

#### There are three primary ways that Wormcat Batch is Run

1. With an Excel file as Input
2. With a directory path to CSV file with Worm Base or Sequence Ids as Input
3. With either of the above as Input and a Path to an externally prepared Annotation file

#### Additionally 
4. Wormcat batch can also be run as an R / RStudio container enabling the execution of arbitrary RScripts


### Local Execution

<br>

**1. With an Excel file as Input**

You can download an Example Microsoft Excel file [here](http://www.wormcat.com/static/download/Murphy_TS.xlsx) to confirm the required format. 

**Note:** _When creating your Excel, please follow the naming conventions to avoid processing errors._

* __<full_path_to_excel>__ path on the local machine that contains the Excel file to process.

```
docker run --rm -v <full_path_to_excel>:/usr/data danhumassmed/wormcat_batch:1.0.1 wormcat_cli --input-excel /usr/data/Murphy_TS.xlsx --output-path /usr/data/wormcat_out
```
<br>
<br>

**2. With a directory path to CSV file with Worm Base or Sequence Ids as Input**

You can download an Example Directory of CSV files [here](https://github.com/dphiggs01/Wormcat_batch/raw/master/docker/wormcat_batch/Murphy_TS_csv.zip) to confirm the required format. 

* __<full_path_to_csv>__ path on the local machine that contains the extracted CSV directory.

```
docker run --rm -v <full_path_to_csv>:/usr/data danhumassmed/wormcat_batch:1.0.1 wormcat_cli --input-csv-path /usr/data/Murphy_TS_csv --output-path /usr/data/wormcat_out
```

<br>
<br>

**3. With either of the above as Input and a Path to an externally prepared Annotation file**

You can download an Example Annotation file [here](http://www.wormcat.com/static/download/whole_genome_v2_nov-11-2021.csv) to confirm the required format. 

* __<full_path_to_excel>__ path on the local machine that contains the Excel and annotation file to process.

```
docker run --rm -v <full_path_to_excel>:/usr/data danhumassmed/wormcat_batch:1.0.1 wormcat_cli --input-excel /usr/data/Murphy_TS.xlsx --annotation-file /usr/data/whole_genome_v2_nov-11-2021.csv --output-path /usr/data/wormcat_out
```

<br>
<br>
**4. Wormcat batch can also be run as an R / RStudio container enabling the execution of arbitrary RScripts**

Once the docker container is executed, full access to the Linux machine and RStudio is available at [http:/127.0.0.1:8787](http:/127.0.0.1:8787)

<br>

| Login    | Credentials |
|----------|-------------|
| User:    | rstudio     |
| Passord: | password    |

<br>

* __<full_path_to_output_dir>__ path on the local machine to place outputs from R / RStrudio execution.

<br>


```
docker run --rm -p 8787:8787 -e PASSWORD=password -v <full_path_to_output_dir>:/home/rstudio/projects danhumassmed/wormcat_batch:1.0.1
```

<br>
<br>

**Additional Options**

* See the cli_wormcat --help for a complete list of options

```
docker run --rm danhumassmed/wormcat_batch:1.0.1 wormcat_cli --help
```

<br>

* Execute R Commands
* This command returns the available (internal) Annotation files that wormcat can run
* **Note:** *Add a mount point and execute any RScript*

```
docker run --rm danhumassmed/wormcat_batch:1.0.1 R -q -e "library('wormcat');get_available_annotation_files()"
```
