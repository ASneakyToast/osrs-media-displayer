import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# find specific element by id
results_container = soup.find( id="ResultsContainer" )
print( results_container.prettify() )

# find elements by class name
job_elements = results_container.find_all( "div", class_="card-content" )
for job_element in job_elements:
  title_element = job_element.find( "h2", class_="title" )
  company_element = job_element.find( "h3", class_="company" )
  location_element = job_element.find( "p", class_="location" )
  print( title_element.text.strip() ) # .text specifies element value
  print( company_element.text.strip() ) # .srip() removes extra whitespace
  print( location_element.text.strip() )
  print()
