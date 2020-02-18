import requests
from bs4 import BeautifulSoup
from flask import Flask, json
from scrapper import WorldMeterScrapper as Scrapper
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


def get_soup():
    page = Scrapper.load_page()
    soup = Scrapper.create_soup(page.text)
    return soup


@app.route('/')
def main():
    return "<h1>Welcome to CoronaVirus meter</h1><br>/basic</br>/table<br>/part"


@app.route('/basic')
def basic_data():
    basic = Scrapper.get_basic_data(get_soup())
    return json.jsonify(basic)


@app.route('/table')
def table():
    table = Scrapper.get_table(get_soup())
    return json.jsonify(table)


@app.route('/part')
def part():
    divs = Scrapper.get_all_div(get_soup())
    return json.jsonify(divs)


if __name__ == '__main__':
    app.run()
