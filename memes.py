"""

Memes from reddit

All the rights belong to the sub-reddit and the posts' respective OP

https://www.reddit.com/r/memes/

"""

# Libs
import requests,random,json

URL="https://www.reddit.com/r/memes/new.json"
HEADERS = {"User-Agent":"Mozilla/5.0"}

# Get a random meme
def get_meme():
    site = requests.get(URL,timeout=10,headers=HEADERS)
    data = json.loads(site.text)
    post = random.choice(data["data"]["children"])
    try:
        image = post["data"]["url_overridden_by_dest"]
    except:
        get_meme()
    return image