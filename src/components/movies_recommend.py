import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object
from dataclasses import dataclass
import json
import bs4 as bs
import urllib.request
import pickle
import os
import sys

class Movies_session:
    def __init__(self):
        logging.info('Data Ingestion methods Starts')
        try:
            self.df=pd.read_csv(os.path.join('data/processed_data','main_data.csv'))
            logging.info('Dataset read as pandas Dataframe')

            filename = os.path.join('data','nlp_model.pkl')
            self.clf_model = pickle.load(open(filename, 'rb'))

            self.vectorizer = pickle.load(open(os.path.join('data','tranform.pkl'),'rb'))
            logging.info('Ingestion of Data is completed')
              
        except Exception as e:
            logging.info('Exception occured at Data Ingestion stage')
            raise CustomException(e,sys)

    def convert_to_list(self,my_list):
        try:
            logging.info('String Coversion of list started')
            my_list = my_list.split('","')
            my_list[0] = my_list[0].replace('["','')
            my_list[-1] = my_list[-1].replace('"]','')
            logging.info('string convert_to_list run successfully')
            return my_list      
        except Exception as e:
            logging.info('error occur in conversion to list (string) function')
            raise CustomException(e,sys)

    def convert_to_list_num(self,my_list):
        try:
            logging.info('Number Coversion of list started')
            my_list = my_list.split(',')
            my_list[0] = my_list[0].replace("[","")
            my_list[-1] = my_list[-1].replace("]","")
            logging.info('number convert_to_list run successfully')
            return my_list
        except Exception as e:
            logging.info('error occur in conversion to list (number) function')
            raise CustomException(e,sys)
        
    def get_suggestions(self):
        try:
            logging.info('suggestion started')
            data = self.df
            return list(data['movie_title'].str.capitalize())
        except Exception as e:
            logging.info('error occur in get_suggestion function')
            raise CustomException(e,sys)

# if __name__ == "__main__":
#     obj = Movies_session()
#     print(obj.get_suggestions())