from datetime import date

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from base import Session, engine, Base, Adds



with sync_playwright() as p:

    today = date.today()
    today_date = today.strftime("%d-%m-%Y") # dd-mm-YY

    Base.metadata.create_all(engine)
    session = Session()
  
    browser = p.chromium.launch()
    page = browser.new_page()
    # First page
    page.goto('https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273')
    page.is_visible('main')
    html = page.inner_html('main')
    soup = BeautifulSoup(html, 'lxml')
    search_items = soup.find_all('div', {'class': 'search-item'})
    
    for item in search_items:
        # Image urls
        img_url = item.find('div', {'class': 'image'}).img['src']

        # Date posted
        date_posted = item.find('span', {'class': 'date-posted'}).text.strip()
        if date_posted.upper().isupper(): # To know if there any letters
            date_posted = today_date
        else:
            date_posted = date_posted.replace('/', '-')
        
        # currency
        price = item.find('div', {'class': 'price'}).text.strip()
        if '$' in price:
            currency = 'USD'
        else:
            currency = price
        
        # Add to our database
        add_1 = Adds(img_url=img_url, date_posted=date_posted, currency=currency)
        session.add(add_1)

    session.commit()

    # total_ads = soup.find('span', {'class': 'resultsShowingCount-1707762110'}).text.split()[-2]
    # pages = int(int(total_ads) / 40) + 1
    
    for i in range(2,5): # There were max 100 pages.
        page.goto(f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{i}/c37l1700273')
        page.is_visible('main')
        html = page.inner_html('main')
        soup = BeautifulSoup(html, 'lxml')
        search_items = soup.find_all('div', {'class': 'search-item'})
        
        for item in search_items:
            # Image urls
            img_url = item.find('div', {'class': 'image'}).img['src']

            # Date posted
            date_posted = item.find('span', {'class': 'date-posted'}).text.strip()
            if date_posted.upper().isupper(): # To know if there any letters
                date_posted = today_date
            else:
                date_posted = date_posted.replace('/', '-')
            
            # currency
            price = item.find('div', {'class': 'price'}).text.strip()
            if '$' in price:
                currency = 'USD'
            else:
                currency = price
            
            # Add to our database
            add_1 = Adds(img_url=img_url, date_posted=date_posted, currency=currency)
            session.add(add_1)

    session.commit()
    session.close()
        