import urllib.request
import feedparser

url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=10'
data = urllib.request.urlopen(url).read()
parsed = feedparser.parse(data)

for entry in parsed["entries"]:
    print("-", entry["title"])