import os
import sys
import pickle
import numpy as np 
import pandas as pd
import sqlite3

from src.exception import CustomException
from src.logger import logging

def save_object(file_path, obj):
    try:
        logging.info("File process..")
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("File saved successfully.")
    except Exception as e:
        raise CustomException(e, sys)
    
def sqli_connect(db_name):
    try:
        conn = sqlite3.connect(db_name+'.db')
        logging.info("Connected to database successfully")
        return conn
    except Exception as e:
        raise CustomException(e,sys)    

# if __name__ == "__main__":
#     sqli_connect('database')     