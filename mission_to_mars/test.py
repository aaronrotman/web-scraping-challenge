# Dependencies and setup
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from splinter import Browser
import time


def scrape():


    # WEATHER
    url = 'https://twitter.com/marswxreport?lang=en'

    tweet_response = requests.get(url)
    print(tweet_response)

    tweet_soup = bs(tweet_response.text, 'lxml')
    print(tweet_soup.prettify())

    # weather_tweet = tweet_soup.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    weather_list = []
    weather_tweet = tweet_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    for weather in weather_tweet:
        weather_list.append(weather)
    mars_weather = weather_list[0]
    mars_weather = mars_weather.replace('\n', ' ')


    # FACT TABLE
    # Store the url
    url = 'https://space-facts.com/mars'

    # Scrape tabular data from the website
    tables = pd.read_html(url)

    # Store the desired table
    fact_table = tables[0]

    # Clean up table dataframe
    # Rename columns
    fact_table.columns = ['Attribute', 'Value']
    # Set 'Attribute' column as the index
    fact_table.set_index('Attribute', inplace=True)

    html_table = fact_table.to_html()

    # Dictionary of scraping results
    mars_dict = {
        'fact_table': html_table,
        'weather': mars_weather
    }

    return mars_dict
