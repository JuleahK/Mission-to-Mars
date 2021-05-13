#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


url = 'https://redplanetscience.com/'
browser.visit(url)


# In[4]:


browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[5]:


html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')


# In[6]:


news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# # ## JPL Space Images Featured Image

# In[8]:


url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # ## Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[14]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


df.to_html()


# In[16]:


browser.quit()


# In[ ]:




