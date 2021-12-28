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
    pages = {page for page in corpus}
    linked_pages = corpus[page] if corpus[page] != set() else pages
    output = dict()

    # probability of a page linked by links & linked by being randomly chosen
    proba_by_link = damping_factor/len(linked_pages) 
    proba_by_random = (1- damping_factor)/len(corpus)

    for key in corpus:
        # every page would have 0.05% probabiility
        output[key] = proba_by_random
        # if the page is linked by the input page
        if key in linked_pages: 
            output[key] += proba_by_link
    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = [page for page in corpus]
    samples = []
    pageranks = dict()

    previous_sample = random.choice(pages)
    for i in range(n):
        transit_model = transition_model(corpus, previous_sample, damping_factor)
        weights = [transit_model[key] for key in transit_model]           
        new_sample = random.choices(pages, weights = weights, k = 1)
        samples.append(new_sample[0])
        previous_sample = new_sample[0]
    
    pagerank_values = [samples.count(page)/n for page in pages]
    
    for i, pagerank_value in enumerate(pagerank_values):
        pageranks[pages[i]] = pagerank_value
    
    return pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = [page for page in corpus]

    # each page has 1/N in the beginning
    pageranks = dict()
    for page in pages:
        pageranks[page] = 1/len(pages)
    
    big_difference = True
    while big_difference:
        updated_pageranks = update_pageranks(corpus, pageranks, damping_factor)    
        
        big_difference = False
        for page in updated_pageranks:
            if abs(updated_pageranks[page] - pageranks[page]) > 0.001:
                big_difference = True
        pageranks = updated_pageranks
    
    return pageranks


def update_pageranks(corpus, initial_pageranks, d):
    """
    Update the pageranks based on the previously updated pageranks
    """
    pageranks = initial_pageranks.copy()
    # update the rank of each page in pageranks
    for current_page in pageranks:
        # get a dictionary of pages that link to the current page
        linked_by_pages = linked_by(corpus, current_page)
        sum = 0
        # for each page that links to the current page
        for linking_page in linked_by_pages:
            sum += initial_pageranks[linking_page] / linked_by_pages[linking_page]
        
        # applying the iterative pagerank equation
        pageranks[current_page] = (1 - d)/ len(initial_pageranks) + d * sum
    
    return pageranks


def linked_by(corpus, page):
    """
    Given the corpus and a page thereof, return pages that link to that particular page
    in question alongside number in links in those pages in the form of dictionary
    """
    linked_by = dict()

    for key in corpus:
        if corpus[key] == set():
            linked_by[key] = len(corpus)
        if page in corpus[key]:
            linked_by[key] = len(corpus[key])

    return linked_by

if __name__ == "__main__":
    main()

# from pagerank import transition_model, sample_pagerank
# corpus1 = {'1.html': {'2.html'}, '2.html': {'3.html', '1.html'}, '3.html': {'4.html', '2.html'}, '4.html': {'2.html'}}
# corpus2 = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
# transition_model(corpus2, "1.html", 0.85)