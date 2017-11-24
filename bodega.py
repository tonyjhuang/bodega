import urllib2
from bs4 import BeautifulSoup

URL = 'https://shop.bdgastore.com/collections/new-arrivals?page={}&sort_by=price-ascending'

def ptof(price):
    return float(price.strip('$'))

def format_prod_caption(prod_caption):
    brand = prod_caption.h3.get_text().strip()
    product = prod_caption.h4.get_text().strip()
    price = prod_caption.h5.span.get_text()
    if prod_caption.h5.s:
        original_price = prod_caption.h5.s.get_text()
        price += ' ({}% off)'.format((ptof(original_price) - ptof(price)) / ptof(original_price) * 100)
    callout = prod_caption.h5.p.get_text().strip()

    size_list = prod_caption.find('ul', class_='size')
    sizes = None
    if size_list:
        sizes = ','.join(
            [size.get_text().strip() for size in size_list.find_all('li', class_='available')])


    components = [brand, product, price, callout, sizes]
    return ' : '.join([x for x in components if x])


def get_available_items(html):
    soup = BeautifulSoup(html, 'html.parser')
    prod_prices = soup.find_all('h5', class_='prod-price')
    for prod_price in prod_prices:
        if prod_price.p.get_text().strip() != 'Sold Out':
            print format_prod_caption(prod_price.parent)

print '\n\nFINDING CHEAP NON-SOLD OUT ITEMS AT BODEGA'
for i in range(50):
    print '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'page ' + str(i)
    response = urllib2.urlopen(URL.format(i))
    html = response.read()
    get_available_items(html)
