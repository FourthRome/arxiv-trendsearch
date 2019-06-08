#!/usr/bin/env python3
import urllib
import feedparser
import re
from nltk.corpus import stopwords

MAX_RESULTS = 100 # For the purpose of my test task it's 10000, change it if needed
BATCH_SIZE = 100 # Should be a divisor of MAX_RESULTS
SPLIT_REGEX = re.compile(r"(?:-{2,}|[^a-zA-Z\-])+") # Regex used to split titles into words
STOPWORDS = set(stopwords.words("english"))

if __name__ == "__main__":
    one_more_query = True

    while one_more_query:
        print("Search arxiv.org trends for (type your query below):", end='\n')
        search_query = input().strip().replace(" ", "+")

        words = {}

        for batch_num in range(MAX_RESULTS // BATCH_SIZE):
            url = "http://export.arxiv.org/api/query?search_query={0}&start={1}&max_results={2}".format(
                search_query,
                BATCH_SIZE * batch_num,
                BATCH_SIZE)

            print(url)
            try:
                data = urllib.request.urlopen(url).read()
            except urllib.error.URLERROR as e:
                print("Sorry, something is wrong with the url ", url)
                print("The following error occurred:")
                print(e.reason)
                words = {}
                break
            
            parsed = feedparser.parse(data)

            if not parsed.entries:
                break
            
            for entry in parsed.entries:
                for word in SPLIT_REGEX.split(entry.title):
                    word = word.lower()
                    if len(word) > 1 and word not in STOPWORDS:
                        if word in words:
                            words[word] += 1
                        else:
                            words[word] = 1
        
        if words:
            print("The most trending words in titles of the search result are:")
            for word in sorted(words, key=words.get, reverse=True)[:10]:
                print(word, words[word], end="\n") 
        else:
            print("Sorry, your search didn't give any results", end="\n\n")

        print("One more query? (y/n)")
        if input() != "y":
            one_more_query = False
