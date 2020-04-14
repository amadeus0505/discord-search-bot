from apiclient.discovery import build

try:
    with open("./app_utils/api_key", "r") as key_file:
        api_key = key_file.read().strip()
except FileNotFoundError:
    print("You have to create a file named 'api_key' in ./app_utils/, which contains your google custom search api key")
    exit(0)

resource = build("customsearch", "v1", developerKey=api_key).cse()


def get_googlesearch(query):
    result = resource.list(q=query, cx="016235836115943068962:dgg3iorp2y3").execute()
    items = []
    for item in result["items"][0:4]:
        items.append({"title": item["title"], "link": item["link"]})
    return items


if __name__ == '__main__':
    print(get_googlesearch("python"))

