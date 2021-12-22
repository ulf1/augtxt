from augtxt.punct import remove_syntaxinfo


def test1():
    text = ("Die Lehrerin [MASK] einen Roman. "
            "Die Schülerin [MASK] ein Aufsatz, der sehr [MASK] war.")
    augmented = remove_syntaxinfo(text)
    assert augmented == ("Die Lehrerin [MASK] einen Roman Die Schülerin "
                         "[MASK] ein Aufsatz der sehr [MASK] war")
