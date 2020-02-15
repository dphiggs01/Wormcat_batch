# Wormcat Batch

### Overview
*Wormcat Batch* is a command line tool that allows you to batch multiple
runs of Wormcat from a Microsoft Excel File.


### Prerequisites

*Wormcat Batch* requires Python 3.5+ and R 3.4.1+ with a Wormcat
package installed.

If you are unsure if you have Wormcat installed you can run
`find.package("wormcat")` from an R command prompt.

If *Wormcat* is not install you can follow the directions
[here](https://github.com/dphiggs01/Wormcat/blob/master/README.md)
to install Wormcat. Note: Wormcat can be installed as an R package you
do NOT need to checkout the source unless you intend to modify Wormcat.
The readme file explains how to install Wormcat as an R package.


### Excel spreadsheet Naming Conventions

Once you have the R package installed you will create an Excel
Spreadsheet with the required data for batch execution.

See the file `Example/Murphy_TS.xsl` for details.

<img src="./Images/Sample_Input.png"  height="405" width="500"/>

Note:

* The Spreadsheet Name should ONLY be composed of Letters, Numbers and
Underscores (_) and has an extension .xlsx, .xlt, .xls
* The Sheet Names within the spreadsheet should ONLY be composed of
Letters, Numbers and Underscores (_) other characters may cause the
batch process to fail!
* Each sheet requires a column name "gene ID" (This column name is case sensitive)

### To Run the Batch Process

To run the batch process open a terminal window, change directory to your
project directory.

```
$pip install wormcat_batch
$wormcat_cli
```

<img src="./Images/Example_Run.png"  height="288" width="800"/>


After execution the Output Directory will contain all the Wormcat run data and a
summary Excel spreadsheet.



### Sample Output

<img src="./Images/Sample_Output.png"  height="415" width="800"/>




