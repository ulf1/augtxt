from typing import List
import copy
import numpy as np
import scipy.stats
import augtxt.typo as typo
import re


fn_dict = {
    'typo.swap_consecutive': typo.swap_consecutive,
    'typo.pressed_twice': typo.pressed_twice,
    'typo.drop_char': typo.drop_char,
    'typo.drop_n_next_twice': typo.drop_n_next_twice,
    'typo.pressed_shiftalt': typo.pressed_shiftalt
}


def random_args(cfg_: dict):
    """ randomly pick alternative args """
    cfg = copy.copy(cfg_)
    for k, v in cfg.items():
        if isinstance(v, (list, tuple)):
            j = scipy.stats.randint.rvs(0, len(v))
            cfg[k] = v[j]
    return cfg


def wordaug(original: str, settings: List[dict]) -> str:
    """Apply different augmentation functions to one word

    Parameters:
    -----------
    original : str

    settings : List[dict]

    Return:
    -------
    str
        The augmented variant of the input word

    Example:
    --------
        from augtxt.augmenters import wordaug
        from collections import Counter
        import numpy as np
        np.random.seed(seed=42)

        settings = [
            {'p': 0.04, 'fn': 'typo.drop_n_next_twice',
             'args': {'loc': ['m', 'e'], 'keep_case': True}},
            {'p': 0.04, 'fn': 'typo.swap_consecutive',
             'args': {'loc': ['m', 'e'], 'keep_case': True}}]

        tokenseq = ["Dies", "ist", "ein", "Satz", "."]

        n_trials = 1000
        results = [' '.join([wordaug(word, settings) for word in tokenseq])
                   for _ in range(n_trials)]

        Counter(results)
    """
    result = copy.copy(original)
    # loop over all augmentation methods in random order
    for i in np.random.permutation(len(settings)):
        # apply augmentation with a given probability
        if settings[i]['p'] >= scipy.stats.uniform.rvs():
            # read fn args and randomly pick alternative args
            cfg = random_args(settings[i]['args'])
            # augment the word
            result = fn_dict[settings[i]['fn']](result, **cfg)
    # next
    return result


def sentaug(original: str,
            settings: List[dict],
            exclude: List[str] = None,
            num_augmentations: int = 1,
            pmax: float = 0.1) -> List[str]:
    """ Apply different augmentation functions to at least one word or up
          a certain percentage of words in a sentence

    Parameters:
    -----------
    original : str
        The original sentence as string. If a List[str] it is assumed to be
          pretokenized.

    settings : List[dict]

    exclude : List[str]
        List of strings that are excluded from augmentation

    num_augmentations : int (default: 1)
        Number of augmentations to generate

    pmax : float (default 0.1)
        The maximum percentage of words per sentence to augment

    Return:
    -------
    List[str]
        The augmented variant of the input sentence

    Example:
    --------
        from augtxt.augmenters import sentaug
        import numpy as np
        np.random.seed(seed=42)

        settings = [
            {'weight': 1, 'fn': 'typo.drop_n_next_twice',
             'args': {'loc': ['m', 'e'], 'keep_case': True}},
            {'weight': 1, 'fn': 'typo.swap_consecutive',
             'args': {'loc': ['m', 'e'], 'keep_case': True}}]

        exclude = ["[MASK]", "[UNK]"]

        orginal = 'Die Lehrerin [MASK] einen Roman.'

        augm = sentaug(original, settings=settings, exclude=exclude, 2, 0.1)
    """
    # tokenization
    # if isinstance(original, str):
    token = [t for t in re.split('[ .,;:!?]', original) if len(t) > 0]
    # elif isinstance(original, (tuple, list)):
    #     token = original
    # else:
    #     raise Exception(f"type(orginal)={type(original)} is not supported")

    # if len(token) == 0:
    #     return []

    # number of words to augment
    num_aug = max(int(len(token) * pmax), 1)

    # which tokens are not excluded?
    if exclude is None:
        exclude = []
    indicies = np.where([t not in exclude for t in token])[0]

    if len(indicies) == 0:
        return []

    # extract settings for shuffling
    fns = [item.get("fn") for item in settings]
    configs = [item.get("args") for item in settings]
    weights = np.array([item.get("weight") for item in settings])
    p = weights / weights.sum()

    augmentations = []
    for _ in range(num_augmentations):
        augsent = copy.copy(original)
        # draw random tokens
        selected = np.random.choice(indicies, size=num_aug)
        # loop over selected tokens to augment them
        for i in selected:
            # get random augmentation function
            j = np.random.choice(range(len(p)), size=1, replace=False, p=p)[0]
            cfg = random_args(configs[j])
            # augment the choosen token
            augword = fn_dict[fns[j]](token[i], **cfg)
            # replace original word with augmented word
            augsent = augsent.replace(token[i], augword, 1)
        # save augmented sentence
        augmentations.append(augsent)
    # done
    return augmentations
