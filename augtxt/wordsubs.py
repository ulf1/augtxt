from typing import Optional, List, Dict
from pathlib import Path
import os
import json
import fasttext
import kshingle as ks
import gc


# default settings
PATH_BUFFER = f"{str(Path.home())}/augtxt_data/fasttext-buffer"
PATH_FASTTEXT = f"{str(Path.home())}/augtxt_data/fasttext"


def lookup_synonyms_fasttext(words: List[str], lang: str,
                             max_neighbors: Optional[int] = 100,
                             min_vector_score: Optional[float] = 0.65,
                             max_shingle_score: Optional[float] = 0.35,
                             kmax: Optional[int] = 8,
                             n_max_wildcards: Optional[int] = None,
                             path_buffer: Optional[str] = PATH_BUFFER,
                             path_fasttext: Optional[str] = PATH_FASTTEXT
                             ) -> Dict[str, List[str]]:
    """Lookup synonyms for a given list of words
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
    model = fasttext.load_model(
        os.path.join(path_fasttext, f"wiki.{lang}.bin"))

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
