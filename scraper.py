import requests
import lxml
from bs4 import BeautifulSoup
from getpass import getpass
from mysql.connector import connect, Error
import json
import datetime
from datetime import date
import time

today = date.today()


def scrape_function():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37"
    url = 'https://www.investing.com/equities/52-week-high'
    source = requests.get(url, headers={'User-Agent': user_agent}).text
    soup = BeautifulSoup(source, 'lxml')
    table = soup.find('div', class_='wrapper').find('section', id='leftColumn').find(
        'div', id='stockPageInnerContent').find('table').find('tbody')
    todays_stocks = []

    for item in table.find_all('tr'):
        contents = item.find_all('td')
        name, link = contents[1].find(
            'a').text, 'https://www.investing.com' + contents[1].find('a')['href']
        name = name.replace("'", "")
        todays_stocks.append([name, link])
    # stock_data = [name, link] + [contents[i].text for i in range(3, 7)]
    return todays_stocks


def name_to_ticker(name):
    search_results = requests.get("https://finnhub.io/api/v1/search?q={0}&token={1}".format(
        name.lower(), "c08cdff48v6plm1elgig")).json()
    if search_results and search_results["result"]:
        return search_results["result"][0]["displaySymbol"]
    else:
        return ""


def stock_data(ticker):
    data = requests.get("https://finnhub.io/api/v1/stock/metric?symbol={0}&metric=all&token={1}".format(
        ticker, "c08cdff48v6plm1elgig")).json()
    try:
        if data and data["metric"]:
            high, low = data["metric"]["52WeekHigh"], data["metric"]["52WeekLow"]
            if high and low:
                return [round(high, 3), round(low, 3)]
            else:
                return ["", ""]
        else:
            return ["", ""]
    except:
        pass


def test_update():
    try:
        connection = connect(
            host="localhost",
            user="root",
            password=getpass("enter password: "),
            database="52_week_high_freq",
        )
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM freq_stocks;")
        result = cursor.fetchall()
        for i in range(len(result)):
            if i % 50 == 0:
                time.sleep(5)
            name = result[i][0]
            ticker = name_to_ticker(name)
            if ticker:
                high, low = stock_data(ticker)
                cursor.execute("UPDATE freq_stocks SET ticker='{0}', high='{1}', low='{2}' WHERE name='{3}';".format(
                    ticker, high, low, name))
            print(name, ticker)
            connection.commit()
    except Error as e:
        print(e)


def update_database():
    try:
        connection = connect(
            host="localhost",
            user="root",
            password=getpass("enter password: "),
            database="52_week_high_freq",
        )
        cursor = connection.cursor(buffered=True)
        stocks = scrape_function()
        for item in stocks:
            name, link, high, low, change, percent_change = item
            cursor.execute(
                "SELECT * FROM freq_stocks WHERE name='{0}';".format(name))
            result = cursor.fetchall()
            print(result)
            if result:  # updating
                updated_freq = result[0][2] + 1
                cursor.execute("UPDATE freq_stocks SET frequency='{0}', dates = JSON_ARRAY_APPEND(dates, '$', '{1}') WHERE name='{2}';".format(
                    updated_freq, today, name))
            else:  # initialization
                cursor.execute(
                    "INSERT INTO freq_stocks (name, ticker, link, frequency) VALUES ('{0}', '{1}', '{2}', 1);".format(name, name_to_ticker(name), link))
                cursor.execute(
                    "UPDATE freq_stocks SET dates = JSON_ARRAY_INSERT('[]', '$[0]', '{0}') WHERE name='{1}';".format(today, name))
        cursor.execute("SELECT * FROM freq_stocks;")
        result = cursor.fetchall()
        for row in result:
            name, link, frequency, dates = row[:4]
            diff = (today - datetime.datetime.strptime(
                dates[1:-1].split(', ')[0][1:-1], '%Y-%m-%d').date()).days
            if diff > 30:  # if interval between today and earliest listed day is more than 30 days
                cursor.execute("UPDATE freq_stocks SET frequency='{0}', dates = JSON_REMOVE(dates, '$[0]') WHERE name='{1}';".format(
                    frequency - 1, name))
        cursor.execute("SELECT * FROM freq_stocks;")
        result = cursor.fetchall()
        for row in result:
            name, link, frequency, dates = row[:4]
            if not dates:  # if no occurrences on 52-week-highs list within 30 days before today, remove entry
                cursor.execute(
                    "DELETE FROM freq_stocks WHERE name='{0}';".format(name))
        result = cursor.fetchall()
        for i in range(len(result)):  # updating values
            if i % 50 == 0: # sleep for 5 seconds every 50 requests
                time.sleep(5)
            name = result[i][0]
            ticker = name_to_ticker(name)
            if ticker:
                high, low = stock_data(ticker)
                cursor.execute("UPDATE freq_stocks SET ticker='{0}', high='{1}', low='{2}' WHERE name='{3}';".format(
                    ticker, high, low, name))
            print(name, ticker)
            connection.commit()
    except Error as e:
        print(e)

# call function
update_database()
