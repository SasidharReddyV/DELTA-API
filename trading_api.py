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


MOM_API_KEY="08zzAOGvmYayCzdQPlXqbDhu7ayRZT"
delta_api_url = "https://api.india.delta.exchange/v2"
API_SECRET="TZm7kNbf91csQxCvRpl6t8u4bQfvplTa1Tdr39u6OCH3L68glptH2BNr4bgT"



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
    
    def get_curr_timestamp(self):
        """
        returns the Unix timestamp for the current time in UTC timezone
        
        """
        d = datetime.datetime.utcnow()
        epoch = datetime.datetime(1970,1,1)
        return str(int((d - epoch).total_seconds())*1) #1000 to get in millis
    
    def convert_date_to_timestamp(self,_date):
        """
        returns the Unix timestamp for a specific date in the format 'YYYYMMDD'
        
        """
        specific_date = datetime.datetime.strptime(_date, '%Y%m%d')
        epoch = datetime.datetime(1970, 1, 1)
        return str(int((specific_date - epoch).total_seconds()))
    
    
    def convert_date_time_to_timestamp(self,_datetime):
        """
        returns the Unix timestamp for a specific UTC date-time in the format 'YYYYMMDD-H:M:S'
        
        """
        specific_date = datetime.datetime.strptime(_datetime, '%Y%m%d-%H:%M:%S')
        epoch = datetime.datetime(1970, 1, 1)
        return str(int((specific_date - epoch).total_seconds()))
    
    def convert_timestamp_to_date_time(self,timestamp):
        """
        returns the UTC date-time in the format 'YYYYMMDD-H:M:S' from a Unix timestamp.
        """
        epoch = datetime.datetime(1970, 1, 1)
        specific_date = epoch + datetime.timedelta(seconds=int(timestamp))
        return specific_date.strftime('%Y%m%d-%H:%M:%S')
    
    def place_limit_ord(self,price,qty,side):
        timestamp = self.get_curr_timestamp()
        params = {
              "product_symbol": "BTCUSD",
              "limit_price": price,
              "size": qty,
              "side": side,
              "order_type": "limit_order",
              "post_only": False,
              "client_order_id": "1"
            }
        method = 'POST'
        path = '/v2/orders'
        query_string = ''
        payload = json.dumps(params)
        signature_data = method + timestamp + path + query_string + payload
        signature = self.generate_signature(signature_data)
        headers = {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'api-key': MOM_API_KEY,
              'signature': signature,
              'timestamp': timestamp
              }
        
        
        r = requests.post(f"{delta_api_url}/orders", json= params, headers = headers)
        print(r.json())

    
    def place_market_ord(self,qty,side):
        timestamp = self.get_curr_timestamp()
        params = {
              "product_symbol": "BTCUSD",
              "size": qty,
              "side": side,
              "order_type": "market_order",
              "client_order_id": "1"
            }
        method = 'POST'
        path = '/v2/orders'
        query_string = ''
        payload = json.dumps(params)
        signature_data = method + timestamp + path + query_string + payload
        signature = self.generate_signature(signature_data)
        headers = {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'api-key': MOM_API_KEY,
              'signature': signature,
              'timestamp': timestamp
              }
        r = requests.post(f"{delta_api_url}/orders", json= params, headers = headers)
        print(r.json())
    
    def place_cancel_ord(self,exch_ord_id, client_ord_id):
        timestamp = self.get_curr_timestamp()
        params = {
              "product_symbol": "BTCUSD",
              "id":exch_ord_id,
              "client_order_id": str(client_ord_id)
              }
        method = 'DELETE'
        path = '/v2/orders'
        query_string = ''
        payload = json.dumps(params)
        signature_data = method + timestamp + path + query_string + payload
        signature = self.generate_signature(signature_data)
        headers = {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'api-key': MOM_API_KEY,
              'signature': signature,
              'timestamp': timestamp
              }

        r = requests.delete(f"{delta_api_url}/orders", json=params, headers = headers)
        print(r.json())
        

    def place_modify_ord(self,exch_ord_id,new_price, new_qty):
        timestamp = self.get_curr_timestamp()
        params = {
              "product_symbol": "BTCUSD",
              "limit_price": new_price,
              "size": new_qty,
              "id": exch_ord_id #exch id is int client is string
            }
        method = 'PUT'
        path = '/v2/orders'
        query_string = ''
        payload = json.dumps(params)
        signature_data = method + timestamp + path + query_string + payload
        signature = self.generate_signature(signature_data)
        headers = {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'api-key': MOM_API_KEY,
              'signature': signature,
              'timestamp': timestamp
              }
        
        r = requests.put(f"{delta_api_url}/orders", json= params, headers = headers)
        print(r.json())
        
        
   
        
    def place_cancel_all_ords(self):
        headers = {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'api-key': MOM_API_KEY,
              'signature': '****',
              'timestamp': '****'
              }
        params = {
          "product_symbol": "BTCUSD",
          "contract_types": "perpetual_futures",
          "cancel_limit_orders": True,
          "cancel_stop_orders": True,
          "cancel_reduce_only_orders": True
                }
        r = requests.delete(f"{delta_api_url}/orders/all", json=params, headers = headers)
        print(r.json())
        
    def get_active_orders(self):
        timestamp = self.get_curr_timestamp()
        method = 'GET'
        path = '/v2/orders'
        query_string = ''
        signature_data = method + timestamp + path + query_string 
        signature = self.generate_signature(signature_data)
        headers = {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'api-key': MOM_API_KEY,
              'signature': signature,
              'timestamp': timestamp
              }
        r = requests.get('https://api.india.delta.exchange/v2/orders', headers = headers)
        print(r.json())

    
    
    
    
    



api_instance = API_TRADING(MOM_API_KEY,API_SECRET,delta_api_url)
#api_instance.place_limit_ord("101000",1,"sell")
api_instance.get_active_orders()
#api_instance.place_cancel_ord(306456487, '1')
#api_instance.place_modify_ord(306456487,"102000", 2)
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
    