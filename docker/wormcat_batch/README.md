# Sofware Provided

| Docker Tag | Wormcat     | Wormcat Batch|
|------------|-------------|--------------|
| 1.0.1      | version 2.0 | v1.0.8       |

## Wormcat Batch


[http://www.wormcat.com/](http://www.wormcat.com/)


WormCat will provide enrichment data from the nested annotation list with broad categories in Category 1 (Cat1) and more specific categories in Cat2 and Cat3. For example, sbp-1 is in Metabolism: lipid: transcriptional regulator. WormCat output provides scaled bubble charts with enrichment scores that meet a Bonferroni false discovery rate cut off of 0.01 as SGV files. The download directory includes CSV files on the data used for the graph (e.g. rgs_fisher_cat1_apv.csv) (apv is appropriate p value). We also include CSV files with categories that have at least one returned gene and p value from Fisher’s exact test (rgs_fisher_cat1.csv). The rgs_and_category.csv file returns the input gene with annotations.

<br>

---

**Note:** You do NOT need to download and install any software to run Wormcat as it is available for use at [wormcat.com](http://wormcat.com). 

The reasons you may desire to execute your own instance of Wormcat with Docker.

1. You desire to intergrate Wormcat into a Bioinformatics pipeline.
2. You have *many, many* gene sets to run against and you do not want to manually run them through the website.
3. You would like to provide your own Annotation file or modify one of the provided Annotation files.
4. You want to experiment with RStudio with Wormcat pre-installed.

<br>

You can download an Example Microsoft Excel file [here](http://www.wormcat.com/static/download/Murphy_TS.xlsx) to confirm the required format. 

When creating your own Excell please take care to follow the naming conventions to avoid processing errors.

<br>

<img src="https://www.umassmed.edu/contentassets/4edf0cb3ed5245c2883e9bd514462c72/wormcat-graphic-for-web-768x436.jpg" alt="Alt Text">

<br>
<br>

<br>

# Usage

The provided Docker image is compatible with [Singularity](https://sylabs.io/docs/) and is actively used in [NextFlow](https://www.nextflow.io/) Pipelines configured for an HPC.

<br>

### Local Execution

To run Wormcat or Wormcat Batch locally prepare your Excel file and execute with the below command.

Substituting the following:
* __<full_path_to_excel>__ path on the local machine that contains the Excel file to process.
* __<my_wormcat>.xlsx__ the name of the Excel file you want to process.

<br>

```
docker run --rm -v <full_path_to_excel>:/usr/data danhumassmed/wormcat_batch:1.0.1 wormcat_cli --input_excel /usr/data/<my_wormcat>.xlsx --output-path /usr/data
```

```
docker run --rm -v <full_path_to_excel>:/usr/data danhumassmed/wormcat_batch:1.0.1 wormcat_cli --input_excel /usr/data/<my_wormcat>.xlsx --output-path /usr/data
```

<br>

The output will be a Zipfile containing the results of the run.