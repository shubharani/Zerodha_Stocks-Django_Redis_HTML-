from django.shortcuts import render
from rest_framework.decorators import api_view
import json
from django.conf import settings
import redis
import csv
import requests
from datetime import datetime
from bs4 import BeautifulSoup
# from django.core.cache import cache

# Create your views here.

# def test_vue(request):
#     return render(request, 'vue_app/test.html',data)

# Connect to our Redis instance
r = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)


def home(request):
    data = get_stock_by_name("")
    return render(request, 'vue_app/test.html',{'data': data})

def get_stock_by_name(name):
        stock_gen = r.scan_iter('*name:{}*'.format(name.lower()))
        return get_stocks(stock_gen)

def get_stocks(iterator):
    stocks = []
    for item in iterator:
        stock = dict()
        stock_prop_values = r.hmget(item, columns)
        for ind, prop in enumerate(stock_prop_values):
            stock[columns[ind]] = prop.decode("utf-8")
        stocks.append(stock)
    return stocks

columns = ['code', 'name', 'open', 'high', 'low', 'close']

def create_stock(data):
    pipe = r.pipeline()
    # print("lkhkj",data['name'])
    primary_key = 'code:{}::name:{}'.format(data['code'], data['name'].lower())
    print("before",data)
    pipe.hmset(primary_key, data)
    # pipe.zadd('top_ten', {primary_key: data['code']})  # use data['turnover'] if needed
    pipe.execute()

# def get_top_ten():
#     top_ten = r.zrange('top_ten', 0, 9)
#     return get_stocks(top_ten)

FIELD_CSV_MAP = {
    'code': 'SC_CODE',
    'name': 'SC_NAME',
    'open': 'OPEN',
    'high': 'HIGH',
    'low': 'LOW',
    'close': 'CLOSE'
} 

BASE_URL = "https://www.bseindia.com/"
HOMEPAGE_PATH = "/markets/MarketInfo/BhavCopy.aspx"
DOWNLOAD_LINK_ELEMENT_ID = "ContentPlaceHolder1_btnhylZip"
def get_download_page(page_path):  # /markets/MarketInfo/BhavCopy.aspx
        response = requests.get(BASE_URL+page_path)
        page = response.content
        return page

def get_download_url(page):  # /download/BhavCopy/Equity/EQ250719_CSV.ZIP
    parsed_page = BeautifulSoup(page, 'html.parser')
    download_path = parsed_page.find(id=DOWNLOAD_LINK_ELEMENT_ID).get('href')
    return download_path

# @staticmethod
def get_zip(file_url):
    try:
        res = requests.get(file_url)
        zipped_file = ZipFile(BytesIO(res.content))
        return zipped_file
    except:  # TODO : Handle individual exceptions, create a decorator
        raise Exception("Some error in downloading processing zip file")

# @staticmethod
def extract_csv_from_zip(zipped_file):
    csv_filename = zipped_file.infolist()[0].filename
    op_file_name = zipped_file.extract(csv_filename)
    zipped_file.close()
    return op_file_name


def process_csv_to_db(csv_file):
    with open(csv_file) as stocks:
        csv_reader = csv.reader(stocks, delimiter=",")
        field_index = dict()
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                for field in FIELD_CSV_MAP.keys():
                    field_index[field] = row.index(FIELD_CSV_MAP[field])
            else:
                data = dict()
                for field, index in field_index.items():
                    field_value = row[index]
                    if isinstance(field_value, str):
                        field_value = field_value.strip()
                    data[field] = field_value
                # print(data)
                create_stock(data)
            line_count += 1

home_page = get_download_page(HOMEPAGE_PATH)
zip_dload_url = get_download_url(home_page)
zipfile_obj = get_zip(zip_dload_url)
extracted_csv_filename = extract_csv_from_zip(zipfile_obj)
process_csv_to_db(extracted_csv_filename)