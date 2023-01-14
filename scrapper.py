import requests
from bs4 import BeautifulSoup

URL = 'https://bananarepublic.gapcanada.ca/browse/category.do?cid=26219&nav=meganav%3AMen%3ALAST%20CHANCE%20SALE%3Amen%27s%20sale#department=75'
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="faceted-grid")

print(results.prettify())

