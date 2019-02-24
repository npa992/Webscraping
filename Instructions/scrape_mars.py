#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return  Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    url='https://mars.nasa.gov/news/'
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')

    news_title=soup.find_all('div',class_='content_title')[0].text


    news_paragraph=soup.find_all('div',class_='article_teaser_body')[0].text


    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')


    img=soup.find_all('li',class_='slide')
    featured_image_url='https://www.jpl.nasa.gov'+img[0].find('a')['data-fancybox-href']



    url='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')

    tweet=soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather=tweet[4].text


    url='http://space-facts.com/mars/'
    tables = pd.read_html(url)
    df=pd.DataFrame(tables[0])
    html_table=df.to_html().replace('\n', '')

    
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')

    links=soup.find_all('h3')

    hemisphere_image_urls={}

    for link in links:
        browser.click_link_by_partial_text(link.text)
        soup = BeautifulSoup(browser.html, 'html.parser')
        img=soup.find('div',class_='downloads').find('a')
        hemisphere_image_urls[link.text]=img['href']
        print(link.text)
        print(img['href'])
        browser.back()

    
    first_dict={'news_title':news_title,'news_paragraph':news_paragraph,"mars_weather":mars_weather,
    'featured_img_url':featured_image_url, 'table':html_table}

    final_dict={**first_dict, **hemisphere_image_urls}

    browser.quit()
    
    return final_dict
    
