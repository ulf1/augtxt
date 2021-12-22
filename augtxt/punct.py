import re


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
