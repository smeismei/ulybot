# set the apikey and limit
import json
import requests
from config import TENORTOKEN


def random_gif(search_term):
    apikey = TENORTOKEN  # click to set to your apikey
    lmt = 1
    ckey = "ulys"  # set the client_key for the integration and use the same value for all API calls

    # get the top 8 GIFs for the search term
    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s&random=true"
        % (search_term, apikey, ckey, lmt)
    )

    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        top_8gifs = json.loads(r.content)
        # print(json.dumps(top_8gifs,indent=4))
        url = top_8gifs["results"][0]["itemurl"]
        return url
    else:
        return None
