# NSFW GIFS

# Libs
import requests
import random
from bs4 import BeautifulSoup

# Vars
URL = "http://porngipfy.com/"
URLS = ["http://porngipfy.com/category/lesbian","http://porngipfy.com/?s=ass",
"http://porngipfy.com/category/boobs","http://porngipfy.com/category/anal",
"http://porngipfy.com/tag/butthole","http://porngipfy.com/tag/hardcore/","http://porngipfy.com/",
"http://porngipfy.com/tag/black/","http://porngipfy.com/tag/sex/","http://porngipfy.com/tag/cumshot/",
"http://porngipfy.com/tag/cumshot/"
]

def get_porn():
  # Get a random gif
  r_url = random.choice(URLS)
  site = requests.get(r_url,timeout=10)
  soup = BeautifulSoup(site.content, "html.parser")
  img = soup.find_all("div", {"class": "thumb-image"})
  elem = img[random.randrange(0,len(img))].find("img")
  gif = elem["data-gif"]
  return gif
