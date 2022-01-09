from typing import List
import copy
import numpy as np
import scipy.stats
import augtxt.typo
import augtxt.order
import augtxt.punct
import re


fn_dict = {
    'typo.swap_consecutive': augtxt.typo.swap_consecutive,
    'typo.pressed_twice': augtxt.typo.pressed_twice,
    'typo.drop_char': augtxt.typo.drop_char,
    'typo.drop_n_next_twice': augtxt.typo.drop_n_next_twice,
    'typo.pressed_shiftalt': augtxt.typo.pressed_shiftalt,
}


def random_args(cfg_: dict):
    """ randomly pick alternative args """
    cfg = copy.copy(cfg_)
    for k, v in cfg.items():
        if isinstance(v, (list, tuple)):
            j = scipy.stats.randint.rvs(0, len(v))
            cfg[k] = v[j]
    return cfg


def wordtypo(original: str, settings: List[dict]) -> str:
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
        from augtxt.augmenters import wordtypo
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
        results = [' '.join([wordtypo(word, settings) for word in tokenseq])
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


def senttypo(original: str,
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
        from augtxt.augmenters import senttypo
        import numpy as np
        np.random.seed(seed=42)

        settings = [
            {'weight': 1, 'fn': 'typo.drop_n_next_twice',
             'args': {'loc': ['m', 'e'], 'keep_case': True}},
            {'weight': 1, 'fn': 'typo.swap_consecutive',
             'args': {'loc': ['m', 'e'], 'keep_case': True}}]

        exclude = ["[MASK]", "[UNK]"]

        orginal = 'Die Lehrerin [MASK] einen Roman.'

        augm = senttypo(original, settings=settings, exclude=exclude, 2, 0.1)
    """
    # tokenization
    token = [t for t in re.split('[ .,;:!?]', original) if len(t) > 0]

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


fn_dict2 = {
    'order.swap_consecutive': augtxt.order.swap_consecutive,
    'order.drop_word': augtxt.order.drop_word,
    'order.write_twice': augtxt.order.write_twice,
    'order.drop_n_next_twice': augtxt.order.drop_n_next_twice
}


def sentaugm(sentence, settings, exclude=["[MASK]"]):
    """

    Example:
    --------
    from augtxt.augmenters import sentaugm
    import augtxt.keyboard_layouts as kbl
    import numpy as np

    typo_settings = [
        {'weight': 2, 'fn': 'typo.drop_n_next_twice',
        'args': {'loc': 'u', 'keep_case': True}},
        {'weight': 2, 'fn': 'typo.swap_consecutive',
        'args': {'loc': 'u', 'keep_case': True}},
        {'weight': 1, 'fn': 'typo.pressed_twice',
        'args': {'loc': 'u', 'keep_case': True}},
        {'weight': 1, 'fn': 'typo.drop_char',
        'args': {'loc': 'u', 'keep_case': True}},
        {'weight': 1, 'fn': 'typo.pressed_shiftalt',
        'args': {'loc': ['b', 'm']}, 'keymap': kbl.qwertz_de}
    ]

    order_settings = [
        {'weight': 3, 'fn': 'order.swap_consecutive'},
        {'weight': 2, 'fn': 'order.drop_word'},
        {'weight': 1, 'fn': 'order.write_twice'},
        {'weight': 1, 'fn': 'order.drop_n_next_twice'},
    ]

    settings = {
        "typo": {"num_augmentations": 6,
                 "settings": typo_settings, "pmax": 0.1},
        "punct": {"num_augmentations": 3},
        "order": {"num_augmentations": 6, "settings": order_settings}
    }

    np.random.seed(seed=42)
    exclude = ["[MASK]", "[UNK]"]
    sentence = 'Die Lehrerin [MASK] einen Roman.'
    augs = sentaugm(sentence, settings, exclude)
    """
    augs = []
    req_num = sum([v.get("num_augmentations") for _, v in settings.items()])
    for _ in range(2):
        # typographical errors
        if settings.get("typo"):
            augs.extend(augtxt.augmenters.senttypo(
                sentence, exclude=exclude, **settings.get("typo")))

        # interpunctation errors
        if settings.get("punct"):
            cfg = settings.get("punct")
            if cfg.get("num_augmentations", 0) > 0:
                augs.append(augtxt.punct.remove_syntaxinfo(sentence))
            if cfg.get("num_augmentations", 0) > 1:
                for _ in range(1, cfg.get("num_augmentations", 0)):
                    augs.append(augtxt.punct.merge_words(sentence, num_aug=1))

        # word order errors
        if settings.get("order"):
            cfg = settings.get("order")
            weights = np.array([item.get('weight') for item
                                in cfg.get("settings")])
            p = weights / weights.sum()
            idx = np.random.choice(range(len(p)),
                                   size=cfg.get("num_augmentations"),
                                   replace=True, p=p)
            for i in idx:
                fname = cfg.get("settings")[i].get('fn')
                augs.append(fn_dict2[fname](
                    sentence, exclude=exclude, num_aug=1))
        # done?
        if len(set(augs)) >= req_num:
            break
    # filter duplicates
    augs = list(set(augs))
    # chop excess
    return augs[:req_num]
