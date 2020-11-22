from typing import Optional, Union
import numpy as np
import scipy.stats


def swap_consecutive(word: str,
                     loc: Optional[Union[int, float, str]] = 0,
                     keep_case: Optional[bool] = False
                    ) -> str:
    """Swap two consecutive chars (dt. Vertauscher)

    word : str
        One word token

    loc : Union[int, float, str]
        If `int`, the index of the 1st char to swap
        If `float`, the `p` of `binom.rvs(n, p)`
        If 'b', then `binom.rvs(n, p=0.1)`
        If 'm', then `binom.rvs(n, p=0.5)`
        If 'e', then `binom.rvs(n, p=0.9)`

    keep_case : bool  (Default False, i.e. never)
        Enforce the original letter cases on the new string.

    Examples:
    ---------
        typo_swap_consecutive("Kinder", loc=0)
        iKnder

        typo_swap_consecutive("Kinder", loc=0, keep_case=True)
        Iknder

        np.random.seed(seed=42)
        typo_swap_consecutive("Kinder", loc='middle', keep_case=True)
        typo_swap_consecutive("Kinder", loc='begin', keep_case=True)
        typo_swap_consecutive("Kinder", loc='end', keep_case=True)
        'Kindre', 'Iknder', 'Kindre'
    """
    # abort prematurly
    n_chars = len(word)
    if n_chars < 2:
        return word

    # copy string to mutable char list
    res = [c for c in word]

    # find index of the 1st char
    if isinstance(loc, int):  # Given index
        i = max(0, min(n_chars - 2, loc))

    elif isinstance(loc, float): # Pick random index
        binom_n = n_chars - 2
        binom_p =  max(0.0, min(1.0, loc))
        i = scipy.stats.binom.rvs(binom_n, binom_p)

    elif isinstance(loc, str):  # Pick random index
        binom_n = n_chars - 2
        if isinstance(loc, str):
            if loc in ('begin', 'b'):
                binom_p = 0.1
            elif loc in ('middle', 'm'):
                binom_p = 0.5
            elif loc in ('end', 'e'):
                binom_p = 0.9
        i = scipy.stats.binom.rvs(binom_n, binom_p)
   
    # enforce letter case
    if keep_case:
        c0, c1 = res[i].isupper(), res[i+1].isupper()

    # swap
    res[i], res[i+1] = res[i+1], res[i]

    # enforce previous letter cases
    if keep_case:
        res[i] = res[i].upper() if c0 else res[i].lower()
        res[i+1] = res[i+1].upper() if c1 else res[i+1].lower()

    return ''.join(res)
