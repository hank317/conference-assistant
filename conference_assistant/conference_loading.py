import os
import pandas as pd
from docx import Document


def table_to_text(file_path:str, file_type:str) -> str:
    """Read file content, supporting Excel spreadsheets, CSV, TSV files, etc.

    Args:
        file_path (str): The path where the file exists.
        file_type (str): File extension.

    Returns:
        str: Conference information
    """
    if file_type in ['.xls', '.xlsx']:
        file = pd.read_excel(file_path)
    elif file_type == '.csv':
        file = pd.read_csv(file_path)
    else:
        file = pd.read_csv(file_path, sep='\t')
    text = ''
    # traverse every row
    for index, row in file.iterrows():
        # Traverse every column
        row_text = ''
        for column_name in file.columns:
            value = row[column_name]
            if value and type(value) == str:
                row_text += str(column_name) + '：' + str(value) + '；'
        if row_text:
            text += row_text + '\n'
    return text


def word_to_text(file_path:str) -> str:
    """Read the content of a Word file.

    Args:
        file_path (str): The path where the file exists.

    Returns:
        str: Conference information.
    """
    file = Document(file_path)
    full_text = []
    for paragraph in file.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)


def txt_to_text(file_path:str) -> str:
    """Read the content of a plain text file.

    Args:
        file_path (str): The path where the file exists.

    Returns:
        str: Conference information.
    """
    text = ''
    with open(file_path, 'r') as file:
        text = file.read()
    return text
            

def get_file(file_path:list[str]) -> str:
    """Read file content according to different file types, supporting Word documents, Excel spreadsheets, TXT plain text, CSV, and TSV, etc.

    Args:
        file_path (list[str]): The path where the file exists.

    Returns:
        str: Conference information.
    """
    if not file_path:
        return 'No conference information is avaliable'
    all_text = ''
    for path in file_path:
        # get file extension
        extension = os.path.splitext(path)[1]
        # determine file type based on extension
        if extension.lower() in ['.doc', '.docx']:
            all_text += word_to_text(path) + '\n'
        elif extension.lower() in ['.xls', '.xlsx', '.csv', '.tsv']:
            all_text += table_to_text(path, extension.lower()) + '\n'
        elif extension.lower() in ['.txt']:
            all_text += txt_to_text(path) + '\n'
    return all_text
    
    
    

    

