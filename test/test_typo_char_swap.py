import numpy as np
from txtaug.typo import (
    typo_char_swap)


def test1():
    augm = typo_char_swap("Kinder", loc=0)
    assert augm == "iKnder"

def test2():
    augm = typo_char_swap("Kinder", loc=0, keep_case=True)
    assert augm == "Iknder"

def test3():
    augm = typo_char_swap("Kinder", loc=1)
    assert augm == "Knider"

def test4():
    augm = typo_char_swap("Kinder", loc=2)
    assert augm == "Kidner"

def test5():
    augm = typo_char_swap("Kinder", loc=3)
    assert augm == "Kinedr"

def test6():
    augm = typo_char_swap("Kinder", loc=4)
    assert augm == "Kindre"

def test7():
    augm = typo_char_swap("Kinder", loc=0.0)
    assert augm == "iKnder"

def test8():
    augm = typo_char_swap("Kinder", loc=0.0, keep_case=True)
    assert augm == "Iknder"

def test9():
    augm = typo_char_swap("Kinder", loc=1.0)
    assert augm == "Kindre"

def test10():
    np.random.seed(seed=42)
    augm = (
        typo_char_swap("Kinder", loc='begin', keep_case=True),
        typo_char_swap("Kinder", loc='middle', keep_case=True),
        typo_char_swap("Kinder", loc='end', keep_case=True)
    )
    assert augm == ('Iknder', 'Kindre', 'Kinedr')

def test11():
    np.random.seed(seed=42)
    augm = (
        typo_char_swap("Kinder", loc=0.1, keep_case=True),
        typo_char_swap("Kinder", loc=0.5, keep_case=True),
        typo_char_swap("Kinder", loc=0.9, keep_case=True)
    )
    assert augm == ('Iknder', 'Kindre', 'Kinedr')

def test12():
    augm = typo_char_swap("A", loc=0)
    assert augm == "A"

def test13():
    augm = typo_char_swap("AB", loc=0)
    assert augm == "BA"

def test14():
    augm = typo_char_swap("AB", loc=123)
    assert augm == "BA"
