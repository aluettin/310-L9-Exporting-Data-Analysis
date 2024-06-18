import requests
from bs4 import BeautifulSoup
import json

def get_soup(url):
  r = requests.get(url)
  r.raise_for_status()
  html = r.text.encode("utf-8")
  soup = BeautifulSoup(html, "html.parser")
  return soup

# First web scraper
def get_categories(url):
  soup = get_soup(url)
  data = {}
  # Select and extract category animals here
  categories = soup.find_all("dl")
  for category in categories: 
    category_name = category.find("dt").get_text()
    category_animals = soup.find_all("a")
    # Add extracted data to data dictionary
    data[category_name] = category_animals
  # Return the data
  return data

# Second web scraper
def get_animal(url):
  soup = get_soup(url)
  table = soup.find("table", {"class": "infobox biota"})
  if not table:
    return "No class found."
  rows = table.find_all("tr")
  for row in rows:
    if "Class:" in row.get_text():
      animal_class = row.find("a").contents[0]
  return animal_class

category_data = get_categories("https://skillcrush.github.io/web-scraping-endangered-species/")

# Combine scrapers
collected_data = []

for category in category_data:
  for animal in category_data[category]:
    animal_href = animal["href"]
    animal_name = animal.contents[0]
    animal_class = get_animal(animal_href)
    if len(animal_name) > 3:
      collected_data.append({
        "Category":category,
        "Animal Name":animal_name,
        "Animal Class":animal_class
      })

# Save data to json file
with open("data.json", "w") as jsonfile:
  json.dump(collected_data, jsonfile)