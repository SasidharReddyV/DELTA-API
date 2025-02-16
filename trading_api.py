#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 10:10:05 2025

@author: sasidharreddy
"""

import os
import hashlib
import hmac
import base64
import requests
import datetime
import csv
import time
import json


MOM_API_KEY="vAHP5D1PacHQTsI3UgUS4eNZ6Fw4Fa"
delta_api_url = "https://api.india.delta.exchange/v2"



class API_TRADING:
    def __init__(self, api_key, api_secret,api_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url
        
        
    def setup_request_types(self):
        self.get_orderbook= os.path.join(self.api_url, "l2orderbook")
        self.get_historical_candles= os.path.join(self.api_url, "history/candles")
        
       
    
    def generate_signature(self,message):
        message = bytes(message, 'utf-8')
        secret = bytes(self.api_secret, 'utf-8')
        hash = hmac.new(secret, message, hashlib.sha256)
        return hash.hexdigest()
    
    def get_curr_timestamp():
        """
        returns the Unix timestamp for the current time in UTC timezone
        
        """
        d = datetime.datetime.utcnow()
        epoch = datetime.datetime(1970,1,1)
        return str(int((d - epoch).total_seconds()))
    
    def convert_date_to_timestamp(_date):
        """
        returns the Unix timestamp for a specific date in the format 'YYYYMMDD'
        
        """
        specific_date = datetime.datetime.strptime(_date, '%Y%m%d')
        epoch = datetime.datetime(1970, 1, 1)
        return str(int((specific_date - epoch).total_seconds()))
    
    
    def convert_date_time_to_timestamp(_datetime):
        """
        returns the Unix timestamp for a specific UTC date-time in the format 'YYYYMMDD-H:M:S'
        
        """
        specific_date = datetime.datetime.strptime(_datetime, '%Y%m%d-%H:%M:%S')
        epoch = datetime.datetime(1970, 1, 1)
        return str(int((specific_date - epoch).total_seconds()))
    
    def convert_timestamp_to_date_time(timestamp):
        """
        returns the UTC date-time in the format 'YYYYMMDD-H:M:S' from a Unix timestamp.
        """
        epoch = datetime.datetime(1970, 1, 1)
        specific_date = epoch + datetime.timedelta(seconds=int(timestamp))
        return specific_date.strftime('%Y%m%d-%H:%M:%S')
    
    def place_limit_ord(price,qty,side,stop_price = None):
        headers = {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'api-key': MOM_API_KEY,
              'signature': '****',
              'timestamp': '****'
              }
        
        params = {
              "product_id": 27,
              "product_symbol": "BTCUSD",
              "limit_price": price,
              "size": qty,
              "side": side,
              "order_type": "limit_order",
              "stop_order_type": "stop_loss_order",
              "stop_price": "56000",
              "trail_amount": "50",
              "stop_trigger_method": "last_traded_price",
              "mmp": "disabled",
              "post_only": False,
              "reduce_only": False,
              "client_order_id": "34521712",
              "cancel_orders_accepted": False
            }
        r = requests.post(delta_api_url+'/orders', params= params, headers = headers)
        print(r.json())

    
    def place_market_ord():
        pass
    
    def place_cancel_ord():
        pass
    def place_modify_ord():
        pass
    def place_cancel_all_ords():
        pass
    
    
    
    
    
test_api = API_TRADING("abc", "edf", delta_api_url)
#print(test_api.generate_signature( "this is a messge"))

headers = {
  'Accept': 'application/json'
}

start_day = API_TRADING.convert_date_to_timestamp('20240601')

"""
total_data = []


csv_file = 'output.csv'
file_exists = os.path.isfile(csv_file)
while(True):
    upto_candles = str(int(start_day)+2000*15*60)
    r = requests.get('https://api.india.delta.exchange/v2/history/candles', params={
  'resolution': '15m',  'symbol': 'BTCUSD',  'start': start_day,  'end': upto_candles
}, headers = headers)
    data = r.json()['result']
    if(not data):
        break
    sorted_data = sorted(data, key=lambda x: x['time'])
    start_day = str(int(upto_candles)+15*60)
    print(f"running for start_day:{start_day}")
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if not file_exists or os.stat(csv_file).st_size == 0:
            writer.writeheader()
        writer.writerows(sorted_data)
    time.sleep(1)
    
"""  
    
#print(API_TRADING.convert_timestamp_to_date_time(1717200000))
#print(API_TRADING.convert_timestamp_to_date_time(1737000000))
    