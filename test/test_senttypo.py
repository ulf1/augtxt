from augtxt.augmenters import senttypo
import augtxt.keyboard_layouts as kbl
import numpy as np

settings = [
    {
        'weight': 2, 'fn': 'typo.drop_n_next_twice',
        'args': {'loc': 'u', 'keep_case': True}
    },
    {
        'weight': 2, 'fn': 'typo.swap_consecutive',
        'args': {'loc': 'u', 'keep_case': True}},
    {
        'weight': 1, 'fn': 'typo.pressed_twice',
        'args': {'loc': 'u', 'keep_case': True}
    },
    {
        'weight': 1, 'fn': 'typo.drop_char',
        'args': {'loc': 'u', 'keep_case': True}
    },
    {
        'weight': 1, 'fn': 'typo.pressed_shiftalt',
        'args': {'loc': ['b', 'm']},
        'keymap': kbl.qwertz_de,
        'trans': kbl.keyboard_transprob
    },
]


def test1():
    np.random.seed(seed=42)
    exclude = ["[MASK]", "[UNK]"]
    sentence = 'Die Lehrerin [MASK] einen Roman.'
    augmentations = senttypo(
        sentence, settings=settings, exclude=exclude,
        num_augmentations=10, pmax=0.1)
    assert len(augmentations) == 10
    assert augmentations == [
        'Die Lehrerin [MASK] eien Roman.',
        'Die Lehrerin [MASK] einen Rooman.',
        'Die Lehrerin [MASK] eieen Roman.',
        'Die Lehrerin [MASK] einen Romna.',
        'Die Lehrerin [MASK] einen Romann.',
        'Die Lehrein [MASK] einen Roman.',
        'Die Leheerin [MASK] einen Roman.',
        'Diie Lehrerin [MASK] einen Roman.',
        'Die Eehrerin [MASK] einen Roman.',
        'Ide Lehrerin [MASK] einen Roman.']
