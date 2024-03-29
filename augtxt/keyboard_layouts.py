
def find_index(c: str, keymap: dict) -> (int, str):
    """Find index
    Examples:
        idx, mode = find_index("h", macbook_us)
    """
    for mode in keymap.keys():
        try:
            return keymap[mode].index(c), mode
        except Exception:
            pass
    return None, None


# default transition probabilities
keyboard_transprob = {
    "keys": [.0, .75, .2, .05],
    "shift": [.9, 0, .05, .05],
    "alt": [.9, .05, .0, .05],
    "shift+alt": [.3, .35, .35, .0]
}


macbook_us = {
    "keys": [
        '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'',
        'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'
    ],
    "shift": [
        '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+',
        'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"',
        'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?'
    ],
    "alt": [
        '`', '¡', '™', '£', '¢', '∞', '§', '¶', '•', 'ª', 'º', '–', '≠',
        'œ', '∑', '´', '®', '†', '¥', '¨', 'ˆ', 'ø', 'π', '“', '‘', '«',
        'å', 'ß', '∂', 'ƒ', '©', '˙', '∆', '˚', '¬', '…', 'æ',
        'Ω', '≈', 'ç', '√', '∫', '˜', 'µ', '≤', '≥', '÷'
    ],
    "shift+alt": [
        '`', '⁄', '€', '‹', '›', 'ﬁ', 'ﬂ', '‡', '°', '·', '‚', '—', '±',
        'Œ', '„', '´', '‰', 'ˇ', 'Á', '¨', 'ˆ', 'Ø', '∏', '”', '’', '»',
        'Å', 'Í', 'Î', 'Ï', '˝', 'Ó', 'Ô', '', 'Ò', 'Ú', 'Æ',
        '¸', '˛', 'Ç', '◊', 'ı', '˜', 'Â', '¯', '˘', '¿'
    ]
}

qwertz_de = {
    "keys": [
        '^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ß', "'",
        'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'ü', '+',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', '#',
        '<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-'
    ],
    "shift": [
        '°', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', '`',
        'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'Ü', '*',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', "'",
        '>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_'
    ],
    "alt": [
        '′', '¹', '²', '³', '¼', '½', '¬', '{', '[', ']', '}', '\\', '¸',
        '@', 'ł', '€', '¶', 'ŧ', '←', '↓', '→', 'ø', 'þ', '"', '~',
        'æ', 'ſ', 'ð', 'đ', 'ŋ', 'ħ', '̣', 'ĸ', 'ł', '˝', '^', '’',
        '|', '»', '«', '¢', '„', '“', '”', 'µ', '·', '…', '–'

    ],
    "shift+alt": [
        '″', '¡', '⅛', '£', '¤', '⅜', '⅝', '⅞', '™', '±', '°', '¿', '˛',
        'Ω', 'Ł', '€', '®', 'Ŧ', '¥', '↑', 'ı', 'Ø', 'Þ', '°', '¯',
        'Æ', 'ẞ', 'Ð', 'ª', 'Ŋ', 'Ħ', '˙', '&', 'Ł', '̣', '̣', '˘',
        '', '›', '‹', '©', '‚', '‘', '’', 'º', '×', '÷', '—'
    ]
}
