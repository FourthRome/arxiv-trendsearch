#!/usr/bin/env python3

"""
"""

from sys import exit
import urllib
import feedparser
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# MAX_RESULTS defines amount of search results taken into account.
MAX_RESULTS = 100
# BATCH_SIZE should be a divisor of MAX_RESULTS.
BATCH_SIZE = 100
# SPLIT_REGEXP sets the regexp for separators between the words in titles
SPLIT_REGEXP = r"(?:-{2,}|[^a-zA-Z\-])+"
# STOPWORDS are words to be omitted from the search result.
# I'm not sure if I should put the initializing code somewhere else,
# thus preventing execution of this line if this script is (somehow)
# included into another project. Please let me know if you have any 
# ideas on this.
STOPWORDS = set(stopwords.words("english"))


def load_batch(search_query, batch_number):
    """Load a batch (i.e. a page) of search results.

    This function returns a string in the Atom 1.0 format (not parsed XML).
    """

    url = "http://export.arxiv.org/api/query?search_query={0}&start={1}&max_results={2}".format(
            search_query,
            BATCH_SIZE * batch_number,
            BATCH_SIZE)
    
    try:
        xml_feed = urllib.request.urlopen(url).read()
    except urllib.error.URLERROR as e:
        print("Sorry, something is wrong with the url {0}".format(url))
        print("The following error occurred: {0}".format(e.reason))
        exit(1)
    
    return xml_feed


def update_word_amounts(word_amounts, parsed_batch, tokenizer=RegexpTokenizer(SPLIT_REGEXP, gaps=True)):
    """Update information about amount of words.

    'tokenizer' is set by default so that RegexpTokenizer is only 
    created once. With SPLIT_REGEXP and gaps=True we show the tokenizer 
    string patterns that act like fillers between words."""
    for entry in parsed_batch.entries:
        decade = int(entry.published[:4])
        decade -= decade % 10
        if decade not in word_amounts:
            word_amounts[decade] = dict()
        
        for word in tokenizer.tokenize(entry.title):
            word = word.lower()
            if len(word) > 1 and word not in STOPWORDS:
                if word in word_amounts[decade]:
                    word_amounts[decade][word] += 1
                else:
                    word_amounts[decade][word] = 1


if __name__ == "__main__":
    # Get the search query from console.
    print("Search arxiv.org trends for:")
    search_query = input().strip().replace(" ", "+")
    print("")

    # word_amounts is a nested dictionary: {decade:{word:count}}, where 
    # 'decade' is an integer, first year of the decade (e.g. 1990 or 
    # 2000), and 'count' is amount of times the 'word' appeared in titles
    # of papers published in that decade.
    word_amounts = dict()

    for batch_number in range(MAX_RESULTS // BATCH_SIZE):
        # Load next batch of Atom feed and parse it.  Check if there are
        # any search results in it.  Recalculate amounts of words for
        # each decade.
        parsed_batch = feedparser.parse(load_batch(search_query, batch_number)) 
        if not parsed_batch.entries:
            break
        update_word_amounts(word_amounts, parsed_batch)
    
    if not word_amounts:
        print("Sorry, your search didn't give any results. Try another one.")
        exit(0)

    for decade in sorted(word_amounts):
        print("The top words among your search results, published in {0}-{1}, are:".format(decade, decade + 9))
        for number, word in enumerate(sorted(word_amounts[decade], key=word_amounts[decade].get, reverse=True)[:10]):
            print("{0:<2} - {1:<30} - occurred {2} times".format(number + 1, word, word_amounts[decade][word]))
        print("")

