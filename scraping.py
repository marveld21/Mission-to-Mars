# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
        "hemisphere_data": hemisphere_scrape(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

#----------------Mars Hemisphere Scraping------------------------------
def hemisphere_scrape(browser) :
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    hemisphere_image_urls = []
    html = browser.html
    marssoup = soup(html, 'html.parser')
    h3s = marssoup.find_all('h3')

    #titles
    titles = []

    for h3 in h3s[:4]:
        titles.append(h3.text)

    # get urls extensions for image urls
    urlext = []
    for item in marssoup.find_all(attrs={'class':'itemLink product-item'}):
        urlext.append(item.get('href'))

    #make list unique
    urlextunique = []
    list_set = set(urlext)
    # convert the set to the list
    unique_list = (list(list_set))
    for x in unique_list:
        urlextunique.append(x)
    urlextunique

    urlext2=[]
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

    #combine titles and jpgs to dict
    #and combine dicts to list
    dict = {}
    hemisphere_image_urls = []
    for x in range(0,4):
        dict = {'img_url':jpg[x]}
        hemisphere_image_urls.append(dict)
        dict = {'title':titles[x]}
        hemisphere_image_urls.append(dict)

    browser.quit()
    return hemisphere_image_urls




if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())