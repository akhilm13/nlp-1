from trigram_tagger import SubjectTrigramTagger
from bs4 import BeautifulSoup
import sys
import requests
import re
import pickle
import nltk
from nltk.corpus import stopwords
import mysql.connector
stop = stopwords.words('english')

# Noun Part of Speech Tags used by NLTK

NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
VERBS = ['VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ']
title = ''
def download_document(url):
    """Downloads document using BeautifulSoup, extracts the subject and all
    text stored in paragraph tags
    """
    global title
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('title').get_text()
    document = ' '.join([p.get_text() for p in soup.find_all('p')])
    return document

def clean_document(document):
    """Remove enronious characters. Extra whitespace and stop words"""
    document = re.sub('[^A-Za-z .-]+', ' ', document)
    document = ' '.join(document.split())
    document = ' '.join([i for i in document.split() if i not in stop])
    return document

def tokenize_sentences(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    return sentences

def get_entities(document):
    """Returns Named Entities using NLTK Chunking"""
    entities = []
    sentences = tokenize_sentences(document)

    # Part of Speech Tagging
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                entities.append(' '.join([c[0] for c in chunk]).lower())
    return entities

def word_freq_dist(document):
    """Returns a word count frequency distribution"""
    words = nltk.tokenize.word_tokenize(document)
    words = [word.lower() for word in words if word not in stop]
    fdist = nltk.FreqDist(words)
    return fdist

def extract_subject(document):
    # Get most frequent Nouns
    fdist = word_freq_dist(document)
    most_freq_nouns = [w for w, c in fdist.most_common(10)
                       if nltk.pos_tag([w])[0][1] in NOUNS]

    # Get Top 10 entities
    entities = get_entities(document)
    top_10_entities = [w for w, c in nltk.FreqDist(entities).most_common(10)]

    # Get the subject noun by looking at the intersection of top 10 entities
    # and most frequent nouns. It takes the first element in the list
    subject_nouns = [entity for entity in top_10_entities
                    if entity.split()[0] in most_freq_nouns]
    return subject_nouns

def merge_multi_word_subject(sentences, subject):
    """Merges multi word subjects into one single token
    ex. [('steve', 'NN', ('jobs', 'NN')] -> [('steve jobs', 'NN')]
    """
    if len(subject.split()) == 1:
        return sentences
    subject_lst = subject.split()
    sentences_lower = [[word.lower() for word in sentence]
                        for sentence in sentences]
    for i, sent in enumerate(sentences_lower):
        if subject_lst[0] in sent:
            for j, token in enumerate(sent):
                start = subject_lst[0] == token
                exists = subject_lst == sent[j:j+len(subject_lst)]
                if start and exists:
                    del sentences[i][j+1:j+len(subject_lst)]
                    sentences[i][j] = subject
    return sentences

def put_in_db(link, content, subjects,title = 'No title'):
    # connecting to db
    cnx = mysql.connector.connect(user='user', host='127.0.0.1', password="", database='db', port=3306)
    cursor = cnx.cursor()
    print("select new_article('" + title + "','" + content + "','" + link + "')")
    # querry executing
    cursor.execute("select new_article('" + title + "','" + content + "','" + link + "')")
    # adding the article to db and getting its id
    theid = 0
    for id in cursor:
        theid = id
        idT =  re.findall(r'\d+', str(id))
        print(idT[0])

    # adding the tags to db and getting their ids
    tags = []
    for s in subjects:
        print("select add_tag('" + s + "';")
        cursor.execute("select add_tag('" + s + "')")
        for id in cursor:
            idsT = re.findall(r'\d+', str(id))   
            tags.append(idsT[0])

    # linking in db article with tags
    for i in tags:
        print("call link_article_tag(" + str(idT[0]) + "," + str(i) + ")")
        print(i)
        cursor.execute("call link_article_tag(" + str(idT[0]) + "," + str(i) + ")")
    # THIS IS THE LIST OF TAGS returned
        cnx.commit()
        #cnx.close()

def get_subject(link):


    url = link
#'https://www.usatoday.com/story/news/world/2018/02/19/donald-trump-jr-s-trip-india-could-mix-business-and-u-s-foreign-policy/352127002/'
    document = download_document(url)
    #link is the LINK
    # document = pickle.load(open('document.pkl', 'rb'))
    #This is the title print(title)
    # THIS IS THE ARTICLE print (document)
    document = clean_document(document)
    subjects = extract_subject(document)
    
    

    put_in_db(link, document, subjects,title)

    return subjects

