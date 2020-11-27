import numpy as np
from augtxt.typo import swap_consecutive


def test1():
    augm = swap_consecutive("Kinder", loc=0)
    assert augm == "iKnder"


def test2():
    augm = swap_consecutive("Kinder", loc=0, keep_case=True)
    assert augm == "Iknder"


def test3():
    augm = swap_consecutive("Kinder", loc=1)
    assert augm == "Knider"


def test4():
    augm = swap_consecutive("Kinder", loc=2)
    assert augm == "Kidner"


def test5():
    augm = swap_consecutive("Kinder", loc=3)
    assert augm == "Kinedr"


def test6():
    augm = swap_consecutive("Kinder", loc=4)
    assert augm == "Kindre"


def test7():
    augm = swap_consecutive("Kinder", loc=0.0)
    assert augm == "iKnder"


def test8():
    augm = swap_consecutive("Kinder", loc=0.0, keep_case=True)
    assert augm == "Iknder"


def test9():
    augm = swap_consecutive("Kinder", loc=1.0)
    assert augm == "Kindre"


def test10():
    np.random.seed(seed=42)
    augm = (
        swap_consecutive("Kinder", loc='begin', keep_case=True),
        swap_consecutive("Kinder", loc='middle', keep_case=True),
        swap_consecutive("Kinder", loc='end', keep_case=True)
    )
    assert augm == ('Iknder', 'Kindre', 'Kinedr')


def test11():
    np.random.seed(seed=42)
    augm = (
        swap_consecutive("Kinder", loc=0.1, keep_case=True),
        swap_consecutive("Kinder", loc=0.5, keep_case=True),
        swap_consecutive("Kinder", loc=0.9, keep_case=True)
    )
    assert augm == ('Iknder', 'Kindre', 'Kinedr')


def test12():
    augm = swap_consecutive("A", loc=0)
    assert augm == "A"


def test13():
    augm = swap_consecutive("AB", loc=0)
    assert augm == "BA"


def test14():
    augm = swap_consecutive("AB", loc=123)
    assert augm == "BA"
