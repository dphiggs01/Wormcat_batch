# Wormcat Batch

### Overview
*Wormcat Batch* is a command line tool that allows you to batch multiple runs of Wormcat from a Microsoft Excel File.

### Prerequisites

*Wormcat Batch* requires that a fully functioning 'R' Wormcat package is installed and Python 3.6

If you are unsure if you have Wormcat installed you can run `is_wormcat_installed.R`
This simple script can be found in the `Code` directory and will return the location
of the wormcat R installation if it is installed.

If *Wormcat* is not install you can follow the directions [here](https://github.com/dphiggs01/Wormcat/blob/master/README.md)
to install Wormcat. Note: Wormcat can be installed as an R package you do NOT need to checkout the
source unless you intend to modify Wormcat. The readme file explains how to install Wormcat as an R package.


### Excel spreadsheet Naming Conventions

Once you have the R package installed you will create an Excel Spreadsheet with the
required data for batch execution.

See the file `Example/Murphy_TS.xsl` for details.

Note:

* Th Spreadsheet Name should ONLY be composed of Letters, Numbers and Underscores (_)
and has an extension .xlsx, .xlt, .xls
* The Sheet Names within the spreadsheet should ONLY be composed of Letters, Numbers and Underscores (_)
other characters may cause the batch process to fail!
* Each sheet requires a column name "gene ID" (This column name is case sensitive)

### To Run the Batch Process

To run the batch process open a terminal window, change directory to the
location of the Wormcat_batch.

Execute: `python ./runwormcat_batch.py`


<img src="./Images/Example_Run.png"  height="283" width="700"/>


### Sample Output

<img src="./Images/Sample_Output.png"  height="405" width="800"/>




