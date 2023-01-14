from requests_html import HTMLSession
from pprint import pprint
from bs4 import BeautifulSoup


session = HTMLSession()
r = session.get('https://bananarepublic.gapcanada.ca/browse/category.do?cid=26219&nav=meganav%3AMen%3ALAST%20CHANCE%20SALE%3Amen%27s%20sale#department=75')
r.html.render()


#for price in price:
#    print(price, end="\n"*2)

#print(results.prettify())

sel = ("#faceted-grid > section > div > div:nth-child(1) > div > div:nth-child(3) > div.product-card-price > div > div")
print(r.html.find(sel, first=True).text)