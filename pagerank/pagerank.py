import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = dict()
    #copy all keys from corpus to model
    for key in corpus:
        model[key] = (1-damping_factor)/len(corpus)

    #if page has no links, return model
    if len(corpus[page]) == 0:
        for key in model:
            model[key] += damping_factor/len(corpus)
    else:
        for link in corpus[page]:
            model[link] += damping_factor/len(corpus[page])

    total = 0
    for key in model:
        total += model[key]
    if total != 1:
        raise Exception("total is not 1")
    
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visits = dict()
    for key in corpus:
        visits[key] = 0

    page = random.choice(list(corpus.keys()))
    visits[page] += 1
    total = 1
    for i in range(n-1):
        transition = transition_model(corpus, page, damping_factor)
        page = random.choices(list(transition.keys()), list(transition.values()))[0]
        total += 1
        visits[page] += 1

    model = dict()
    for key in corpus:
        model[key] = visits[key]/total

    total = 0
    for key in model:
        total += model[key]
    if total != 1:
        raise Exception("total is not 1")
    return model

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    error = 0.001
    model = dict()
    for key in corpus:
        #set all values to 1/n
        model[key] = 1/len(corpus)
        #if page has no links, link to all pages including itself
        if len(corpus[key]) == 0:
            corpus[key] = list(corpus.keys())
    
    while True:
        #create new model with values from model
        new_model = model.copy()

        #update new model
        for page in model:
            new_model[page] = (1-damping_factor)/len(corpus)
            for key in corpus:
                if page in corpus[key]:
                    new_model[page] += damping_factor*new_model[key]/len(corpus[key])

        #check if new model is close enough to model
        finished = True
        for key in model:
            if abs(new_model[key] - model[key]) > error:
                finished = False
                break

        model = new_model
        
        if finished:
            total = 0
            for key in model:
                total += model[key]
            if total > (1 - error):
                raise Exception("total is not 1")
            return new_model


if __name__ == "__main__":
    main()
