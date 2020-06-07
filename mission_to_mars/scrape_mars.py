# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from splinter import Browser
import time

def scrape():
    # # Dictionary to store the scraped data
    mars_dict = {}

    # MARS NEWS
    # Store the URL for the NASA Mars News website
    news_url = "https://mars.nasa.gov/news/"
    # Chrome driver setup
    executable_path = {'executable_path': 'chromedriver.exe'}   
    # Instantiate Browser
    browser = Browser('chrome', **executable_path, headless=False)
    # Attempt to scrape the NASA Mars News website
    try:
        # Visit the url
        browser.visit(news_url)
        # Wait for the website to fully load
        time.sleep(5)
        # Scrape the html from the site
        html = browser.html
        # Close the browser
        browser.quit()

        # Create Beautiful Soup object from scraped html
        soup = bs(html, "html.parser")

        # Extract and store the latest news title and paragraph description
        latest_news = soup.find('div', class_="image_and_description_container")
        news_title = latest_news.find('div', class_='content_title').text
        news_p = latest_news.find('div', class_='article_teaser_body').text
        news_dict = {'title': news_title, 'para': news_p}
        # Add the news title and paragraph description to the scraping results dictionary: 'mars_dict'
        mars_dict['latest_news'] = news_dict

    # Handle errors
    except Exception as e:
        # Print exception
        print(e)
        mars_dict['latest_news'] = {'title': 'Scraping Failed', 'paragrah': 'Scraping Failed'}
        # Close the browser
        browser.quit()


    # MARS FEATURED IMAGE
    # Base URL
    feat_img_base_url = "https://www.jpl.nasa.gov/"
    # URL to scrape
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Attempt to scrape the JPL Mars website's featured image
    try: 
        
        # Instantiate Browser
        browser = Browser('chrome', **executable_path, headless=False)
        # Visit the url
        browser.visit(jpl_url)
        # Scrape the html from the site
        html = browser.html
        # Create Beautiful Soup object from scraped html
        soup = bs(html, "html.parser")
        # Extract the URL for the featured image page
        feat_image = soup.find('div', class_="carousel_items")
        feat_img_url = feat_image.a['data-link']

        # Navigate to the article page for the featured image
        browser.visit(f"{feat_img_base_url}{feat_img_url}")
        # Scrape the html from the featured image page
        feat_img_html = browser.html
        # Create Beautiful Soup object from scraped html
        feat_soup = bs(feat_img_html, "html.parser")
        # Extract the URL for the full size featured image
        img_fig = feat_soup.find('figure', class_='lede')
        img_fig_url = img_fig.a['href']
        
        # Add the full size featured image url to the scraping results dictionary: 'mars_dict'
        mars_dict['feat_image_url'] = f"{feat_img_base_url}{img_fig_url}"
        
        # Close the browser
        browser.quit()
    # Handle errors
    except Exception as e:
        # Print exception
        print(e)
        mars_dict['feat_image_url'] = "#"
        # Close the browser
        browser.quit()
        

    # MARS WEATHER 
    # URL to scrape
    url = 'https://twitter.com/marswxreport?lang=en'
    # Instantiate Browser
    browser = Browser('chrome', **executable_path, headless=False)

    # Attempt to scrape the Mars weather twitter account
    try: 
        # Visit the Mars Weather twitter page
        browser.visit(url)
        # Wait for the website to load
        time.sleep(5)
        # Create Beautiful Soup object from scraped html
        html = browser.html
        soup = bs(html, "html.parser")
        weather_data = soup.find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
        # Replace line breaks with spaces
        replaced_weather_data = weather_data.text.replace("\n", " ")
        mars_dict['weather'] = replaced_weather_data
        browser.quit()
    # Handle errors
    except Exception as e:
        # Print exception
        print(e)
        mars_dict['weather'] = "Scraping Failed"
        browser.quit()


    # MARS FACTS
    # Store the URL to scrape
    url = 'https://space-facts.com/mars'

    # Attempt to scrape the Mars facts website
    try: 
        # Scrape tabular data from the website using pandas
        tables = pd.read_html(url)

        # Store the Mars fact table
        fact_table = tables[0]

        # Clean up table dataframe
        # Rename columns
        fact_table.columns = ['Attribute', 'Value']
        # Set 'Attribute' column as the index
        fact_table.set_index('Attribute', inplace=True)

        # Convert the fact table to an html string
        html_table = fact_table.to_html()
        
        # Add the Mars fact table html string to the scraping results dictionary: 'mars_dict'
        mars_dict['fact_table'] = html_table
        
    # Handle errors
    except Exception as e:
        # Print exception
        print(e)


    # MARS HEMISPHERES
    # Base URL
    hemi_base_url = 'https://astrogeology.usgs.gov'
    # URL to scrape
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Instantiate Browser
    browser = Browser('chrome', **executable_path, headless=False)

    # Go to the mars hemispheres website
    browser.visit(url)
    # Scrape the html
    html = browser.html
    # Create Beautiful Soup object from scraped html
    soup = bs(html, 'lxml')

    # Extract the div containing the link to each hemisphere page
    image_links = soup.find_all('div', class_='description')

    # List to store full size hemisphere image urls
    hemisphere_image_urls = []

    # Attempt to scrape each hemisphere page to extract the full size image URL
    for link in image_links:
        # Visit hemisphere page
        try:
            print(f'Visiting: {link.h3.text}')
            # Wait for website to load
            time.sleep(1)
            print('Visiting...')
            # Visit hemisphere page
            browser.click_link_by_partial_text(link.h3.text)
            # Wait for website to load
            time.sleep(1)
            
            # Scrape html
            html = browser.html
            # Create Beautiful Soup object from scraped html
            soup = bs(html, 'lxml')

            # Store the image title
            title = soup.find('h2', class_='title')
            # Store the image URL
            image = soup.find('img', class_='wide-image')
            
            # Add the image title and url to the list of hemisphere image urls
            hemisphere_image_urls.append({'title': title.text, 'img_url': f"{hemi_base_url}{image['src']}"})
            print('Data scraped')
            
            # Return to the previous page
            browser.visit(url)
        except Exception as e:
            print(e)
            browser.visit(url)

    # Close the browser
    browser.quit()
    # Add the Mars hemisphere image URLs to the scraping results dictionary: 'mars_dict'
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict