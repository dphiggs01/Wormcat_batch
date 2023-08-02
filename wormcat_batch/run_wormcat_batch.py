import os
import sys
import argparse
import pandas as pd
import shutil
import zipfile
import importlib.metadata
from datetime import datetime
from wormcat_batch.execute_r import ExecuteR
from wormcat_batch.create_wormcat_xlsx import process_category_files
from wormcat_batch.create_sunburst import create_sunburst

import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
warnings.simplefilter(action='ignore', category=FutureWarning)

def extract_csv_files(input_excel_nm, csv_file_path):
    '''
    Create CSV Files from the given Excel spreadsheet
    '''
    input_excel = pd.ExcelFile(input_excel_nm)
    for sheet in input_excel.sheet_names:
        sheet_df = input_excel.parse(sheet)
        sheet_df.to_csv(f'{csv_file_path}{os.path.sep}{sheet}.csv', index=False)

        
def process_csv_files(csv_file_path, wormcat_out_path, annotation_file):
    '''
    Read the csv data files and process each individually through Wormcat
    '''
    for dir_content in os.listdir(csv_file_path):
        conetnt_full_path = os.path.join(csv_file_path, dir_content)
        if os.path.isfile(conetnt_full_path):
            with open(conetnt_full_path, 'r') as file:
                header_line = file.readline().strip()
            wormcat_input_type = header_line.replace(' ', '.')
            csv_file_nm = os.path.basename(conetnt_full_path)
            file_nm_wo_ext = csv_file_nm[:-4] # Remove .csv from file name
            title = file_nm_wo_ext.replace('_', ' ')
            wormcat_output_dir = f'{wormcat_out_path}{os.path.sep}{file_nm_wo_ext}'
            executeR = ExecuteR()
            executeR.worm_cat_fun(conetnt_full_path, wormcat_output_dir, title, annotation_file, wormcat_input_type)
            create_sunburst(wormcat_output_dir)
    return wormcat_out_path

def create_summary_spreadsheet(wormcat_out_path, annotation_file, out_xsl_file_nm):
    '''
    After all the sheets on the Excel have been executed or CSV files processed 
    create a dataframe that can be used to summarize the results.
    This dataframe is used to create the output Excel.
    '''
    process_lst = []
    for dir_nm in os.listdir(wormcat_out_path):
        for cat_num in [1,2,3]:
            rgs_fisher = f"{wormcat_out_path}{os.path.sep}{dir_nm}{os.path.sep}rgs_fisher_cat{cat_num}.csv"
            cat_nm = f"Cat{cat_num}"
            row = {'sheet': cat_nm, 'category': cat_num, 'file': rgs_fisher,'label': dir_nm}
            process_lst.append(row)

    df_process = pd.DataFrame(process_lst, columns=['sheet', 'category', 'file','label'])
    process_category_files(df_process, annotation_file, out_xsl_file_nm)

## Wormcat Utility functions

def get_wormcat_lib():
    '''
    Find the location where the R Wormcat program is installed
    '''
    executeR = ExecuteR()
    path = executeR.wormcat_library_path_fun()
    if path:
        first_quote=path.find('"')
        last_quote=path.rfind('"')
        if last_quote == -1:
            print("Wormcat is not installed or cannot be found.")
            exit(-1)
        path = path[first_quote+1:last_quote]
    # print(f"wormcat_lib_path={path}")
    return path

def get_category_files(path):
    '''
    Get the list of available annotation files for Wormcat.
    These files exist in the R wormcat install under the "extdata" directory
    '''
    category_files=[]
    index=1
    path = "{}{}extdata".format(path, os.path.sep)
    for root, dirs, files in os.walk(path):
        for filename in files:
            category_files.append(filename)
            index +=1

    return category_files

## Utility functions

def create_directory(directory, with_backup=False):
    '''
    Utility function to create a directory and backup the original if it exists and has content
    '''
    if with_backup and os.path.exists(directory) and os.listdir(directory):
        print(f"Creating backup of existing directory [{directory}]")
        # Create backup directory name with a unique timestamp suffix
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = f"{directory}_{timestamp}.bk"
        shutil.move(directory, backup_dir)

    os.makedirs(directory, exist_ok=True)

def zip_directory(directory_path, zip_file_name):
    '''
    Compress the content of a directory in zip format.
    '''
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory_path))

