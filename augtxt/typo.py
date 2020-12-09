from typing import Optional, Union
import numpy as np
import scipy.stats
import augtxt.keyboard_layouts as kbl


def draw_index(n: int, loc: Union[int, float, str]) -> int:
    """Get index

    Parameters:
    -----------
    n : int
        upper value from interval [0,n] to draw from

    loc : Union[int, float, str]
        If `int`, the index of the 1st char to swap
        If `float`, the `p` of `binom.rvs(n, p)`
        If 'b', then `binom.rvs(n, p=0.1)`
        If 'm', then `binom.rvs(n, p=0.5)`
        If 'e', then `binom.rvs(n, p=0.9)`
        if 'u', then uniform random

    Return:
    -------
    int
        An list index

    Examples:
    ---------
        np.random.seed(seed=42)
        idx = draw_index(7, loc='middle')
    """
    if isinstance(loc, int):  # Given index
        i = max(0, min(n, loc))

    elif isinstance(loc, float):  # Pick random index
        p = max(0.0, min(1.0, loc))
        i = scipy.stats.binom.rvs(n, p)

    elif isinstance(loc, str):  # Pick random index
        if loc in ('uniform', 'u'):
            i = scipy.stats.randint.rvs(0, n + 1)
        else:
            if loc in ('begin', 'b'):
                p = 0.1
            elif loc in ('middle', 'm'):
                p = 0.5
            elif loc in ('end', 'e'):
                p = 0.9
            else:
                raise Exception("Unknown p (loc) for binom")
            i = scipy.stats.binom.rvs(n, p)

    return i


def swap_consecutive(word: str,
                     loc: Optional[Union[int, float, str]] = 'u',
                     keep_case: Optional[bool] = False
                     ) -> str:
    """Swap two consecutive chars (dt. Vertauscher)

    Parameters:
    -----------
    word : str
        One word token

    loc : Union[int, float, str]
        see augtxt.typo.draw_index

    keep_case : bool  (Default False, i.e. never)
        Enforce the original letter cases on the new string.

    Return:
    -------
    str
        The augmented variant of the input word

    Examples:
    ---------
        from augtxt.typo import swap_consecutive
        swap_consecutive("Kinder", loc=0)
        # iKnder

        swap_consecutive("Kinder", loc=0, keep_case=True)
        # Iknder

        np.random.seed(seed=42)
        swap_consecutive("Kinder", loc='middle', keep_case=True)
        swap_consecutive("Kinder", loc='begin', keep_case=True)
        swap_consecutive("Kinder", loc='end', keep_case=True)
        # 'Kindre', 'Iknder', 'Kindre'
    """
    # abort prematurly
    n_chars = len(word)
    if n_chars < 2:
        return word

    # copy string to mutable char list
    res = [c for c in word]

    # find index of the 1st char
    i = draw_index(n_chars - 2, loc)

    # enforce letter case
    if keep_case:
        c0, c1 = res[i].isupper(), res[i + 1].isupper()

    # swap
    res[i], res[i + 1] = res[i + 1], res[i]

    # enforce previous letter cases
    if keep_case:
        res[i] = res[i].upper() if c0 else res[i].lower()
        res[i + 1] = res[i + 1].upper() if c1 else res[i + 1].lower()

    return ''.join(res)


def pressed_twice(word: str,
                  loc: Optional[Union[int, float, str]] = 'u',
                  keep_case: Optional[bool] = False
                  ) -> str:
    """A key is pressed twice accidentaly (dt. Einfüger)

    Parameters:
    -----------
    word : str
        One word token

    loc : Union[int, float, str]
        see augtxt.typo.draw_index

    flip_case : bool  (Default False, i.e. never)
        Enforce the letter case of the succeeding charcter.

    Return:
    -------
    str
        The augmented variant of the input word

    Example:
    --------
        from augtxt.typo import pressed_twice
        augm = pressed_twice("Test", loc=['b', 'e'], keep_case=True)
    """
    # abort prematurly
    n_chars = len(word)
    if n_chars == 1:
        return word + word

    # find index of the 1st char
    i = draw_index(n_chars - 1, loc)

    # save letter case
    i2 = min(i + 1, n_chars - 1)
    if keep_case:
        case = word[i2].isupper()
        c = word[i].upper() if case else word[i].lower()
    else:
        c = word[i]

    return word[:i2] + c + word[i2:]


