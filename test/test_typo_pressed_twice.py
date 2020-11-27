import numpy as np
from augtxt.typo import pressed_twice


def test1():
    augm = pressed_twice("Eltern", loc=0)
    assert augm == "EEltern"


def test2():
    augm = pressed_twice("Eltern", loc=1)
    assert augm == "Elltern"


def test3():
    augm = pressed_twice("Eltern", loc=2)
    assert augm == "Elttern"


def test4():
    augm = pressed_twice("Eltern", loc=3)
    assert augm == "Elteern"


def test5():
    augm = pressed_twice("Eltern", loc=4)
    assert augm == "Elterrn"


def test6():
    augm = pressed_twice("Eltern", loc=5)
    assert augm == "Elternn"


def test7():
    np.random.seed(seed=7)
    augm = (
        pressed_twice("Eltern", loc='begin'),
        pressed_twice("Eltern", loc='middle'),
        pressed_twice("Eltern", loc='end')
    )
    assert augm == ('EEltern', 'Elteern', 'Elternn')


def test8():
    augm = pressed_twice("Ab", loc=0, keep_case=False)
    assert augm == "AAb"


def test9():
    augm = pressed_twice("Ab", loc=0, keep_case=True)
    assert augm == "Aab"


def test10():
    augm = pressed_twice("A", loc=0, keep_case=True)
    assert augm == "AA"
