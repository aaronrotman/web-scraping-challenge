# Dependencies and setup
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from splinter import Browser
import time


def scrape():
    # MARS FEATURED IMAGE
    feat_img_base_url = "https://www.jpl.nasa.gov/"
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Chrome driver setup
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    try:
        browser.visit(jpl_url)
        html = browser.html

        soup = bs(html, "html.parser")

        print(soup.prettify())

        feat_image = soup.find('div', class_="carousel_items")
        feat_img_url = feat_image.a['data-link']

        # Navigate to article page for the featured image
        browser.visit(f"{feat_img_base_url}{feat_img_url}")

        feat_img_html = browser.html
        feat_soup = bs(feat_img_html, "html.parser")


        img_fig = feat_soup.find('figure', class_='lede')
        img_fig_url = img_fig.a['href']

        # Close the browser
        browser.quit()
    except Exception as e:
        print(e)
        # Close the browser
        browser.quit()
    # WEATHER
    url = 'https://twitter.com/marswxreport?lang=en'
    try:
        tweet_response = requests.get(url)
        print(tweet_response)

        tweet_soup = bs(tweet_response.text, 'lxml')
        print(tweet_soup.prettify())

        weather_list = []
        weather_tweet = tweet_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
        for weather in weather_tweet:
            weather_list.append(weather)
        mars_weather = weather_list[0]
        mars_weather = mars_weather.replace('\n', ' ')
    except Exception as e:
        print(e)
        # Close the browser
        browser.quit()

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

    # HEMISPHERE IMAGE URLS
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Store the URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Go to website
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'lxml')

    image_links = soup.find_all('div', class_='description')
    hemi_base_url = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = []

    for link in image_links:
        try:
            print(f'Visiting: {link.h3.text}')
            time.sleep(1)
            print('Visiting...')
            browser.click_link_by_partial_text(link.h3.text)
            time.sleep(1)
            
            html = browser.html
            soup = bs(html, 'lxml')

            title = soup.find('h2', class_='title')
            
            image = soup.find('img', class_='wide-image')
            print(image['src'])
            hemisphere_image_urls.append({'title': title.text, 'img_url': f"{hemi_base_url}{image['src']}"})
            print('Data scraped')
            browser.visit(url)
        except Exception as e:
            print(e)
            browser.visit(url)
    # Close the browser
    browser.quit()

    # Dictionary of scraping results
    mars_dict = {
        'fact_table': html_table,
        'weather': mars_weather,
        'hemisphere_image_urls': hemisphere_image_urls,
        'feat_image_url': f"{feat_img_base_url}{img_fig_url}"
    }
    return mars_dict
