[![PyPI version](https://badge.fury.io/py/augtxt.svg)](https://badge.fury.io/py/augtxt)
[![DOI](https://zenodo.org/badge/315031055.svg)](https://zenodo.org/badge/latestdoi/315031055)

# augtxt -- Text Augmentation
Yet another text augmentation python package.

## Table of Contents
* Usage
    * [`augtxt.augmenters` - Pipelines](#pipelines)
    * [`augtxt.typo` - Typographical Errors](#typographical-errors-tippfehler)
    * [`augtxt.wordsubs` - Word substitutions](#word-substitutions)
* Appendix
    * [Installation](#installation)
    * [Commands](#commands)
    * [Support](#support)
    * [Contributing](#contributing)


# Usage

```py
import augtxt
import numpy as np
```


## Pipelines

### Word Augmentation 
The function `augtxt.augmenters.wordaug` applies randomly different augmentations to one word.

```py
from augtxt.augmenters import wordaug
import augtxt.keyboard_layouts as kbl
import numpy as np
from collections import Counter

settings = [
    {
        'p': 0.04,
        'fn': 'typo.drop_n_next_twice',
        'args': {'loc': ['m', 'e'], 'keep_case': True}
    },
    {
        'p': 0.04,
        'fn': 'typo.swap_consecutive',
        'args': {'loc': ['m', 'e'], 'keep_case': True}
    },
    {
        'p': 0.02,
        'fn': 'typo.pressed_twice',
        'args': {'loc': 'u', 'keep_case': True}
    },
    {
        'p': 0.02,
        'fn': 'typo.drop_char',
        'args': {'loc': ['m', 'e'], 'keep_case': True}
    },
    {
        'p': 0.02,
        'fn': 'typo.pressed_shiftalt',
        'args': {'loc': ['b', 'm'], 'keymap': kbl.macbook_us, 'trans': kbl.keyboard_transprob}
    },
]

np.random.seed(seed=42)
word = "Blume"
newwords = []
for i in range(1000):
    newwords.append( wordaug(word, settings) )

Counter(newwords)
```



## Typographical Errors (Tippfehler)
The `augtxt.typo` module is about augmenting characters to mimic human errors while using a keyboard device.


### Swap two consecutive characters (Vertauscher)
A user mix two consecutive characters up.

- Swap 1st and 2nd characters: `augtxt.typo.swap_consecutive("Kinder", loc=0)`  (Result: `iKnder`)
- Swap 1st and 2nd characters, and enforce letter cases: `augtxt.typo.swap_consecutive("Kinder", loc=0, keep_case=True)`  (Result: `Iknder`)
- Swap random `i`-th and `i+1`-th characters that are more likely at the end of the word: `np.random.seed(seed=123); augtxt.typo.swap_consecutive("Kinder", loc='end')`

### Add double letter (Einfüger)
User presses a key twice accidentaly

- Make 5th letter a double letter: ``augtxt.typo.pressed_twice("Eltern", loc=4)`  (Result: `Elterrn`)


### Drop character (Auslasser)
User presses the key not enough (Lisbach, 2011, p.72), the key is broken, finger motion fails.

- Drop the 3rd letter: `augtxt.typo.drop_char("Straße", loc=2)` (Result: `Staße`)


### Drop character followed by double letter (Vertipper)
Letter is left out, but the following letter is typed twice.
It's a combination of `augtxt.typo.pressed_twice` and `augtxt.typo.drop_char`.

```py
from augtxt.typo import drop_n_next_twice
augm = drop_n_next_twice("Tante", loc=2)
# Tatte
```


### Pressed SHIFT, ALT, or SHIFT+ALT
Usually `SHFIT` is used to type a capital letter, and `ALT` or `ALT+SHIFT` for less common characters. 
A typo might occur because these special keys are nor are not pressed in combination with a normal key.
The function `augtxt.typo.pressed_shiftalt` such errors randomly.

```py
from augtxt.typo import pressed_shiftalt
augm = pressed_shiftalt("Onkel", loc=2)
# OnKel, On˚el, Onel
```

The `keymap` can differ depending on the language and the keyboard layout.

```py
from augtxt.typo import pressed_shiftalt
import augtxt.keyboard_layouts as kbl
augm = pressed_shiftalt("Onkel", loc=2, keymap=kbl.macbook_us)
# OnKel, On˚el, Onel
```

Further, transition probabilities in case of a typo can be specified

```py
from augtxt.typo import pressed_shiftalt
import augtxt.keyboard_layouts as kbl

keyboard_transprob = {
    "keys": [.0, .75, .2, .05],
    "shift": [.9, 0, .05, .05],
    "alt": [.9, .05, .0, .05],
    "shift+alt": [.3, .35, .35, .0]
}

augm = pressed_shiftalt("Onkel", loc=2, keymap=kbl.macbook_us, trans=keyboard_transprob)
```


## Word substitutions
The `augtxt.wordsubs` module is about replacing specific strings, e.g. words, morphemes, named entities, abbreviations, etc.


### Pseudo-synonyms from pretrained word embedding
The **semantic similarity** between two words can be measured with a similarity metric (e.g. jaccard score, cosine similarity) between the corresponding **word vectors** from pretrained **word embeddings** (e.g. word2vec, GloVe, and fastText).

Furthermore, we compute the character-level (non-semantically) k-shingle based jaccard similarity to exclude **near duplicates**, or resp. to favor *semantic similar words with a different spelling*.


#### fastText
(1) Download a language-specifc pretrained fastText embedding, e.g. 

```sh
augtxt_downloader.py --fasttext --lang=de
```

(2) Tokenize the whole corpus, and create a list of unique words, e.g. 

```py
import itertools
token_seqs = [["Das", "ist", "ein", "Satz", "."], ["Dies", "ist", "ein", "anderer", "Satz", "."]]
vocab = set(itertools.chain(*token_seqs))
# {'anderer', 'Satz', '.', 'Das', 'ein', 'Dies', 'ist'}
```

(3) Lookup up synonyms. Make sure that the `lang` parameter corresponds to the `--lang` parameter in step (1).

```py
import augtxt.wordsubs

synonyms = augtxt.wordsubs.pseudo_synonyms_fasttext(
    vocab, lang='de',
    max_neighbors=25, 
    min_vector_score=0.65,  # Jaccard similarity btw. fastText vectors
    max_shingle_score=0.35,  # Jaccard similarity btw. k-shingles
    kmax=8,  # the k in k-shingle
    n_max_wildcards=1  # number of wildcards in each shingle
)
```

We prefer the term **pseudo-synonyms** because the results can be considered to be **inaccurate**. For example, `#einleitungssatz` was identified as similar to the token `satz`. It contains a hashtag `#` what can be considered as **inaccurate**.

```py
{
    'anderer': ['verschiedener', 'einiger', 'vieler', 'diverser', 'sonstiger', 
                'etlicher', 'einzelner', 'bestimmter', 'ähnlicher'], 
    'satz': ['sätze', 'anfangssatz', 'schlussatz', 'eingangssatz', 'einleitungssatzes', 
             'einleitungsssatz', 'einleitungssatz', 'behauptungssatz', 'beispielsatz', 
             'schlusssatz', 'anfangssatzes', 'einzelsatz', '#einleitungssatz', 
             'minimalsatz', 'inhaltssatz', 'aufforderungssatz', 'ausgangssatz'], 
    '.': [',', '🎅'], 
    'das': ['welches', 'solches'], 
    'ein': ['weiteres'], 
    'dies': ['was', 'umstand', 'dass']
}
```

The function `augtxt.wordsubs.pseudo_synonyms_fasttext` stores all pseudo-synonyms inside a buffer file on your HDD in the background. In order to call this buffer file directly, and to avoid preprocessing with fastText again, you can use the following function:

```py
import itertools
import augtxt.wordsubs
token_seqs = [["Das", "ist", "ein", "Satz", "."], ["Dies", "ist", "ein", "anderer", "Satz", "."]]
vocab = set(itertools.chain(*token_seqs))
synonyms = augtxt.wordsubs.lookup_buffer_fasttext(vocab, lang='de')
```

**Please note**: When using the function `augtxt.wordsubs.pseudo_synonyms_fasttext` with [fastText pretrained models](https://fasttext.cc/docs/en/pretrained-vectors.html), then (1) you have to cite [Bojanowski et. al. (2017)](https://arxiv.org/abs/1607.04606), and (2) the subsequently derived data, e.g. the augmented examples, fall under the [CC BY-SA 3.0 license](https://fasttext.cc/docs/en/pretrained-vectors.html#license).


### Using pseudo-synonym dictionaries to augment tokenized sequences
It is recommend to filter `vocab` further. For example, PoS tag the sequences and only augment VERB and NOUN tokens.

```py
import itertools
import augtxt.wordsubs
import numpy as np

original_seqs = [["Das", "ist", "ein", "Satz", "."], ["Dies", "ist", "ein", "anderer", "Satz", "."]]
vocab = set([s.lower() for s in itertools.chain(*original_seqs) if len(s) > 1])

synonyms = augtxt.wordsubs.lookup_buffer_fasttext(
    vocab, lang='de')

np.random.seed(42)
augmented_seqs = augtxt.wordsubs.synonym_replacement(
    original_seqs, synonyms, num_augm=10, keep_case=True)

# check results for 1st sentence
for s in augmented_seqs[0]:
    print(s)
```



## References
- Lisbach, B., 2011. Linguistisches Identity Matching. Vieweg+Teubner, Wiesbaden. https://doi.org/10.1007/978-3-8348-9791-6
- Bojanowski, P., Grave, E., Joulin, A., Mikolov, T., 2017. Enriching Word Vectors with Subword Information. arXiv:1607.04606 [cs].


# Appendix

## Installation
The `augtxt` [git repo](http://github.com/ulf1/augtxt) is available as [PyPi package](https://pypi.org/project/augtxt)

```sh
pip install augtxt>=0.2.0
pip install git+ssh://git@github.com/ulf1/augtxt.git
```


## Commands
Install a virtual environment

```
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

Python commands

* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `pytest`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`

Clean up 

```
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```

## Support
Please [open an issue](https://github.com/ulf1/augtxt/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/augtxt/compare/).
