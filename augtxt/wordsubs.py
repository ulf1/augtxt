from typing import Optional, List, Dict, Union
from pathlib import Path
import os
import json
import fasttext
import kshingle as ks
import gc
import scipy.stats
import copy
import itertools


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


def synonym_replacement(original_seqs: List[List[str]],
                        synonyms: Dict[str, List[str]],
                        num_augm: int,
                        min_repl: Union[int, float] = 1,
                        max_repl: Union[int, float] = 1.0,
                        keep_case: Optional[bool] = False
                        ) -> List[List[List[str]]]:
    """Replace words with synonyms

    original_seqs: List[List[str]],
        A list of tokenized sequences.

    synonyms: Dict[str, List[str]]
        Synonym dictionary

    num_augm: int
        Target number of random augmentations per sequence

    min_repl: Union[int, float] = 1
        Minimum number of replaced words

    max_repl: Union[int, float] = 1.0
        Maximum number of replaced words

    keep_case : bool  (Default False, i.e. never)
        Enforce the original letter cases on the new string.
    """
    augmented_seqs = []
    for seq in original_seqs:
        # save all augmentations of the current sequences in a tmp list
        curaug = []

        # token indicies that are available to augment
        availidx = [i for i, word in enumerate(seq)
                    if word.lower() in synonyms.keys()]
        n_avail = len(availidx)

        if n_avail >= 1:
            # determine the number of words to replace
            n_seqlen = len(seq)

            if isinstance(min_repl, int):
                n_low = max(1, min(n_avail, min_repl))
            elif isinstance(min_repl, float):
                n_low = max(1, min(n_avail, int(n_seqlen * min_repl)))

            if isinstance(max_repl, int):
                n_high = max(n_low, min(n_seqlen, max_repl))
            elif isinstance(max_repl, float):
                n_high = max(n_low, min(n_avail, int(n_seqlen * max_repl)))

            # find all combinations of token indicies that can be replaced
            combos = []
            for num in range(n_low, n_high + 1):
                combos.extend(list(itertools.combinations(availidx, num)))
            n_combos = len(combos)

            if n_combos > 0:
                # Generate augmentations for the current sentence
                for q in range(num_augm):
                    # copy original seqs
                    tmp = copy.copy(seq)
                    # pick the next combination of indicies
                    indices = combos[q % n_combos]
                    # for each augmentable token
                    for i in indices:
                        # memorize if it's a capital letter
                        if keep_case:
                            iscap = seq[i][0].isupper()
                        # get synonyms (Use the orginal sequencen `seq`!)
                        word = seq[i].lower()
                        if word in synonyms.keys():
                            syns = synonyms[word]
                            if syns:  # if there are any synonyms
                                # pick random synonym (And store into `tmp`)
                                j = scipy.stats.randint.rvs(0, len(syns))
                                tmp[i] = syns[j]
                                # transform capital letter
                                if keep_case:
                                    if iscap:
                                        tmp[i] = tmp[i][0].upper() + tmp[i][1:]
                    # save results
                    curaug.append(tmp)

        # save results
        augmented_seqs.append(curaug)

    # done
    return augmented_seqs
