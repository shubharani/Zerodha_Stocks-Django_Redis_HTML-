from django.shortcuts import render
from rest_framework.decorators import api_view
import json
from django.conf import settings
import redis
import csv
import requests
from datetime import datetime
# from django.core.cache import cache

# Create your views here.

# def test_vue(request):
#     return render(request, 'vue_app/test.html',data)

# Connect to our Redis instance
r = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)


def home(request):
    # response = requests.get('http://freegeoip.net/json/')
    #  data = {
    #     'articles': "articles1",
    #     'authors': "authors1",
    # }
    # data = data.json()
    # saveToRedis()
    data = get_stock_by_name("")
    return render(request, 'vue_app/test.html',{'data': data})


def saveToRedis():
    r.flushall()
    # csv_values = csv.DictReader(open(getBhavCopy(), 'r'))
    # csv_values = csv.DictReader(open("file.csv", 'r'))
    # for row in csv_values:
    #     r.hmset(row['SC_NAME'].rstrip(), dict(row))
    # r.set('scrape_date',str(datetime.today().date().day))

def get_stock_by_name(name):
    results = []
    # if r.get('scrape_date') != str(datetime.today().date().day):
    #     saveToRedis()
    if name == '':
        results = "DATA NOT FOUND"
        return results
    for equity in r.scan_iter(match='*'+str(name).upper()+'*'):
        results.append(r.hgetall(equity))
    return results

# def get_stock_all():
#     # if r.get('scrape_date') != str(datetime.today().date().day):
#     #     saveToRedis()
#     results = []
#     keys = r.keys('*')
#     # keys.remove('scrape_date')
#     for equity in keys:
#         res = r.hgetall(equity))
#         stock = dict()
#         for ind, prop in enumerate(res):
#             stock[columns[ind]] = prop.decode("utf-8")
#         results.append(stock)
#     return results


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
    print("lkhkj",data['name'])
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
                print(data)
                create_stock(data)
            line_count += 1

# process_csv_to_db("file.CSV")