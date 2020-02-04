import sys
import pandas as pd


DEL_CHARS = " ".join([chr(i) for i in list(range(32)) + list(range(127, 256))])
TRANSFORM_TABLE = str.maketrans(DEL_CHARS, " " * len(DEL_CHARS))


# each excel sheet represents a table
def excel_to_csv(path: str, excel_sheets: list):
    xls = pd.ExcelFile(path)

    for sheet in xls.sheet_names:
        if sheet in excel_sheets:
            df = pd.read_excel(xls, sheet)
            u = df.select_dtypes(object)
            columns = u.columns
            for c in columns:
                df[c] = df[c].apply(lambda x: str(x).translate(TRANSFORM_TABLE))
            df.to_csv(sheet + ".csv", index=False)


if __name__ == "__main__":
    """
    argv[1] - excel file containing multiple sheets
    argv[2] - sheets to convert
    
    Example: python generate_csv.py file.xlsx Sheet1,Sheet2
    """
    excel_to_csv(sys.argv[1], list(sys.argv[2].split(',')))

