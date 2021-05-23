#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html=browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## JPL Space Images Featured Image

# In[8]:


url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


full_image_elem=browser.find_by_tag('button')[1]
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


# ##  Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# ## Deliverable 1: High-Resolution Mars' Hemisphere Images and Titles

# ### Hemispheres

# In[29]:


# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
browser.visit(url)


# In[30]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[31]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.

html = browser.html
img_soup = soup(html, 'html.parser')

image_urls = [(a.text, a['href']) for a in browser
         .find_by_css('div[class="description"] a')]

for title,url in image_urls:
    
    hemispheres = {}
    
    browser.visit(url)
    img_url = browser.find_by_css('img[class="wide-image"]')['src']
    hemispheres['img_url'] = img_url
    hemispheres['title'] = title
    
    hemisphere_image_urls.append(hemispheres)    


# In[33]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[34]:


# 5. Quit the browser
browser.quit()


# In[ ]:




