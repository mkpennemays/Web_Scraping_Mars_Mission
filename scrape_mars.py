from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

##### TOP NEWS STORY ######

# URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
# Retrieve page with the requests module
    response = requests.get(url)

# Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

# results are returned as an iterable list
    results = soup.find_all('div', class_="slide")

# Loop through returned results
    nasa_news =[]
    for result in results:
    # Error handling
        try:
        # Identify and return title of listing
            title = result.find('div', class_="content_title").text
            teaser = result.find('div', class_="rollover_description_inner").text

            if (title):
                news_detail = {"title":title,"teaser":teaser}
                nasa_news.append(news_detail)
        except AttributeError as e:
            print(e)


######  MARS FACTS #####
    url_3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_3)
    mars_facts_df = tables[0]
    mars_facts_html_table = mars_facts_df.to_html()

######  MARS IMAGES #####

    url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url_4)

    items = browser.find_by_id("product-section")
    items = browser.find_by_css('div[class="description"]')
    item_count = len(items)
    main_url = "https://astrogeology.usgs.gov"
    hemisphere_image_urls = []
    for x in range(item_count):   
        browser.visit(url_4)
        items = browser.find_by_id("product-section")
        items = browser.find_by_css('div[class="description"]')
        atags = items[x].find_by_tag('a')
        
        atags[0].click()
        #find the link for the image and save to list
            #find div download
        new_url = browser.url
        response = requests.get(new_url)
        soup = bs(response.text, 'html.parser')
        results = soup.find_all('h2')
        img_label = results[0].text
        images = soup.find_all('img')
        images = soup.find_all('img', attrs={"class":"wide-image"})
        link_text = main_url + images[0]['src']
        hemisphere_image_urls.append({"title":img_label, "url": link_text})

    browser.quit()
    mars_data = {"top_story": nasa_news[0],"mars_facts": mars_facts_html_table, "mars_images":hemisphere_image_urls}  
    #save this to mongodb
    return mars_data






