# WormCat Batch

### Overview
*WormCat Batch* is a command line tool that allows you to batch multiple
runs of [WormCat](http://wormcat.com) from a Microsoft Excel File or a directory path with WormCat formatted csv files.

**Note:** You can also run WormCat Batch as a docker container. Find more information on running WormCat Batch as a Docker container [here](https://hub.docker.com/r/danhumassmed/wormcat_batch).

### Prerequisites

*WormCat Batch* requires Python 3.5+ and R 3.4.1+ with a WormCat
package installed.

If you are unsure if you have WormCat installed, you can run
`find.package("wormcat")` from an R command prompt.

If *WormCat* is not installed, you can follow the directions
[here](https://github.com/dphiggs01/Wormcat/blob/master/README.md)
to install WormCat. 

**Note:** WormCat can be installed as an R package you;
do NOT need to checkout the source unless you intend to modify WormCat.
The readme file explains how to install WormCat as an R package.


### Excel spreadsheet Naming Conventions

Once you have the R package installed, you will create an Excel
Spreadsheet with the required data for batch execution.

See the file `Example/Murphy_TS.xsl` for details on formating the Excel.

<img src="https://raw.githubusercontent.com/dphiggs01/Wormcat_batch/master/Images/Sample_Input.png"  height="405" width="500"/>

**Note:**

* The Spreadsheet Name should ONLY be composed of Letters, Numbers and
Underscores (_) and has an extension .xlsx, .xlt, .xls
* The Sheet Names within the spreadsheet should ONLY be composed of
Letters, Numbers, and Underscores (_) other characters may cause the
batch process to fail!
* Each sheet requires a column name 'Sequence ID' or 'Wormbase ID'
(This column name is case-sensitive)

### To Run the Batch Process

To run the batch process, open a terminal window, change the directory to your
project directory.

```
$pip install wormcat_batch
$wormcat_cli --help
```

<img src="https://raw.githubusercontent.com/dphiggs01/Wormcat_batch/master/Images/Example_Run.png"  height="288" width="800"/>


After execution, the Output Directory will contain all the WormCat run data and a
summary Excel spreadsheet.



### Sample Output


<img src="https://raw.githubusercontent.com/dphiggs01/Wormcat_batch/master/Images/Sample_Output.png"  height="415" width="800"/>

### Local development /test hints

#### Setup to test
* conda activate <appropriate_env>
* pip install .

#### Test
* cd /Users/dan/delme #some working directory
* wormcat_cli --input-excel ${PROJ_HOME}/Example/Murphy_TS.xlsx --output-path ./output  
* wormcat_cli --input-csv-path ${PROJ_HOME}/Example/Murphy_TS_CSV--output-path ./output 

#### Deploy
* Advance the version number in setup.py
* `conda deactivate # twine is installed in base env`
* `increment setup.py version`
* `cd <project directory>`
* `rm -rf ./dist`
* `rm -rf ./wormcat_batch.egg-info`
* `python setup.py sdist`
* `twine check dist/*`
* `twine upload --repository pypi dist/*`
* `git add .`
* `git commit -m "some comment"`
* `git push`




