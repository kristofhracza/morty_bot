# GIF REQUEST FEATURE

# Libs
import requests
import random
from bs4 import BeautifulSoup

# Vars
URL = "https://tenor.com/"

def get_gif(q):
  Q_URL = f"https://tenor.com/search/{q}-gifs"
  # Get a random gif
  site = requests.get(Q_URL,timeout=10)
  soup = BeautifulSoup(site.content, "html.parser")
  img = soup.find_all("div", {"class": "Gif"})
  elem = img[random.randrange(0,len(img))].find("img")
  gif = elem["src"]
  return gif
