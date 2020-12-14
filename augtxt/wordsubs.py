from typing import Optional, List, Dict
from pathlib import Path
import os
import json
import fasttext
import kshingle as ks
import gc


# default settings
FASTTEXT_BUFFER = f"{str(Path.home())}/augtxt_data/pseudo_synonyms/fasttext"
FASTTEXT_MODELS = f"{str(Path.home())}/augtxt_data/fasttext"


def pseudo_synonyms_fasttext(words: List[str], lang: str,
                             max_neighbors: Optional[int] = 100,
                             min_vector_score: Optional[float] = 0.65,
                             max_shingle_score: Optional[float] = 0.35,
                             kmax: Optional[int] = 8,
                             n_max_wildcards: Optional[int] = None,
                             path_buffer: Optional[str] = FASTTEXT_BUFFER,
                             path_fasttext: Optional[str] = FASTTEXT_MODELS
                             ) -> Dict[str, List[str]]:
    """Lookup pseudo-synonyms from pretrained fastText embedding for a given
         list of words.

    Parameters:
    -----------
    words: List[str]
        A list of words, or resp. a vocabulary list. Large word lists are
          strongly recommended due to the huge fastText model overhead.

    lang: str
        The fastText language code.
        See https://fasttext.cc/docs/en/pretrained-vectors.html

    max_neighbors: Optional[int] = 100
        The number of neighbors to return from the fastText embedding. It is
          also the maximum number of possible pseudo-synonymns.

    min_vector_score: Optional[float] = 0.65
        The smallest acceptable cosine similarity score between our word
          and nearest neighbor in fastText's embedding

    max_shingle_score: Optional[float] = 0.35
        The highest acceptable jaccard similarity score between the k-shingle
          representation of our word and the found nearest neighbors

    kmax: Optional[int] = 8
        k-shingling parameter k

    n_max_wildcards: Optional[int] = None
        k-shingling parameter for the number of wildcards per shingle

    path_buffer: Optional[str] = FASTTEXT_BUFFER
        The folder where to dump buffered pseudo-synonyms for later usage.
          The default is `$HOME/augtxt_data/pseudo_synonyms/fasttext`

    path_fasttext: Optional[str] = FASTTEXT_MODELS
        The folder where pretrained fastText models are stored.
          The default is `$HOME/augtxt_data/fasttext`
    """
    # create buffer folder if not exist
    os.makedirs(path_buffer, exist_ok=True)

    # load buffer file
    try:
        with open(os.path.join(path_buffer, f"{lang}.json"), 'r') as fp:
            buffer = json.load(fp)
    except Exception:
        buffer = {}

    # load fasttext model
    print("[INFO] It takes several minutes to load a FastText model")
    filepath = os.path.join(path_fasttext, f"wiki.{lang}.bin")
    try:
        model = fasttext.load_model(filepath)
    except Exception:
        raise Exception((
            f"The file '{filepath}' is missing.\n"
            "Make sure that you downloaded the pretrained models, e.g.\n"
            "  augtxt_downloader.py --fasttext --lang=de"))

    # init output variable
    synonyms = {}

    # loop over words
    for word in words:
        # convert to lower case
        word = word.lower()

        # lookup word from buffer
        if word in buffer.keys():
            synonyms[word] = buffer[word]
        else:
            # extract synonyms from fasttext
            results = model.get_nearest_neighbors(word, max_neighbors)
            # compute jaccard similarity based on k-shingles
            results = [
                (ks.jaccard_strings(word, syn, k=kmax), vectorscore, syn)
                for vectorscore, syn in results]
            # filter results
            results = [syn for shinglescore, vectorscore, syn in results
                       if (shinglescore <= max_shingle_score) and (
                           vectorscore >= min_vector_score)]
            # update buffer and save results
            if results:
                buffer[word] = results
                synonyms[word] = results

    # save updated buffer file
    with open(os.path.join(path_buffer, f"{lang}.json"), 'w') as fp:
        json.dump(buffer, fp)

    # clean up explicitly
    del buffer
    del model
    gc.collect()

    # done
    return synonyms


def lookup_buffer_fasttext(words: List[str], lang: str,
                           path_buffer: Optional[str] = FASTTEXT_BUFFER
                           ) -> Dict[str, List[str]]:
    """Lookup pseudo-synonyms from local buffer

    Apply this function if you don't want to call fastText at all
      by calling `pseudo_synonyms_fasttext`
    """
    # load buffer file
    with open(os.path.join(path_buffer, f"{lang}.json"), 'r') as fp:
        buffer = json.load(fp)

    # init output variable
    synonyms = {}

    # loop over words
    for word in words:
        # convert to lower case
        word = word.lower()
        # lookup word from buffer
        if word in buffer.keys():
            synonyms[word] = buffer[word]

    # clean up explicitly
    del buffer
    gc.collect()

    # done
    return synonyms
