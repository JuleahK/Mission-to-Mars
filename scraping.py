#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemisphere(browser)


    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres" : hemisphere_image_urls,
      "last_modified": dt.datetime.now()
    }
    
    browser.quit()
    return data


def mars_news(browser):

    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)


    html = browser.html
    news_soup = soup(html, 'html.parser')

   
    try:
        slide_elem = news_soup.select_one('div.list_text')
        
        news_title = slide_elem.find('div', class_='content_title').get_text()
      
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
   
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

   
    html = browser.html
    img_soup = soup(html, 'html.parser')

  
    try:
      
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

   
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url


def mars_facts():

    try:
        
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

  
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

   
    return df.to_html(classes="table table-striped")

def hemisphere(browser):
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    browser.visit(url)
    
    hemisphere_image_urls = []
    
    image_urls = [(a.text, a['href']) for a in browser
         .find_by_css('div[class="description"] a')]
    
    for title,url in image_urls:
        
    
        hemispheres = {}
    
        browser.visit(url)
        img_url = browser.find_by_css('img[class="wide-image"]')['src']
        hemispheres['img_url'] = img_url
        hemispheres['title'] = title
    
        hemisphere_image_urls.append(hemispheres)   
        
    return hemisphere_image_urls
    
    

if __name__ == "__main__":
   
    print(scrape_all())






