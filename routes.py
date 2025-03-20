from app_init import app

from flask import render_template, jsonify, url_for, request, session, redirect
from models import AllowList, db, AllowedEmailEndings, BlockList
import logging
from datetime import datetime
import random

# Routes will be registered with the app instance later

import hmac
import hashlib
import time
import requests
import os
from datetime import datetime

# Cache for storing crypto and economic data
# Global variables for caching
crypto_cache = {}
economic_cache = {}
last_crypto_fetch_time = 0  # Initialize fetch time
last_economic_fetch_time = 0  # Initialize fetch time
CRYPTO_CACHE_DURATION = 5  # Cache duration in seconds
ECONOMIC_CACHE_DURATION = 3600  # 1 hour cache for economic data

def get_coinbase_signature(timestamp, method, request_path, body=''):
    try:
        message = f'{timestamp}{method}{request_path}{body}'
        key = os.environ['COINBASE_API_SECRET'].encode('utf-8')
        signature = hmac.new(key, message.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature
    except Exception as e:
        logging.error(f"Signature generation error: {str(e)}")
        logging.error(f"Timestamp: {timestamp}, Method: {method}, Path: {request_path}")
        return None

def fetch_crypto_data(symbol):
    api_key = os.environ['COINBASE_API_KEY']
    base_url = 'https://api.coinbase.com/api/v3/brokerage'
    endpoint = f'/products/{symbol}-USD/ticker'
    
    timestamp = str(int(time.time()))
    signature = get_coinbase_signature(timestamp, 'GET', endpoint)
    
    if not signature:
        logging.error(f"Failed to generate signature for {symbol}")
        return None
    
    headers = {
        'CB-ACCESS-KEY': api_key,
        'CB-ACCESS-SIGN': signature,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'Content-Type': 'application/json'
    }
    
    try:
        logging.info(f"Fetching crypto data for {symbol}")
        logging.info(f"Request Headers: {headers}")
        logging.info(f"Request URL: {base_url}{endpoint}")
        
        response = requests.get(f'{base_url}{endpoint}', headers=headers)
        
        logging.info(f"Response Status Code: {response.status_code}")
        logging.info(f"Response Headers: {response.headers}")
        logging.info(f"Response Content: {response.text}")
        
        response.raise_for_status()
        data = response.json()
        
        # More robust error checking
        if not data or 'price' not in data:
            logging.error(f"Invalid data received for {symbol}: {data}")
            return None
        
        price = float(data['price'])
        change = float(data.get('price_change_24h', 0))
        volume = float(data.get('volume_24h', 0))
        high = float(data.get('high_24h', price))
        low = float(data.get('low_24h', price))
        
        return {
            'price': price,
            'change': (change / (price - change)) * 100 if change != 0 else 0,
            'volume': volume,
            'high': high,
            'low': low
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for {symbol}: {str(e)}")
        return None
    except ValueError as e:
        logging.error(f"Value parsing error for {symbol}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching {symbol} data: {str(e)}")
        return None

def fetch_fred_economic_data():
    api_key = os.environ['FRED_API_KEY']
    base_url = 'https://api.stlouisfed.org/fred/series/observations'
    
    indicators = {
        'unemployment': 'UNRATE',  # Unemployment Rate
        'inflation': 'CPIAUCSL',  # Consumer Price Index
        'gdp_growth': 'GDP',      # GDP Growth Rate
        'interest_rate': 'FEDFUNDS'  # Federal Funds Rate
    }
    
    economic_data = {}
    
    for name, series_id in indicators.items():
        try:
            params = {
                'series_id': series_id,
                'api_key': api_key,
                'file_type': 'json',
                'limit': 2,  # Get last two observations
                'sort_order': 'desc'
            }
            
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            observations = data['observations']
            latest_value = float(observations[0]['value'])
            previous_value = float(observations[1]['value'])
            
            change_percent = ((latest_value - previous_value) / previous_value) * 100
            
            economic_data[name] = {
                'value': latest_value,
                'change_percent': change_percent,
                'trend': 'positive' if change_percent >= 0 else 'negative'
            }
        except Exception as e:
            logging.error(f"Error fetching {name} data: {str(e)}")
            economic_data[name] = {
                'value': 0,
                'change_percent': 0,
                'trend': 'neutral'
            }
    
    return economic_data

@app.route('/api/economic-indicators')
def get_economic_indicators():
    global last_economic_fetch_time, economic_cache
    
    current_time = time.time()
    if current_time - last_economic_fetch_time > ECONOMIC_CACHE_DURATION:
        try:
            economic_data = fetch_fred_economic_data()
            economic_cache = economic_data
            last_economic_fetch_time = current_time
        except Exception as e:
            logging.error(f"Error updating economic indicators: {str(e)}")
    
    return jsonify(economic_cache)

@app.route('/api/crypto-prices')
def get_crypto_prices():
    global last_crypto_fetch_time, crypto_cache
    
    current_time = time.time()
    if current_time - last_crypto_fetch_time > CRYPTO_CACHE_DURATION:
        symbols = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL']
        new_data = {}
        
        for symbol in symbols:
            data = fetch_crypto_data(symbol)
            if data:
                new_data[symbol] = data
            elif symbol in crypto_cache:
                new_data[symbol] = crypto_cache[symbol]
            else:
                new_data[symbol] = {
                    'price': 0,
                    'change': 0,
                    'volume': 0,
                    'high': 0,
                    'low': 0
                }
        
        crypto_cache = new_data
        last_crypto_fetch_time = current_time
    
    return jsonify(crypto_cache)

@app.route('/')
def home_route():
    return render_template('home.html', title='Home', logo_url=app.config['LOGO_URL'])

@app.route('/team')
def company_admins_route():
    allowed_emails = AllowList.query.all()
    allowed_endings = AllowedEmailEndings.query.all()
    blocked_emails = [block.email for block in BlockList.query.all()]
    
    # Add is_blocked attribute to each allowed email
    for email in allowed_emails:
        email.is_blocked = email.email in blocked_emails
    
    return render_template('company_admins.html', 
                         allowed_emails=allowed_emails,
                         allowed_endings=allowed_endings,
                         logo_url=app.config['LOGO_URL'])