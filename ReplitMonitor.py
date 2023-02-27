import requests
import time
import config
from flask import Flask
from threading import Thread
import logging

logging.basicConfig(filename='output.log', level=logging.ERROR)

app = Flask('')


@app.route('/')
def home():
    return "Скрипт SNAA активен"


def run():
    app.run(host='0.0.0.0', port=80)


with open('output.log', 'w') as f:
    pass


def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()

while True:
    try:
        response = requests.head(config.link)
        response.raise_for_status()
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something Else", err)
    time.sleep(60)