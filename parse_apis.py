import json
from urllib.parse import urlparse, parse_qsl

# add a tag to the site that does something obvious like an alert that includes a unique string

def parse_gtag_reqs() -> list:
    with open("gtag_requests.json", "r", encoding="utf-8") as f:
        tags = json.loads(f.read())

    print(tags[1])
    
    return tags

def split_url(url):
    parse_result = urlparse(url)
    query = parse_result.query

    return dict(parse_qsl(query))




if __name__ == "__main__":
    tags = parse_gtag_reqs()
    for tag in tags:
        try:
            url = tag["request"]["url"]
            query_dict = split_url(url)
            print(query_dict)
        except Exception:
            pass