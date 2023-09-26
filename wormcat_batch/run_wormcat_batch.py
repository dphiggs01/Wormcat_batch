"""
Module provides functionality for running Wormcat in batch mode at the command linr
"""
import os
import sys
import argparse
import shutil
import zipfile
import importlib.metadata
from datetime import datetime
import warnings
import pandas as pd
from wormcat_batch.execute_r import ExecuteR
from wormcat_batch.create_wormcat_xlsx import process_category_files
from wormcat_batch.create_sunburst import create_sunburst

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
warnings.simplefilter(action='ignore', category=FutureWarning)


def extract_csv_files(input_excel_nm, csv_file_path):
    """
    Create CSV Files from the given Excel spreadsheet
    """
    try:
        input_excel = pd.ExcelFile(input_excel_nm)
    except ValueError:
        print(f"ERROR: File Name [{input_excel_nm}[] is Not a Valid Excel File.")
        sys.exit(-1)
    
    for sheet in input_excel.sheet_names:
        sheet_df = input_excel.parse(sheet)
        sheet_df.to_csv(
            f'{csv_file_path}{os.path.sep}{sheet}.csv', index=False)


def process_csv_files(csv_file_path, wormcat_out_path, annotation_file):
    """
    Read the csv data files and process each individually through Wormcat
    """
    for dir_content in os.listdir(csv_file_path):
        if dir_content.endswith(".csv"):
            content_full_path = os.path.join(csv_file_path, dir_content)
            if os.path.isfile(content_full_path):
                header_line = None
                first_line = None
                with open(content_full_path, 'r', encoding='utf-8') as file:
                    header_line = file.readline().strip()
                    first_line = file.readline().strip()

                # This is a hack to check for Wormbase IDs if we see a Wormbase.ID in the first line ignoring the header
                if 'WBGene' in first_line[:16]:
                    header_line = "Wormbase.ID"
                wormcat_input_type = header_line.replace(' ', '.')
                csv_file_nm = os.path.basename(content_full_path)
                file_nm_wo_ext = csv_file_nm[:-4]  # Remove .csv from file name
                title = file_nm_wo_ext.replace('_', ' ')
                wormcat_output_dir = f'{wormcat_out_path}{os.path.sep}{file_nm_wo_ext}'
                execute_r = ExecuteR()
                execute_r.worm_cat_fun(
                    content_full_path, wormcat_output_dir, title, annotation_file, wormcat_input_type)
                create_sunburst(wormcat_output_dir)
    return wormcat_out_path


def create_summary_spreadsheet(wormcat_out_path, annotation_file, out_xsl_file_nm):
    """
    After all the sheets on the Excel have been executed or CSV files processed 
    create a dataframe that can be used to summarize the results.
    This dataframe is used to create the output Excel.
    """
    process_lst = []
    for dir_nm in os.listdir(wormcat_out_path):
        if os.path.isdir(os.path.join(wormcat_out_path, dir_nm)):
            for cat_num in [1, 2, 3]:
                rgs_fisher = f"{wormcat_out_path}{os.path.sep}{dir_nm}{os.path.sep}rgs_fisher_cat{cat_num}.csv"
                cat_nm = f"Cat{cat_num}"
                row = {'sheet': cat_nm, 'category': cat_num,
                    'file': rgs_fisher, 'label': dir_nm}
                process_lst.append(row)

    df_process = pd.DataFrame(process_lst, columns=[
                              'sheet', 'category', 'file', 'label'])
    process_category_files(df_process, annotation_file, out_xsl_file_nm)

# Wormcat Utility functions


def get_wormcat_lib():
    """
    Find the location where the R Wormcat program is installed
    """
    execute_r = ExecuteR()
    path = execute_r.wormcat_library_path_fun()
    if path:
        first_quote = path.find('"')
        last_quote = path.rfind('"')
        if last_quote == -1:
            print("Wormcat is not installed or cannot be found.")
            exit(-1)
        path = path[first_quote+1:last_quote]
    # print(f"wormcat_lib_path={path}")
    return path


def get_category_files(path):
    """
    Get the list of available annotation files for Wormcat.
    These files exist in the R wormcat install under the "extdata" directory
    and end with .csv
    """
    category_files = []
    path = f"{path}{os.path.sep}extdata"
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(".csv"):
                category_files.append(filename)

    return category_files

# Utility functions


