#!/usr/bin/env python3
import urllib
import feedparser

MAX_RESULTS = 10000 # For the purpose of my test task it's 10000, change it if needed
BATCH_SIZE = 100 # Should be a divisor of MAX_RESULTS

if __name__ == "__main__":
    
    one_more_query = True
    
    while one_more_query:
        print("Search arxiv.org trends for (type your query below):", end='\n')
        search_query = input().strip()

        titles = []

        for batch_num in range(MAX_RESULTS // BATCH_SIZE):
            url = "http://export.arxiv.org/api/query?search_query={0}&start={1}&max_results={2}".format(
                search_query,
                BATCH_SIZE * batch_num,
                BATCH_SIZE).replace(" ", "+")

            print(url)
            try:
                data = urllib.request.urlopen(url).read()
            except urllib.error.URLERROR as e:
                print("Sorry, something is wrong with the url ", url)
                print("The following error occurred:")
                print(e.reason)
                titles = []
                break
            
            parsed = feedparser.parse(data)

            if not parsed.entries:
                break
            
            for entry in parsed.entries:
                titles.append(entry.title)
        

        if titles:
            print(titles, end="\n\n")
        else:
            print("Sorry, your search didn't give any results", end="\n\n")

        print("One more query? (y/n)")
        if input() != "y":
            one_more_query = False
