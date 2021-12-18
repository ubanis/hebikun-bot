import aiohttp
import os
import re
import json
import pandas as pd
import csv
import pathlib
from typing import List


def write_new_word_csv(df, csv_file):
    """DataFrame write to csv and old csv backup

    Args:
        df (pandas DataFrame): pandas data frame
        csv_file (str): csv file path

    Returns:
        bool: command result
    """

    old_file = csv_file + '.old'
    file_path_csv = pathlib.Path(csv_file)
    file_path_old = pathlib.Path(old_file)

    if file_path_old.exists():
        try:
            os.remove(old_file)
        except OSError as e:
            print(e)
            return False

    if file_path_csv.exists():
        try:
            os.rename(csv_file, old_file)
        except OSError as e:
            print(e)
            return False
    try:
        df.to_csv(csv_file)
        return True
    except pd.io.common.EmptyDataError as e:
        print(e)
        return False


def write_word_csv_to_json(json_file, word_dict):
    """dict object write to json file

    Args:
        json_file (str): json file path
        word_dict (dict): dict object

    Returns:
        bool: if has error return False
    """

    try:
        with open(json_file, 'w') as f:
            json.dump(word_dict, f, ensure_ascii=False, indent=4)
            return True
    except IOError as e:
        print(e)
        return False


def write_word_csv(new_strings: List[str], csv_file: str) -> bool:
    """write one line to csv file

    Args:
        new_strings (str): new one line data
        csv_file (str): csv file path

    Returns:
        bool: if has error return False
    """

    try:
        with open(csv_file, mode='a', newline="") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(new_strings)
        return True
    except IOError as e:
        print(e)
        return False


def get_files(target_dir_name, pattern='*'):
    """get a match files target directory with pattern

    Args:
        target_dir_name (str): target directory path
        pattern (str, optional): Defaults to '*'. matching string

    Returns:
        list: list of file names
    """

    files = [f for f in os.listdir(
        target_dir_name) if re.search(pattern, f, re.IGNORECASE)]
    return files


async def download_file(url, file_name, allowed_content):
    """download file from the web

    Args:
        url ([str]): [image file url]
        file_name ([str]): [download file file_path]
        allowed_content([dict]): [allowd file type]

    Returns:
        [bool]: if has error return False
    """
    invalid_file_message = 'ERROR: Download file is invalid file'
    invalid_url_message = 'ERROR: invalid url ->'
    download_error_message = 'ERROR: Download error'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    download_file = await r.content.read()
                    file_type = r.headers['Content-Type']
                else:
                    print(download_error_message)
                    return False
            if file_type not in allowed_content:
                print(invalid_file_message)
                return False
            else:
                with open(file_name, 'wb') as f:
                    f.write(download_file)
                return True
    except aiohttp.InvalidURL as e:
        print(invalid_url_message, e)
        print(download_error_message)
        return False
    except IOError as e:
        print(e)
        print(download_error_message)
        return False
