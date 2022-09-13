"""

NSFW gifs for morty

"""

# Libs
import requests
import random
from bs4 import BeautifulSoup

# Vars
URL = "https://porngifs.xxx/"

# Get a random gif
def get_gif():
  site = requests.get(URL,timeout=10)
  soup = BeautifulSoup(site.content, "html.parser")
  img = soup.find_all("img", {"class": ["image","gifplay","lazy-loaded"]})
  img = random.choice(img)
  gif = img["data-gif"]
  return gif
