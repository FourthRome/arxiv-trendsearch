#!/usr/bin/env python3
import urllib
import feedparser
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

MAX_RESULTS = 100 # For the purpose of my test task it's 10000, change it if needed
BATCH_SIZE = 100 # Should be a divisor of MAX_RESULTS
SPLIT_REGEX = r"(?:-{2,}|[^a-zA-Z\-])+" # Regex used to split titles into words
STOPWORDS = set(stopwords.words("english"))



if __name__ == "__main__":
    tokenizer = RegexpTokenizer(SPLIT_REGEX, gaps=True)
