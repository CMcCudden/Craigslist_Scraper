import time
import re
from datetime import datetime
from models.search_listing import SearchListing
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from database import Database
from selenium import webdriver

# Configure database
db = Database()
db.create_search_listing_table()
# db.create_city_state_table()
# db.insert_city()

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

CHROME_DRIVER_PATH = r"/Users/caleb/Documents/chromedriver/chromedriver"
driver = webdriver.Chrome(ChromeDriverManager().install())
header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept-encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,de;q=0.8"
    }

CHICAGO = 'https://chicago.craigslist.org/search/apa?srchType=T&availabilityMode=0&sale_date=all+dates'
HONOLULU = 'https://honolulu.craigslist.org/search/apa?srchType=T&availabilityMode=0&sale_date=all+dates'
HOUSTON = 'https://houston.craigslist.org/search/apa?srchType=T&availabilityMode=0&sale_date=all+dates'
JUNEAU = 'https://juneau.craigslist.org/search/apa?srchType=T&availabilityMode=0&sale_date=all+dates'
LA = 'https://losangeles.craigslist.org/search/apa?srchType=T&availabilityMode=0&sale_date=all+dates'
NASHVILLE ='https://nashville.craigslist.org/search/apa?srchType=T&availabilityMode=0&sale_date=all+dates'
NYC = 'https://newyork.craigslist.org/search/apa?srchType=T&availabilityMode=0&sale_date=all+dates'
PHILADELPHIA = 'https://philadelphia.craigslist.org/search/apa?srchType=T&availabilityMode=0&sale_date=all+dates'
VEGAS = 'https://lasvegas.craigslist.org/search/apa?srchType=T&availabilityMode=0&sale_date=all+dates'


def scrape(URL):
    time.sleep(2)
    driver.get(URL)
# Wait for JS to load
    WebDriverWait(driver, 10).until(
         lambda x: x.find_element(By.ID, "search-results"))

    result_rows = driver.find_elements(By.CLASS_NAME, 'result-row')
    print(f"Found {len(result_rows)} result_rows on page")

    for row in result_rows:
        try:
            price = row.find_element(By.CLASS_NAME, 'result-price').text
            addr = row.find_element(By.CLASS_NAME, 'result-hood').text
            link = row.find_element(By.TAG_NAME, 'a').get_attribute('href')
            pic = row.find_element(By.TAG_NAME, 'img').get_attribute('src')

            print(link)
            print(price)
            print(addr)
            print(pic)

            # Change "$1,300/mo" to 1300, since database expects an integer
            price_int = int(re.sub("[^0-9]", "", price))

            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d")

            if URL == CHICAGO:
                city = 'chicago'
            elif URL == HONOLULU:
                city = 'honolulu'
            elif URL == HOUSTON:
                city = 'houston'
            elif URL == JUNEAU:
                city = 'juneau'
            elif URL == LA:
                city = 'los_angeles'
            elif URL == NASHVILLE:
                city = 'nashville'
            elif URL == NYC:
                city = 'new_york'
            elif URL == PHILADELPHIA:
                city = 'philadelphia'
            else:
                city = 'las_vegas'


            # Make an individual SearchListing object with the above data
            search_listing = SearchListing(address=addr, price=price_int, url=link, date=dt_string, city=city, picture=pic)

            # Save that listing to the database
            db.insert_search_listing(search_listing)

        except Exception as ex:
            print(ex)

    # # fetch all the listings from the db
    my_listings = db.get_all_search_listings()

    # # Print them out
    for listing in my_listings:
        print(f"id: {listing.id} address: {listing.address} price: {listing.price} url {listing.url} date: {listing.date}"
              f"city: {listing.city} picture url: {listing.picture}")


# db.delete_yesterdays_scrape()
time.sleep(5)
scrape(CHICAGO)
time.sleep(5)
scrape(HONOLULU)
time.sleep(5)
scrape(HOUSTON)
time.sleep(5)
scrape(JUNEAU)
time.sleep(5)
scrape(LA)
time.sleep(5)
scrape(NASHVILLE)
time.sleep(5)
scrape(NYC)
time.sleep(5)
scrape(PHILADELPHIA)
time.sleep(5)
scrape(VEGAS)
db.delete_search_listing_emptystr()
driver.close()
# clean up
db.close()
