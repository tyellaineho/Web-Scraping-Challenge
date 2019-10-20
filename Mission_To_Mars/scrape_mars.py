from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}

    #latest news data
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    news_html = browser.html
    soup = BeautifulSoup(news_html, "html.parser")
    #scrape latest news
    mars_data["news_title"] = soup.find('div', class_='content_title').text.strip()
    mars_data['news_p'] = soup.find('div', class_='article_teaser_body').get_text()

    #featured image url
    images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)
    images_html = browser.html
    images_soup = BeautifulSoup(images_html, 'html.parser')
    imageurl_head = 'https://www.jpl.nasa.gov'
    imageurl_tail = images_soup.find('div', class_='carousel_items').a['data-fancybox-href']
    #scrape featured image url
    mars_data['featured_image_url'] = imageurl_head + imageurl_tail

    #weather report
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')
    mars_weather = twitter_soup.find('div', class_='js-tweet-text-container').p.get_text().strip()
    mars_weather = mars_weather.replace('\n', ' ')
    #scrape weather data
    mars_data['mars_weather'] = mars_weather.split('pic.twitter.com')[0]

    #mars table
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    mars_facts = tables[1]
    #scrape table
    html_table = mars_facts.to_html(header=False, index=False)
    mars_data['mars_table'] = html_table.replace('\n', '')

    #hemisphere data
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    hem_html = browser.html
    hem_soup = BeautifulSoup(hem_html, 'html.parser')
    hem_desc = hem_soup.find_all('div', class_='description')
    #find links
    link_head = "https://astrogeology.usgs.gov"
    link_collection = []
    for desc in hem_desc:
        link_tail = desc.a['href']
        link_collection.append(link_head+link_tail)
    #find hemisphere image urls
    hemtitleurl_collection =[]

    for link in link_collection:
        browser.visit(link)
        hemimage_html = browser.html
        hemimage_soup = BeautifulSoup(hemimage_html, 'html.parser')
        hemimage_url = hemimage_soup.find('li').a['href']
        hemimage_title = hemimage_soup.find('h2', class_='title').text.strip()
        hem_dict = {"title" : hemimage_title, "url" : hemimage_url}
        hemtitleurl_collection.append(hem_dict)
        mars_data['hemis_dict'] = hemtitleurl_collection

    print(mars_data['hemis_dict'])

    return mars_data

if __name__ == "__main__":
    print(scrape())