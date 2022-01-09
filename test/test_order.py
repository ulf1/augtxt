import augtxt.order
import numpy as np


def test_swap1():
    """Swap words"""
    np.random.seed(seed=42)
    text = "Tausche die Wörter, lasse sie weg, oder [MASK] was."
    augmented = augtxt.order.swap_consecutive(
        text, exclude=["[MASK]"], num_aug=1)
    target = "die Tausche Wörter, lasse sie weg, oder [MASK] was."
    assert augmented == target


def test_twice1():
    """Write twice"""
    np.random.seed(seed=42)
    text = "Tausche die Wörter, lasse sie weg, oder [MASK] was."
    augmented = augtxt.order.write_twice(
        text, exclude=["[MASK]"], num_aug=1)
    target = "Tausche die die Wörter, lasse sie weg, oder [MASK] was."
    assert augmented == target


def test_drop1():
    """Drop word"""
    np.random.seed(seed=42)
    text = "Tausche die Wörter, lasse sie weg, oder [MASK] was."
    augmented = augtxt.order.drop_word(
        text, exclude=["[MASK]"], num_aug=1)
    target = "Tausche Wörter, lasse sie weg, oder [MASK] was."
    assert augmented == target


def test_follow1():
    """Drop word followed by a double word"""
    np.random.seed(seed=42)
    text = "Tausche die Wörter, lasse sie weg, oder [MASK] was."
    augmented = augtxt.order.drop_n_next_twice(
        text, exclude=["[MASK]"], num_aug=1)
    target = "die die Wörter, lasse sie weg, oder [MASK] was."
    assert augmented == target
