import numpy as np
from typing import List
import re


def swap_consecutive(original,
                     exclude: List[str] = ["[MASK]"],
                     punct: str = ".,;:!?",
                     num_aug: int = 1):
    # simple whitespace tokenization
    token = [t for t in re.split(f"[ {punct}]", original) if len(t) > 0]
    # which tokens are not excluded?
    if exclude is None:
        exclude = []
    indicies = np.where([t not in exclude for t in token])[0]
    # eligible combinations
    twoidx = np.c_[indicies[:-1], indicies[1:]]
    twoidx = twoidx[(twoidx[:, 1] - twoidx[:, 0]) == 1]
    # draw a random pair
    selected = np.random.choice(
        twoidx.shape[0], min(twoidx.shape[0], num_aug), replace=False)
    # swap tokens
    for i, j in twoidx[selected, :]:
        idx1 = original.find(token[i])
        idx2 = original.find(token[j]) + len(token[j])
        original = f"{original[:idx1]} {token[j]} {token[i]} {original[idx2:]}"
        token[j], token[i] = token[i], token[j]
    # clean up
    original = original.strip()
    original = re.sub(' +', ' ', original)
    original = re.sub(f"\\s(?=[{punct}])", "", original)
    # done
    return original


def drop_word(original,
              exclude: List[str] = ["[MASK]"],
              punct: str = ".,;:!?",
              num_aug: int = 1):
    # simple whitespace tokenization
    token = [t for t in re.split(f"[ {punct}]", original) if len(t) > 0]
    # which tokens are not excluded?
    if exclude is None:
        exclude = []
    indicies = np.where([t not in exclude for t in token])[0]
    # draw random tokens
    selected = np.random.choice(
        indicies, size=min(len(indicies), num_aug), replace=False)
    # reomve words from string
    for i in selected:
        original = original.replace(token[i], "").strip()
    # clean up
    original = re.sub(' +', ' ', original)
    original = re.sub(f"\\s(?=[{punct}])", "", original)
    # done
    return original


def write_twice(original,
                exclude: List[str] = ["[MASK]"],
                punct: str = ".,;:!?",
                num_aug: int = 1):
    # simple whitespace tokenization
    token = [t for t in re.split(f"[ {punct}]", original) if len(t) > 0]
    # which tokens are not excluded?
    if exclude is None:
        exclude = []
    indicies = np.where([t not in exclude for t in token])[0]
    # draw random tokens
    selected = np.random.choice(
        indicies, size=min(len(indicies), num_aug), replace=False)
    # reomve words from string
    for i in selected:
        idx = original.find(token[i])
        original = f"{original[:idx]}{token[i]} {original[idx:]}"
    # clean up
    original = original.strip()
    original = re.sub(' +', ' ', original)
    original = re.sub(f"\\s(?=[{punct}])", "", original)
    # done
    return original


def drop_n_next_twice(original,
                      exclude: List[str] = ["[MASK]"],
                      punct: str = ".,;:!?",
                      num_aug: int = 1):
    # simple whitespace tokenization
    token = [t for t in re.split(f"[ {punct}]", original) if len(t) > 0]
    # which tokens are not excluded?
    if exclude is None:
        exclude = []
    indicies = np.where([t not in exclude for t in token])[0]
    # eligible combinations
    twoidx = np.c_[indicies[:-1], indicies[1:]]
    twoidx = twoidx[(twoidx[:, 1] - twoidx[:, 0]) == 1]
    # draw a random pair
    selected = np.random.choice(
        twoidx.shape[0], min(twoidx.shape[0], num_aug), replace=False)
    # drop first token, and add the other one
    for i, j in twoidx[selected, :]:
        idx1 = original.find(token[i])
        idx2 = original.find(token[j])
        original = f"{original[:idx1]} {token[j]} {original[idx2:]}"
    # clean up
    original = original.strip()
    original = re.sub(' +', ' ', original)
    original = re.sub(f"\\s(?=[{punct}])", "", original)
    # done
    return original
