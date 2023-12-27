import json
from urllib.parse import urlparse, parse_qsl

def parse_gtag_reqs() -> list:
    with open("gtag_requests.json", "r", encoding="utf-8") as f:
        tags = json.loads(f.read())
    
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