import os
import sys
import argparse
import pandas as pd
import shutil
import zipfile
import json
from datetime import datetime
from wormcat_batch.execute_r import ExecuteR
from wormcat_batch.create_wormcat_xlsx import process_category_files

import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
warnings.simplefilter(action='ignore', category=FutureWarning)

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
    print(f"wormcat_lib_path={path}")
    return path

def get_category_files(path):
    '''
    get the list of available annotation files for Wormcat.
    These files exist in the R wormcat install under the "extdata" directory
    '''
    category_files=[]
    index=1
    path = "{}{}extdata".format(path, os.path.sep)
    for root, dirs, files in os.walk(path):
        for filename in files:
            category_files.append(filename)
            index +=1

    return category_files, path

def call_wormcat(name, gene_ids, output_dir, annotation_file, input_type):
    '''
    Call the R Wormcat program.
    The input "gene_ids" is provided as a csv file.
    The output of the Wormcat R program is a directory containing the results and a zip of the directory.
    The clean-up process moves the results output to an aggregation directory and deletes the input csv and the zip file.
    '''
    # input_type = 'Wormbase.ID'
    file_nm = f"{name}.csv"
    dir_nm = f"{name}"
    title = dir_nm.replace('_', ' ')

    gene_ids = gene_ids.to_frame(name=input_type)
    # gene_ids.to_csv(file_nm, encoding='utf-8', index=False)
    gene_ids.to_csv(file_nm, index=False)

    executeR = ExecuteR()
    executeR.worm_cat_fun(file_nm, dir_nm, title, annotation_file, input_type)

    # Clean up
    mv_dir = file_nm.replace(".csv", "")
    os.rename(mv_dir, f"{output_dir}{os.path.sep}{mv_dir}")
    if os.path.exists(file_nm):
        os.remove(file_nm)
    if os.path.exists(f"{dir_nm}.zip"):
        os.remove(f"{dir_nm}.zip")
    

def process_spreadsheet(xsl_file_nm, output_dir, annotation_file):
    '''
    Read the Excel file and process each sheet individually through Wormcat
    '''
    xl = pd.ExcelFile(xsl_file_nm)
    for sheet in xl.sheet_names:
        print(f"Processing sheet {sheet}")
        df = xl.parse(sheet)
        if 'Wormbase ID' in df.columns:
            gene_id_all = df['Wormbase ID']
            input_type = 'Wormbase.ID'
        elif 'Sequence ID' in df.columns:
            gene_id_all = df['Sequence ID']
            input_type = 'Sequence.ID'
        else:
            print("ERROR: You must provide column names with either 'Sequence ID' or 'Wormbase ID")
            exit(-1)

        call_wormcat(sheet, gene_id_all, output_dir, annotation_file, input_type)

def files_to_process(output_dir):
    '''
    After all the sheet on the Excel have been executed create a dataframe that can be used to summarize the results
    this dataframe is used to create the output Excel
    '''
    df_process = pd.DataFrame(columns=['sheet', 'category', 'file','label'])
    for dir_nm in os.listdir(output_dir):
        for cat_num in [1,2,3]:
            rgs_fisher = f"{output_dir}{os.path.sep}{dir_nm}{os.path.sep}rgs_fisher_cat{cat_num}.csv"
            cat_nm = f"Cat{cat_num}"
            row = {'sheet': cat_nm, 'category': cat_num, 'file': rgs_fisher,'label': dir_nm}
            df_process = df_process.append(row, ignore_index=True)
    return df_process

##########################################################
## Utility functions

def move_file_to_output_directory(file_path, output_directory,copy=False):
    '''
    Utility function to move or copy a file to a different directory
    '''
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(output_directory, file_name)
    if copy:
        shutil.copy(file_path, destination_path)
    else:
        shutil.move(file_path, destination_path)



def create_directory_with_backup(directory):
    '''
    Utility function to create a directory and backuo the original if it exists
    '''
    if os.path.exists(directory):
        print(f"directory Exists [{directory}]")
        # Create backup directory name with a unique timestamp suffix
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = f"{directory}_{timestamp}.bk"
        # Create a backup of the existing directory
        shutil.copytree(directory, backup_dir)

    # Create a new empty directory
    os.makedirs(directory, exist_ok=True)

def zip_directory(directory_path, zip_name):
    '''
    Utility function to recursivley compress a directory and it subdirectories
    '''
    parent_dir = os.path.dirname(directory_path)
    zip_path = os.path.join(parent_dir, zip_name)
    os.rename(directory_path, zip_path)

    output_path = zip_path.rstrip(os.sep) + '.zip'  # Output zip file path
    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(zip_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, zip_path)  # Get relative path
                zipf.write(file_path, arcname=rel_path)
    return output_path

##########################################################

def main():
    print("Wormcat Batch")
    parser = argparse.ArgumentParser()
    help_statement="wormcat_cli --input-excel <full_path_to_excel> --output-path <full_path_to_out_dir> --backup-output-path True --annotation-file-nm 'whole_genome_v2_nov-11-2021.csv' "
    parser.add_argument('-i', '--input-excel', help='Inputfile in Excel format')
    parser.add_argument('-o', '--output-path', help='Output path')
    parser.add_argument('-b', '--backup-output-path', default=True, help='Backup or create outpath path if it does not exists')
    parser.add_argument('-a', '--annotation-file-nm', default='whole_genome_v2_nov-11-2021.csv', help='Annotation file name')

    with open('setup.json', 'r') as file:
            data = json.load(file)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s v{data["version"]}')
    args = parser.parse_args()

    if not args.input_excel:
        print(help_statement)
        print("Inputfile in Excel format is missing.")
        return

    if not args.output_path:
        print(help_statement)
        print("Output path is missing")
        return

    wormcat_path = get_wormcat_lib()
    annotation_files, path = get_category_files(wormcat_path)

    if not args.annotation_file_nm or not args.annotation_file_nm in annotation_files:
        print(help_statement)
        print("Missing or incorrect annotation-file-nm.")
        print("Available names: {}".format(annotation_files))
        return
 
    # Rest of your program logic goes here
    print("Input Excel:", args.input_excel)
    print("Output Path:", args.output_path)
    print("Backup Path:", args.backup_output_path)
    print("Annotation File Nm:", args.annotation_file_nm)
    
    # Add output to a temp_output director
    temp_output_path= f".{os.path.sep}temp_output"
    create_directory_with_backup(temp_output_path)

    process_spreadsheet(args.input_excel, temp_output_path, args.annotation_file_nm)
    base_input_excel = os.path.basename(args.input_excel)
    input_excel_no_ext = os.path.splitext(base_input_excel)[0]

    out_xsl_file_nm=f"{temp_output_path}{os.path.sep}Out_{base_input_excel}"

    annotation_file =f"{path}{os.path.sep}{args.annotation_file_nm}"
    df_process = files_to_process(temp_output_path)
    process_category_files(df_process, annotation_file, out_xsl_file_nm)
    move_file_to_output_directory(args.input_excel, temp_output_path,copy=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_dir_nm = f"{input_excel_no_ext}_{timestamp}"
    output_zip = zip_directory(temp_output_path, zip_dir_nm)
    move_file_to_output_directory(output_zip, args.output_path)

if __name__ == '__main__':
    main()