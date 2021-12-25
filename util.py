""" general utility module """
import csv
import json
import os
import pathlib
import re
from typing import List, Dict

import aiohttp
import pandas as pd


def write_new_word_csv(data_frame: pd.DataFrame, csv_file: str) -> bool:
    """
    DataFrame write to csv and old csv backup

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
        except OSError as error:
            print(error)
            return False

    if file_path_csv.exists():
        try:
            os.rename(csv_file, old_file)
        except OSError as error:
            print(error)
            return False
    try:
        data_frame.to_csv(csv_file)
        return True
    except pd.io.common.EmptyDataError as error:
        print(error)
        return False


def write_word_csv_to_json(json_file: str, word_dict: Dict) -> bool:
    """dict object write to json file

    Args:
        json_file (str): json file path
        word_dict (dict): dict object

    Returns:
        bool: if has error return False
    """

    try:
        with open(json_file, 'w', encoding="utf-8") as filep:
            json.dump(word_dict, filep, ensure_ascii=False, indent=4)
            return True
    except IOError as error:
        print(error)
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
        with open(csv_file, mode='a', newline="", encoding="utf-8") as filep:
            writer = csv.writer(filep, lineterminator='\n')
            writer.writerow(new_strings)
        return True
    except IOError as error:
        print(error)
        return False


def get_files(target_dir_name: str, pattern='*') -> List:
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


async def download_file(url: str, file_name: str, allowed_content: Dict) -> bool:
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
            async with session.get(url) as resp:
                if resp.status == 200:
                    file_data = await resp.content.read()
                    file_type = resp.headers['Content-Type']
                else:
                    print(download_error_message)
                    return False
            if file_type not in allowed_content:
                print(invalid_file_message)
                return False
            else:
                with open(file_name, 'wb') as filep:
                    filep.write(file_data)
                return True
    except aiohttp.InvalidURL as error:
        print(invalid_url_message, error)
        print(download_error_message)
        return False
    except IOError as error:
        print(error)
        print(download_error_message)
        return False

