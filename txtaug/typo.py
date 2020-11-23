from typing import Optional, Union
import numpy as np
import scipy.stats


def draw_index(n: int, loc: Union[int, float, str]):
    """Get index

    n : int
        upper value from interval [0,n] to draw from

    loc : Union[int, float, str]
        If `int`, the index of the 1st char to swap
        If `float`, the `p` of `binom.rvs(n, p)`
        If 'b', then `binom.rvs(n, p=0.1)`
        If 'm', then `binom.rvs(n, p=0.5)`
        If 'e', then `binom.rvs(n, p=0.9)`

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
        if isinstance(loc, str):
            if loc in ('begin', 'b'):
                p = 0.1
            elif loc in ('middle', 'm'):
                p = 0.5
            elif loc in ('end', 'e'):
                p = 0.9
        i = scipy.stats.binom.rvs(n, p)

    return i


def swap_consecutive(word: str,
                     loc: Optional[Union[int, float, str]] = 0,
                     keep_case: Optional[bool] = False
                     ) -> str:
    """Swap two consecutive chars (dt. Vertauscher)

    word : str
        One word token

    loc : Union[int, float, str]
        see txtaug.typo.draw_index

    keep_case : bool  (Default False, i.e. never)
        Enforce the original letter cases on the new string.

    Examples:
    ---------
        swap_consecutive("Kinder", loc=0)
        iKnder

        swap_consecutive("Kinder", loc=0, keep_case=True)
        Iknder

        np.random.seed(seed=42)
        swap_consecutive("Kinder", loc='middle', keep_case=True)
        swap_consecutive("Kinder", loc='begin', keep_case=True)
        swap_consecutive("Kinder", loc='end', keep_case=True)
        'Kindre', 'Iknder', 'Kindre'
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
                  loc: Optional[Union[int, float, str]] = 0
                  ) -> str:
    """A key is pressed twice accidentaly (dt. Einfüger)"""
    # abort prematurly
    n_chars = len(word)
    if n_chars == 1:
        return word + word

    # find index of the 1st char
    i = draw_index(n_chars - 1, loc)

    return word[:i] + word[i] + word[i:]
