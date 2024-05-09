import os
import glob

def read_data_folder(data_folder):
    """
    Read the data folder and return the documents path.

    Parameters:
        data_folder (str): The path to the data folder.

    Returns:
        str: The path to the documents.
    """
    documents = glob.glob(os.path.join(data_folder, "*"))
    return documents
