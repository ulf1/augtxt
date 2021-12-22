import re
import copy
import numpy as np


def remove_syntaxinfo(text: str) -> str:
    """ Remove `.?!;:,` from string (The $. and $, POS tags in STTS)

    Example:
    --------
    import augtxt.punct
    text = ("Die Lehrerin [MASK] einen Roman. "
            "Die Schülerin [MASK] ein Aufsatz, der sehr [MASK] war.")
    augmented = augtxt.punct.remove_punctcomma(text)
    """
    return re.sub(r'\s+', ' ', re.sub(r'[.?!;:,]+', ' ', text)).strip()


def merge_words(text_: str, sep=[" ", "-", "–"], num_aug: int = 1) -> str:
    """ Remove whitespace- or hyphen-seperated words

    Example:
    --------
    text = "Die Bindestrich-Wörter sind da."
    augmented = merge_words(text)
    """
    text = copy.copy(text_)
    indicies = [i for i, c in enumerate(text) if c in sep]
    indicies = np.flip(np.sort(np.random.choice(indicies, size=num_aug)))
    for i in indicies:
        try:
            text = text[:i] + text[i + 1].lower() + text[(i + 2):]
        except Exception:
            print("sep char at the end of text.")
    return text
