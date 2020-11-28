from typing import List
import copy
import numpy as np
import scipy.stats
import augtxt.typo as typo


fn_dict = {
    'typo.drop_n_next_twice': typo.drop_n_next_twice,
    'typo.swap_consecutive': typo.swap_consecutive,
    'typo.pressed_twice': typo.pressed_twice,
    'typo.drop_char': typo.drop_char,
    'typo.pressed_shiftalt': typo.pressed_shiftalt,
}


def wordaug(original: str, settings: List[dict]):
    result = copy.copy(original)
    # loop over all augmentation methods in random order
    for i in np.random.permutation(len(settings)):
        # apply augmentation with a given probability
        if settings[i]['p'] >= scipy.stats.uniform.rvs():
            # read fn args and randomly pick alternative args
            cfg = copy.copy(settings[i]['args'])
            for k, v in cfg.items():
                if isinstance(v, (list, tuple)):
                    j = scipy.stats.randint.rvs(0, len(v))
                    cfg[k] = v[j]
            # augment the word
            result = fn_dict[settings[i]['fn']](result, **cfg)
    # next
    return result
