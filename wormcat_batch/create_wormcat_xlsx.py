"""
Create the summary Excel file based on the individual Wormcat runs
"""
import pandas as pd


def create_category_summary(data, category_name):
    """
    Utility function create_category_summary
    """
    category = data[category_name].value_counts()
    category = pd.DataFrame(
        {category_name: category.index, 'Count': category.values})
    category = category.sort_values(by=[category_name])
    return category


def process_category_file_row(row, sheet):
    """
    Utility function process_category_file_row
    """
    file_name = row['file']
    label_category = f"Category {row['category']}"
    label_pvalue = f"{row['label']}_PValue"
    label_rgs = f"{row['label']}_RGS"

    cat_results = pd.read_csv(file_name)
    cat_results.rename(columns={'Category': label_category,
                       'RGS': label_rgs, 'PValue': label_pvalue}, inplace=True)
    cat_results.drop('Unnamed: 0', axis=1, inplace=True)
    cat_results.drop('AC', axis=1, inplace=True)

    sheet = pd.merge(sheet, cat_results, on=label_category, how='outer')
    sheet[label_pvalue] = sheet[label_pvalue].apply(significant)
    sheet[label_rgs] = sheet[label_rgs].apply(lambda x: x if x > 0 else 0)
    return sheet


def significant(value):
    """
    Utility function to return abreviations for significat values
    NV = Not a Value
    NS = Not Significant
    """
    ret_val = 'NV'
    if value < 0.05:
        ret_val = value
    elif value >= 0.05:
        ret_val = 'NS'
    return ret_val


def create_legend(writer, values, excel_formats):
    """
    Creates a simple sheet page as a Legend
    """
    data = {'Color Code <=': values[::-1]}
    legend_sheet = pd.DataFrame(data)

    legend_sheet.to_excel(writer, sheet_name='Legend', index=False)
    worksheet = writer.sheets['Legend']
    num_rows, num_columns = legend_sheet.shape
    sheet_range = f"A1:{chr(num_columns + 64)}{num_rows+1}"

    worksheet.conditional_format(sheet_range, {
                                 'type': 'cell', 'criteria': '=', 'value': 0, 'format': excel_formats[0]})
    for index, value in enumerate(values):
        worksheet.conditional_format(sheet_range, {
                                     'type': 'cell', 'criteria': '<=', 'value': value, 'format': excel_formats[index+1]})

    worksheet.autofit()


def process_category_files(files_to_process, annotation_file, out_data_xlsx):
    """
    Processes each category file and create the corasponding Excel summary sheet
    """
    data = pd.read_csv(annotation_file)
    #writer = pd.ExcelWriter("{}".format(out_data_xlsx), engine='openpyxl')
    writer = pd.ExcelWriter(f"{out_data_xlsx}", engine='xlsxwriter')

    sheets = files_to_process['sheet'].unique()
    values = [0.0000000001, 0.00000001, 0.000001, 0.0001, 0.05]
    formats = [{'bg_color': 'white', 'font_color': 'black', 'num_format': '0'},
               {'bg_color': '#244162', 'font_color': 'white',
                   'num_format': '0.000E+00'},
               {'bg_color': '#355f91', 'font_color': 'white',
                   'num_format': '0.000E+00'},
               {'bg_color': '#95b3d7', 'font_color': 'black',
                   'num_format': '0.000E+00'},
               {'bg_color': '#b8cce4', 'font_color': 'black',
                   'num_format': '0.000E+00'},
               {'bg_color': '#f4f2fe', 'font_color': 'black',
                   'num_format': '0.000E+00'}
               ]
    excel_formats = [writer.book.add_format(f) for f in formats]

    create_legend(writer, values, excel_formats)

    for sheet_label in sheets:
        cat_files = files_to_process[files_to_process['sheet'] == sheet_label]
        label_category = f"Category {cat_files['category'].iloc[0]}"
        category_sheet = create_category_summary(data, label_category)
        for index, row in cat_files.iterrows():
            category_sheet = process_category_file_row(row, category_sheet)

        category_sheet.to_excel(writer, sheet_name=sheet_label, index=False)
        worksheet = writer.sheets[sheet_label]
        num_rows, num_columns = category_sheet.shape
        sheet_range = f"B1:{chr(num_columns + 64)}{num_rows+1}"
        # print(f"{range=}")

        worksheet.conditional_format(sheet_range, {
                                     'type': 'cell', 'criteria': '=', 'value': 0, 'format': excel_formats[0]})
        for index, value in enumerate(values):
            worksheet.conditional_format(sheet_range, {
                                         'type': 'cell', 'criteria': '<=', 'value': value, 'format': excel_formats[index+1]})

        worksheet.autofit()

    writer.close()
