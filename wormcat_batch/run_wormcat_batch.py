import os
import pandas as pd
from wormcat_batch.execute_r import ExecuteR
from wormcat_batch.create_wormcat_xlsx import process_category_files

def get_wormcat_lib():
    executeR = ExecuteR()
    path = executeR.wormcat_library_path_fun()
    if path:
        first_quote=path.find('"')
        last_quote=path.rfind('"')
        if last_quote == -1:
            print("Wormcat is not installed or cannot be found.")
            exit(-1)
        path = path[first_quote+1:last_quote]

    return path

def get_category_files(path):
    category_files=[]
    index=1
    path = "{}{}extdata".format(path,os.path.sep)
    for root, dirs, files in os.walk(path):
        for filename in files:
            category_files.append(filename)
            print("[{}]  {}".format(index, filename))
            index +=1

    i = int(input("Select File Name: "))
    category_file = category_files[i-1]
    return category_file, path

def get_output_dir():
    done = False
    output_dir = ""
    while not done:
        output_dir = input("Please provide an Empty Output Directory (or enter to quit): ")
        if output_dir == "":
            exit()
        exists = os.path.exists(output_dir)
        if exists:
            if not os.listdir(output_dir):
                done = True
            else:
                print("Directory is not empty.")
        else:
            print("Directory does NOT exists.")
            y_n = input("Would you like to create this directory? (y/n): ").lower().strip()
            if y_n[:1] == "y":
                try:
                    # Create target Directory
                    os.mkdir(output_dir)
                    done = True
                except FileExistsError:
                    print("Failed to make directory ", output_dir, "!")
            else:
                print("No Directory Provided.")
    return output_dir

def get_spreadsheet_to_process():
    done = False
    speadsheet = ""
    while not done:
        speadsheet = input("Please provide the Full path to input spreadsheet (or enter to quit): ")
        if speadsheet == "":
            exit()
        exists = os.path.isfile(speadsheet)
        if exists:
            if speadsheet[-3:] in ['lsx','xlt','xls']:
                done = True
            else:
                print("Expected Excel file extension")
        else:
            print("Spreadsheet file does NOT exists.")
    return speadsheet

# Call Wormcat once for each sheet (tab) in the spreadsheet
def call_wormcat(name, gene_ids, output_dir, annotation_file):

    input_type = 'Wormbase.ID'
    file_nm = "{}.csv".format(name)
    dir_nm = "{}".format(name)
    title = dir_nm.replace('_', ' ')

    gene_ids = gene_ids.to_frame(name=input_type)
    gene_ids.to_csv(file_nm, encoding='utf-8', index=False)

    executeR = ExecuteR()
    executeR.worm_cat_fun(file_nm, dir_nm, title, annotation_file, input_type)

    # Clean up
    mv_dir = file_nm.replace(".csv", "")
    os.rename(mv_dir, "{}{}{}".format(output_dir,os.path.sep, mv_dir))
    os.remove(file_nm)
    os.remove("{}.zip".format(dir_nm))


# Process the Input spreadsheet
def process_spreadsheet(xsl_file_nm, output_dir, annotation_file):
    xl = pd.ExcelFile(xsl_file_nm)

    for sheet in xl.sheet_names:
        print(sheet)
        df = xl.parse(sheet)
        gene_id_all = df['gene ID']
        call_wormcat(sheet, gene_id_all, output_dir, annotation_file)


def files_to_process(output_dir):
    df_process = pd.DataFrame(columns=['sheet', 'category', 'file','label'])
    for dir_nm in os.listdir(output_dir):
        for cat_num in [1,2,3]:
            rgs_fisher = "{}{}{}{}rgs_fisher_cat{}.csv".format(output_dir,os.path.sep,dir_nm,os.path.sep,cat_num)
            cat_nm = "Cat{}".format(cat_num)
            row = {'sheet': cat_nm, 'category': cat_num, 'file': rgs_fisher,'label': dir_nm}
            df_process = df_process.append(row, ignore_index=True)
    return df_process

def main():
    print("Wormcat Batch")
    wormcat_path = get_wormcat_lib()
    annotation_file, path = get_category_files(wormcat_path)
    output_dir = get_output_dir()
    xsl_file_nm = get_spreadsheet_to_process()
    process_spreadsheet(xsl_file_nm, output_dir, annotation_file)
    start=xsl_file_nm.rfind(os.path.sep)
    out_xsl_file_nm="{}{}Out_{}".format(output_dir,os.path.sep,xsl_file_nm[start+1:])
    annotation_file ="{}{}{}".format(path,os.path.sep,annotation_file)
    df_process = files_to_process(output_dir)
    process_category_files(df_process,annotation_file,out_xsl_file_nm)

if __name__ == '__main__':
    main()