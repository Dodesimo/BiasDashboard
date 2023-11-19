import en_core_web_lg
from datasets import load_dataset
import spacy as sp
import pandas as pd
import random

nlp = en_core_web_lg.load()


def dbIndex(l1):
    # Download each dataset and convert to Pandas dataframe
    targetDataset = load_dataset(l1)
    targetDataset.set_format(type='pandas')
    targetDataset = targetDataset['train'][1:]

    # Base db-index based on implicit bias
    comparisonDataset = load_dataset("henryscheible/implicit_bias")
    comparisonDataset.set_format(type='pandas')
    comparisonDataset = comparisonDataset['train'][1:]
    comparisonDataset = comparisonDataset.drop(['category', 'label'], axis=1)

    # Pick a random entry from the comparison dataset.
    index = random.randrange(0, len(comparisonDataset), 1)

    # Find that entry.
    comparisonEntry = comparisonDataset['sentence'][index]

    # Vectoritze entry.
    vectorizedComparisonEntry = nlp(comparisonEntry)

    # initialitize total cosine similarity
    tcs = 0

    # Go through each target entry
    for entry in targetDataset.columns[0]:
        # Find similariity between each target and the comparison entry
        vecEntry = nlp(entry)
        tcs += vecEntry.similarity(vectorizedComparisonEntry)

    # Raise to inverse power of size
    dbi = tcs ** (1 / len(targetDataset))
    return dbi


def test(l1):
    dbindex =  l1 + 2