## main application functions 

def process_command_arguments():
    '''
    The process_command_arguments method validates and sets the input arguments 
    to conform with downstream processing
    '''
    parser = argparse.ArgumentParser()
    help_statement="wormcat_cli --input-excel <path_to_excel> | --input-csv-path <path_to_csv> --output-path <path_to_out_dir> --annotation-file 'whole_genome_v2_nov-11-2021.csv' --clean-temp False"
    parser.add_argument('-i', '--input-excel', help='Input file in Excel/Wormcat format')
    parser.add_argument('-c', '--input-csv-path', help='Input path to a collection of CSV files in Wormcat format')
    parser.add_argument('-o', '--output-path', help='Output path')
    parser.add_argument('-a', '--annotation-file', default='whole_genome_v2_nov-11-2021.csv', help='Annotation file name or path default=whole_genome_v2_nov-11-2021.csv')
    parser.add_argument('-t', '--clean-temp', default='True', help='Remove files created while processing default=False')

    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s v{importlib.metadata.version("wormcat_batch")}')
    args = parser.parse_args()

    if not args.input_excel and not args.input_csv_path:
        print(help_statement)
        print("An Excel Input file or a path to CSV files is required.")
        sys.exit(-1)

    if not args.output_path:
        print(help_statement)
        print("An Output path is required.")
        sys.exit(-1)

    # if args.annotation_file is not a path to an annotation file
    # vaildate the input name and set the full path
    if not (os.path.sep in args.annotation_file):
        wormcat_path = get_wormcat_lib()
        annotation_files = get_category_files(wormcat_path)
         
        if not args.annotation_file or not args.annotation_file in annotation_files:
            print(help_statement)
            print("Missing or incorrect annotation-file-nm.")
            print("Available names: {}".format(annotation_files))
            sys.exit(-1)
        args.annotation_file = f"{wormcat_path}{os.path.sep}extdata{os.path.sep}{args.annotation_file}"
    
    # Support TRUE or True as input to clean temp
    # otherwise set to False
    if args.clean_temp.lower().title() == 'True':
        args.clean_temp = True
    else:
        args.clean_temp = False

    return args


def main():
    print("Starting Wormcat Batch")

    # Validate the command line arguments
    args = process_command_arguments()

    # Create the output directory if it does not exsist.
    # If it does exist and has content create a backup.
    create_directory(args.output_path, with_backup=True)

    # If we are given an input_csv_path use it.
    if args.input_csv_path:
        csv_file_path = args.input_csv_path
    else:
        # Else we MUST have been given an input_excel
        # Create a directory and extract the Excel sheets as csv data
        csv_file_path = f"{args.output_path}{os.path.sep}csv_files"
        create_directory(csv_file_path)
        extract_csv_files(args.input_excel, csv_file_path)

    # Create a directory based on the Excel file name or CSV directory and a timestamp
    # Wormcat processing will write to this directory
    if args.input_excel:
        base_input_excel = os.path.basename(args.input_excel)
        input_data_nm = os.path.splitext(base_input_excel)[0]
    else:
        input_data_nm = os.path.basename(args.input_csv_path)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_base_dir =f"{input_data_nm}_{timestamp}"
    wormcat_out_path = f"{args.output_path}{os.path.sep}{output_base_dir}"
    create_directory(wormcat_out_path)

    print(f"{args.input_excel=}")
    print(f"{args.input_csv_path=}")
    print(f"{args.output_path=}")
    print(f"{args.annotation_file=}")
    print(f"{args.clean_temp=}")

    # Call Wormcat on each CSV file
    process_csv_files(csv_file_path, wormcat_out_path, args.annotation_file)

    # Create a summary spreadsheet of all CSV runs
    out_xsl_file_nm = f"{wormcat_out_path}{os.path.sep}Out_{input_data_nm}.xlsx"
    create_summary_spreadsheet(wormcat_out_path, args.annotation_file, out_xsl_file_nm)
    
    # Zip the results
    zip_dir_nm = f"{args.output_path}{os.path.sep}{output_base_dir}.zip"
    zip_directory(wormcat_out_path, zip_dir_nm)
    
    # If set Remove files created while processing
    if args.clean_temp:
        shutil.rmtree(wormcat_out_path)
        if args.input_excel:
            shutil.rmtree(csv_file_path)


if __name__ == '__main__':
    main()