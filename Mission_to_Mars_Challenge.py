#!/usr/bin/env python
# coding: utf-8

# In[169]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import selenium


# In[170]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[171]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[172]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[173]:


slide_elem.find('div', class_='content_title')


# In[174]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[175]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[176]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[177]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[178]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[179]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[180]:


# Use the base URL to create an absolute URL
img_url = f'{url}/{img_url_rel}'
img_url


# In[181]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[182]:


df.to_html()


# In[183]:


#browser.quit()


# #start of starter code

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[184]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[185]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.


# In[186]:


html = browser.html
marssoup = soup(html, 'html.parser')


#titles
h3s = marssoup.find_all('h3')
h3s

titles = []

for h3 in h3s[:4]:
    titles.append(h3.text)
print(titles)


# In[187]:


# get urls extensions for image urls
urlext = []
for item in marssoup.find_all(attrs={'class':'itemLink product-item'}):
    urlext.append(item.get('href'))
urlext


# In[188]:


#make list unique
urlextunique = []
list_set = set(urlext)
# convert the set to the list
unique_list = (list(list_set))
for x in unique_list:
    urlextunique.append(x)
urlextunique


# In[189]:


#go to each hemis page and get jpg

urlext2=[]
try: urlextunique.remove('#')
except:
    pass

for uhemi in urlextunique[:4]:
        urlhemi = url+uhemi
        browser.visit(urlhemi)
        html = browser.html
        hemisoup = soup(html, 'html.parser')
        
        urlext = []
        for item2 in hemisoup.find_all('a'):
            urlext.append(item2.get('href'))
        urlext2.append(urlext[3])

jpgs = []
for j in urlext2:
    jpgs.append(url+j)
print(jpgs)

    


# In[190]:


#combine titles and jpgs to dict
#and combine dicts to list
dict = {}
hemisphere_image_urls = []
for x in range(0,4):
    dict = {'img_url':jpgs[x],'title':titles[x]}
    hemisphere_image_urls.append(dict)
print(hemisphere_image_urls)


# In[191]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[192]:


# 5. Quit the browser
browser.quit()


# In[ ]:




