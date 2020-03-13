#!/usr/bin/env python
# coding: utf-8

# In[237]:


### IMPORTING DEPENDENCIES ###
import pymongo
import datetime
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import os
from pprint import pprint
from splinter.exceptions import ElementDoesNotExist


# In[238]:


get_ipython().system('which chromedriver')


# #################################################################
# ### This section is meant to scrape the Nasa Mars News site to 
# ### collect the latest News Title and Paragraph Text 
# ### and save as variables for reference later 
# #################################################################

# In[248]:


# specifying page url
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# initialize chrome browser and splinter
executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# visiting webpage
browser.visit(url)

# defining html
html = browser.html

# creating beautiful soup object
soup = bs(html, 'html.parser')

# getting the first element from the page
element = soup.select_one('ul.item_list li.slide')

# getting latest headline
latest_headline = element.find("div", class_ = "content_title").get_text()

# getting latest description
latest_description = element.find("div", class_ = "article_teaser_body").get_text()

# exit current splinter browser
browser.quit()


# #################################################################
# ### This section is meant to Use splinter to navigate the site 
# ### and find the image url for the current Featured Mars Image 
# ### and assign the url string to a variable 'featured_image_url'
# #################################################################

# In[249]:


# specifying page url
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

# initialize chrome browser and splinter
executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# visiting webpage
browser.visit(url)

# defining the button that takes to the full sized featured image
full_image_button = browser.find_by_id('full_image')

# clicking buttong to view featured image
full_image_button.click()

# defining button to click next; the 'more info' button on the page
more_info_button = browser.find_by_text('more info     ')

# clicking more info
more_info_button.click()

# finding/defining the full res .jpg link
full_res_jpg_button = browser.links.find_by_partial_text('.jpg')

# clicking the full res .jpg link (final navigation)
full_res_jpg_button.click()

# getting featured image url using splinter's browser.url
featured_image_url = browser.url

# exit current splinter browser
browser.quit()


# #################################################################
# ### This section is meant to visit the Mars Weather twitter 
# ### account and scrape the latest Mars weather tweet from 
# ### the page. Save the tweet text for the weather report as a 
# ### variable called 'mars_weather'
# #################################################################

# In[250]:


# specifying page url
url = 'https://twitter.com/marswxreport?lang=en'

# initialize chrome browser and splinter
executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# visiting webpage
browser.visit(url)

ispres = browser.is_element_present_by_id('accessible-list-0', wait_time = 10)

# defining html
html = browser.html

# creating beautiful soup object
soup = bs(html, 'html.parser')

#### CHECK TOMORROW AND LATER TODAY AND TRY TO MAKE BETTER THIS IS ASS ######
divs = soup.find_all('div')
spans = []
texts =[]
for div in divs:
    span = div.find('span')
    if span != None:
        text = span.text
        if text != '':
            texts.append(text)
mars_weather = texts[85]

# exit current splinter browser
browser.quit()


# In[251]:


print(mars_weather)


# #################################################################
# ### This next section of code is meant to visit the Mars Facts
# ### webpage here and use Pandas to scrape the table containing 
# ### facts about the planet including Diameter, Mass, etc.
# #################################################################

# In[252]:


# specifying page url
url = 'https://space-facts.com/mars/'

# initialize chrome browser and splinter
executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# visiting webpage
browser.visit(url)

# defining html
html = browser.html

# creating the soup
soup = bs(html, 'html.parser')

# finding/defining table I want to scrape
scraped_table = soup.find_all('table')[0]

# creating pandas dataframe from html
mars_facts_df = pd.read_html(str(scraped_table))

# exit current splinter browser
browser.quit()


# ############################################################
# ### This next section of code is meant to Visit the USGS 
# ### Astrogeology site here to obtain high resolution images 
# ### for each of Mars' hemispheres.
# ############################################################

# In[253]:


# defining url
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

# initialize chrome browser and splinter
executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# visiting webpage
browser.visit(url)

# establish html
html = browser.html
    
# create soup
soup = bs(html, 'html.parser')

# finding hemisphere items using beautiful soup, then
# looping through items to get each hemisphere title in a list
# called 'mars_hemispheres'
mars_hemisphere_items = soup.find_all('div', class_='item')
mars_hemisphere_titles = []

for item in mars_hemisphere_items:
    mars_hemisphere_titles.append(item.h3.text)

# exit active browser
browser.quit()

# initializing hemisphere urls list and dictionary to hold info
hemisphere_img_urls = []
mars_dict = {}

# for loop to get desired info from each mars hemisphere link
for hemisphere in mars_hemisphere_titles:
    
    # establish new splinter browser
    executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)

    # visiting webpage
    browser.visit(url)
    
    # finds and clicks desired link
    browser.links.find_by_partial_text(hemisphere).click()
    
    # establish html
    html = browser.html
    
    # create soup
    soup = bs(html, 'html.parser')
    
    # gets full resolution image url
    img_url = soup.find('ul').li.a['href']
    
    # creates dictionary item for final list
    mars_dict = {'title' : hemisphere,
                 'img_url' : img_url}
    
    # appends aforementioned dictionary to list
    hemisphere_img_urls.append(mars_dict)
       
    # exit current splinter browser
    browser.quit()


# In[ ]:


### converting notebook to scrape_mars.py file
### NEEDS TO CHANGE FILE NAME
get_ipython().system('jupyter nbconvert --to script mission_to_mars.ipynb')


# In[ ]:





# In[ ]:




