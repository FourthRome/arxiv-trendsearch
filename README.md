# arxiv-trendsearch

A tool to find top words in arxiv.org's search results (articles' titles are analyzed).

## PREREQUISITES

1. Currently to run this utility you need **Python installed on your machine (version 3.6 or higher)**.

2. You will also need to **install `nltk` and `feedparser` modules**.

3. Finally, **before the first run** of the script you might need to open Python interpreter and **run the following:**

```
import nltk
nltk.download("stopwords")
```

## USAGE

Currently this utility can be run as a Python script only. Simply run **`arxiv-trendsearch.py`**. You will be asked to type your search query for arxiv.org; you can use different prefixes for your query, as described [here](https://arxiv.org/help/api/user-manual#query_details).

The utility will get search results from arxiv.org, 

## TODO

- [ ] **Track down the bug with premature search stop;**
- [ ] Make a distribution with `stopwords` stored locally for availability;
- [ ] Make executables that do not need Python interpreter installed (do we need it?); 
- [ ] Update README and documentation to reflect the stages above.

## CONTACTS

@FourthRome
romansdidnotcrucify@gmail.com