def create_directory(directory, with_backup=False):
    """
    Utility function to create a directory and backup the original if it exists and has content
    And the content was put there by a previous run of the program
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    created_by_flag = '.created_by_wormcat_batch'

    if with_backup and os.path.exists(directory) and os.listdir(directory):
        created_by_flag_check = os.path.join(directory, created_by_flag)
        if os.path.exists(created_by_flag_check):
            print(f"Creating backup of existing directory [{directory}]")
            # Create backup directory name with a unique timestamp suffix
            backup_dir = f"{directory}_{timestamp}.bk"
            shutil.move(directory, backup_dir)
        else:
            print("ERROR")
            print(f"Directory {directory} is not Empty and was not created by a prior run of this program.")
            print("Change the output directory to an empty or non exsisting directory.")
            sys.exit(-1)

    try:
        os.makedirs(directory, exist_ok=True)
        if with_backup:
            created_by_flag_check = os.path.join(directory, created_by_flag)
            with open(created_by_flag_check, 'w', encoding='utf-8') as file:
                file.write(timestamp)
    except OSError as err:
        print(f"ERROR: Cannot create directory\n{err}")
        sys.exit(-1)



def zip_directory(directory_path, zip_file_name):
    """
    Compress the content of a directory in zip format.
    """
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(
                    file_path, directory_path))


def is_valid_directory_name(directory_name):
    """
    Check if the directory name string is a valid name
    """
    ret_val = True
    if not isinstance(directory_name, str):
        ret_val = False

    # Check if the directory name is empty or contains only whitespace
    if not directory_name.strip():
        ret_val = False

    # Check if the directory name contains any invalid characters
    invalid_characters = '\'?%*|"<>'
    if any(char in invalid_characters for char in directory_name):
        ret_val = False

    return ret_val

class WormcatArgumentParser(argparse.ArgumentParser):
    """
    Add annotation file descriptions to help text
    """
    def print_help(self, file=None):
        wormcat_path = get_wormcat_lib()
        annotation_files = get_category_files(wormcat_path)
        annotation_file_names = ""
        for index, annotation_file in enumerate(sorted(annotation_files)):
            annotation_file_names += f"\t{index+1} {annotation_file}\n"

        super().print_help(file)
        print(f"\nannotation-files:\n{annotation_file_names}")

def print_error_and_quit(parser, error_msg):
    """
    Print command line ERROR message and quit
    """
    parser.print_usage()
    print(f"ERROR: {error_msg}")
    sys.exit(-1)

def process_command_arguments():
    """
    The process_command_arguments method validates and sets the input arguments 
    to conform with downstream processing
    """
    parser = WormcatArgumentParser()
    parser.add_argument('-i', '--input-excel',
                        help='Input file in Excel/Wormcat format')
    parser.add_argument('-c', '--input-csv-path',
                        help='Input path to a collection of CSV files in Wormcat format')
    parser.add_argument('-o', '--output-path', help='Output path')
    parser.add_argument('-a', '--annotation-file', default='whole_genome_v2_nov-11-2021.csv',
                        help='Annotation file name or path default=whole_genome_v2_nov-11-2021.csv')
    parser.add_argument('-t', '--clean-temp', default='True',
                        help='Remove files created while processing default=True')

    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s v{importlib.metadata.version("wormcat_batch")}')
    args = parser.parse_args()

    if not args.input_excel and not args.input_csv_path:
        print_error_and_quit(parser, "An Excel Input file or a path to CSV files is required.")

    if args.input_excel and args.input_csv_path:
        print_error_and_quit(parser, "--input-excel [-i] and  --input-csv-path [-c] can not be used at the same time.")
    
    if args.input_excel and not os.path.isfile(args.input_excel):
        print_error_and_quit(parser, f""" An Excel Input file not found.
        [{args.input_excel}] is not a valid file name for wormcat batch.""")
      
    if args.input_csv_path and not os.path.isdir(args.input_csv_path):
        print_error_and_quit(parser, f""" A CSV Directory was not found.
        [{args.input_csv_path}] is not a valid directory name for wormcat batch.""")

    if not args.output_path or not is_valid_directory_name(args.output_path):
        print_error_and_quit(parser, f""" An Output path is required with a valid name.
        [{args.output_path}] is not valid directory path for wormcat batch.""")

    # if args.annotation_file is not a path to an annotation file
    # vaildate the input name and set the full path
    if not os.path.sep in args.annotation_file:
        wormcat_path = get_wormcat_lib()
        annotation_files = get_category_files(wormcat_path)
        
        if not args.annotation_file or not args.annotation_file in annotation_files:
            print_error_and_quit(parser, "Missing or incorrect annotation-file-nm. See --help for details.")
            
        args.annotation_file = f"{wormcat_path}{os.path.sep}extdata{os.path.sep}{args.annotation_file}"

    elif args.annotation_file and os.path.sep in args.annotation_file:
        if not os.path.isfile(args.annotation_file):
            print_error_and_quit(parser, f"""Local Annotation file not found.
            [{args.annotation_file}] is not a valid file name for wormcat batch.""")

    # Support TRUE or True as input to clean temp
    # otherwise set to False
    if args.clean_temp.lower().title() == 'True':
        args.clean_temp = True
    else:
        args.clean_temp = False

    print(f"\tInput Excel     = {args.input_excel}")
    print(f"\tInput CSV Path  = {args.input_csv_path}")
    print(f"\tOutput Path     = {args.output_path}")
    print(f"\tAnnotation File = {args.annotation_file}")
    print(f"\tClean Temp      = {args.clean_temp}")
    print("\n")


    return args


def main():
    """
    Main control execution of Wormcat Batch
    """
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
    output_base_dir = f"{input_data_nm}_{timestamp}"
    wormcat_out_path = f"{args.output_path}{os.path.sep}{output_base_dir}"
    create_directory(wormcat_out_path)

    # Call Wormcat on each CSV file
    process_csv_files(csv_file_path, wormcat_out_path, args.annotation_file)

    # Create a summary spreadsheet of all CSV runs
    out_xsl_file_nm = f"{wormcat_out_path}{os.path.sep}Out_{input_data_nm}.xlsx"
    create_summary_spreadsheet(
        wormcat_out_path, args.annotation_file, out_xsl_file_nm)

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
