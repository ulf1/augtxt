from typing import Optional, List, Dict, Union
import scipy.stats
import copy
import itertools
import warnings


warnings.warn(
    "`augtxt.wordsubs` will be deleted in 0.6.0 and replaced.",
    DeprecationWarning
)


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
