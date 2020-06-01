import csv
import os
import pprint
import re

from nltk.stem import WordNetLemmatizer
from nltk import tokenize
from pycorenlp import *
import spacy
import neuralcoref
from typing import List

pp = pprint.PrettyPrinter(indent=4)
nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)
nlp_server = StanfordCoreNLP("http://34.87.20.130:9000/")


def neuralcorefIt(text):
    sentences = tokenize.sent_tokenize(text)
    sentences[0] = sentences[0].capitalize()
    for s in sentences:
        if s[-1] == '?':
            sentences.remove(s)
    doc = nlp(text)
    doc._.coref_clusters
    return doc._.coref_resolved


# Get present tense of verbs in triples using WordNetLemmatizer
def lemma(triples):
    lmtzr = WordNetLemmatizer()
    for t in range(0, len(triples)):
        for i in range(0, len(triples[t])):
            for word in triples[t][i].split(" "):
                triples[t][i] = triples[t][i].replace(word, lmtzr.lemmatize(word, 'v'))
    return triples


# Produce the triples for an article using StanfordCoreNLP and return the result
def gen_triple(text: str) -> List[List[str]]:
    triples = []
    processedText = neuralcorefIt(text)
    output = nlp_server.annotate(processedText,
                                 properties={"annotators": "tokenize,ssplit,pos,lemma,depparse,natlog,openie,dcoref",
                                             "outputFormat": "json",
                                             "triple.strict": "true"})  # , "openie.max_entailments_per_clause":"1"})

    result2 = []

    result = [output["sentences"][0]["openie"] for item in output]
    for i in range(0, len(output["sentences"])):
        result2.append(output['sentences'][i]['openie'])
    for i in range(0, len(result2)):
        for rel in result2[i]:
            subj = rel['subject']
            obj = rel['object']
            for ref in output['corefs']:
                if len(output['corefs'][ref]) > 1 and output['corefs'][ref][1]['position'][0] == i + 1:
                    if output['corefs'][ref][1]['text'] == subj:
                        subj = output['corefs'][ref][0]['text']

            relationSent = [subj, obj, rel['relation']]
            triples.append(relationSent)
    triples = lemma(triples)
    return triples
