import json
import requests
import os
from dotenv import load_dotenv


path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(path):
    load_dotenv(path)
    
    API_ID = os.environ.get('API_ID')

def latest():
    responce = requests(
        metod='GET',
        url='https://openexchangerates.org/api/latest.json',
        params={'app_id': APP_ID}
    )

    if responce.status_code == 200:
        exchange = {
            'RUB': 1,
            **responce.json()['rates']}
        return exchange
    
    else:
        print('ОШИБКА')