from apiclient.discovery import build

with open("./app_utils/api_key", "r") as key_file:
    api_key = key_file.read().strip()

resource = build("customsearch", "v1", developerKey=api_key).cse()


def get_googlesearch(query):
    result = resource.list(q=query, cx="016235836115943068962:dgg3iorp2y3").execute()
    items = []
    for item in result["items"][0:4]:
        items.append({"title": item["title"], "link": item["link"]})
    return items


if __name__ == '__main__':
    print(get_googlesearch("python"))

