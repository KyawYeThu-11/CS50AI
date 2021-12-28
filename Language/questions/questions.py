import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_contents = dict()
    for file in os.listdir(directory):
        fhand = open(os.path.join(directory, file), encoding='utf-8')
        content = fhand.read()
        file_contents[file] = content
    
    return file_contents

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = list()
    for word in nltk.word_tokenize(document.lower()):
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            words.append(word)

    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    appearance = dict()

    for doc in documents:
        unique_words = set(word for word in documents[doc])
        for word in unique_words:
            appearance[word] = appearance[word] + 1 if word in appearance else 1

    return {
        word:math.log(len(documents)/appearance[word])
        for word in appearance
    }
        
                

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranks = dict()
    for file, words in files.items():
        tf_idf = 0
        for query_word in query:
            tf_idf += words.count(query_word) * idfs[query_word]
        ranks[file] = tf_idf

    ranked_files = sorted(ranks, key=lambda file:ranks[file], reverse=True)

    return ranked_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = dict()

    for sentence, words in sentences.items():
        mwm = 0
        appearance = 0
        for query_word in query:
            if query_word in words:
                mwm += idfs[query_word]
                appearance += 1

        ranks[sentence] = (mwm, appearance/len(words))


    ranked_sentences = sorted(ranks, key=lambda sentence:ranks[sentence], reverse=True)
    return ranked_sentences[:n]

if __name__ == "__main__":
    main()
