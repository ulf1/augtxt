from augtxt.augmenters import wordtypo
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
        'args': {'loc': ['b', 'm']},
        'keymap': kbl.macbook_us,
        'trans': kbl.keyboard_transprob
    },
]


def test1():
    np.random.seed(seed=42)
    word = "Blume"
    newwords = []
    for i in range(100):
        newwords.append(wordtypo(word, settings))
    assert list(dict(Counter(newwords)).keys()) == [
        'Blume', 'Blum', 'Bllume', 'Bmme', 'Blumee', 'Bblum',
        'BlUme', 'Bluee', 'Bluem', 'Buume', 'Blmme']