def drop_char(word: str,
              loc: Optional[Union[int, float, str]] = 'u',
              keep_case: Optional[bool] = False
              ) -> str:
    """Drop a character (dt. Auslasser)

    Parameters:
    -----------
    word : str
        One word token

    loc : Union[int, float, str]
        see augtxt.typo.draw_index

    keep_case : bool
        Apply the letter case of the dropped character to the next
          remaining character.

    Return:
    -------
    str
        The augmented variant of the input word

    Example:
    --------
        from augtxt.typo import drop_char
        augm = drop_char("Test", loc='b', keep_case=False)
    """
    # abort prematurly
    n_chars = len(word)
    if n_chars == 1:
        return word

    # find index of the 1st char
    i = draw_index(n_chars - 1, loc)

    # save letter case
    if keep_case:
        case = word[i].isupper()

    # create new word
    res = word[:i] + word[(i + 1):]

    # enforce dropped letter case on the next charcter
    if keep_case:
        res = ''.join([c.upper() if idx == i and case else c
                       for idx, c in enumerate(res)])

    # done
    return res


def drop_n_next_twice(word: str,
                      loc: Optional[Union[int, float, str]] = 'u',
                      keep_case: Optional[bool] = False
                      ) -> str:
    """Letter is left out, but the following letter is typed twice
        (dt. Vertipper)

    Parameters:
    -----------
    word : str
        One word token

    loc : Union[int, float, str]
        see augtxt.typo.draw_index

    keep_case : bool  (Default: False)
        Apply the letter case of the dropped character to the next
          remaining character.

    Return:
    -------
    str
        The augmented variant of the input word

    Example:
    --------
        from augtxt.typo import drop_n_next_twice
        augm = drop_n_next_twice("Test", loc='u', keep_case=False)
    """
    # abort prematurly
    n_chars = len(word)
    if n_chars == 1:
        return word

    # find index of the 1st char
    i = draw_index(n_chars - 2, loc)

    # save letter case
    if keep_case:
        case = word[i].isupper()

    # create new word
    i2 = min(i + 1, n_chars - 1)
    res = word[:i] + word[i2] + word[i2:]

    # enforce dropped letter case on the next charcter
    if keep_case:
        res = ''.join([c.upper() if idx == i and case else c
                       for idx, c in enumerate(res)])
    # done
    return res


def pressed_shiftalt(word: str,
                     loc: Optional[Union[int, float, str]] = 'u',
                     keymap: dict = kbl.macbook_us,
                     trans: dict = kbl.keyboard_transprob
                     ) -> str:
    """Typo due to pressing or not pressing SHIFT, ALT, or SHIFT+ALT

    Parameters:
    -----------
    word : str
        One word token

    loc : Union[int, float, str]
        see augtxt.typo.draw_index

    keymap: dict
        A dictionary with four keyboard states as keys ("keys", "shift",
          "alt", "shift+alt"). Each key stores a list of characters.

    trans : dict
        Contains the transitions probabilities from a given keyboard state
          to another.

    Return:
    -------
    str
        The augmented variant of the input word

    Example:
    --------
        from augtxt.typo import pressed_shiftalt
        augm = pressed_shiftalt("Test")
    """
    # abort prematurly
    n_chars = len(word)
    if n_chars == 1:
        return word

    # find index of the 1st char
    i = draw_index(n_chars - 1, loc)

    # find index and keyboard states in keymap
    idx, state = kbl.find_index(word[i], keymap)
    # draw new keyboard state, and lookup new char for given idx
    if idx:
        newstate = np.random.choice(4, 1, p=trans[state])[0]
        newstate = tuple(keymap.keys())[newstate]
        newchar = keymap[newstate][idx]
        i2 = min(i, n_chars - 1)
        return word[:i2] + newchar + word[(i2 + 1):]
    else:
        return word
