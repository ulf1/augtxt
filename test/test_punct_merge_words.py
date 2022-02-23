from augtxt.punct import merge_words
import numpy as np


def test1():
    np.random.seed(seed=1)
    text = "Die Bindestrich-Wörter sind da."
    augmented = merge_words(text)
    assert augmented == 'Die Bindestrichwörter sind da.'


def test2():
    np.random.seed(seed=1)
    text = ""
    augmented = merge_words(text)
    assert augmented == ''
