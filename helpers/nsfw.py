"""

NSFW gifs

All the rights belong to the sub-reddit and the posts' respective OP / website owner or uploader

https://www.reddit.com/r/nsfw/
https://porngifs.xxx/

"""

# Libs
import requests,random,json
from bs4 import BeautifulSoup

# Vars
URL = "https://porngifs.xxx/"
REDDIT_URLS = ["https://www.reddit.com/r/nsfw/new.json",
"https://www.reddit.com/r/sexygirls/new.json","https://www.reddit.com/r/Nudes/new.json"
"https://www.reddit.com/r/Gonewild18/new.json","https://www.reddit.com/r/camwhores/new.json"
"https://www.reddit.com/r/gonewild/new.json"]
HEADERS = {"User-Agent":"Mozilla/5.0"}


# Get a random gif
def get_gif():
    site = requests.get(URL,timeout=10)
    soup = BeautifulSoup(site.content, "html.parser")
    img = soup.find_all("img", {"class": ["image","gifplay","lazy-loaded"]})
    img = random.choice(img)
    gif = img["data-gif"]
    return gif


# Get a random nsfw image from reddit
def get_nsfw():
    ALLOWED = [".jpg",".png",".gif"]
    site = requests.get(random.choice(REDDIT_URLS),timeout=100,headers=HEADERS)
    print(site.headers)
    # Status check
    data = json.loads(site.text)
    post = random.choice(data["data"]["children"])
    # Error handling
    try:
        image = post["data"]["url_overridden_by_dest"]
        if image[-4:] not in ALLOWED:
            return get_nsfw()
        else:
            return image
    except:
        return get_nsfw()

FUNCTIONS = [get_gif,get_nsfw]
