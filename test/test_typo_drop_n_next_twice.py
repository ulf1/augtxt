from augtxt.typo import drop_n_next_twice


def test1():
    augm = drop_n_next_twice("Ab", loc=0)
    assert augm == "bb"


def test2():
    augm = drop_n_next_twice("Ab", loc=0, keep_case=True)
    assert augm == "Bb"


def test3():
    augm = drop_n_next_twice("A", loc=0)
    assert augm == "A"


def test4():
    augm = drop_n_next_twice("Tante", loc=0)
    assert augm == "aante"


def test5():
    augm = drop_n_next_twice("Tante", loc=1)
    assert augm == "Tnnte"


def test6():
    augm = drop_n_next_twice("Tante", loc=2)
    assert augm == "Tatte"


def test7():
    augm = drop_n_next_twice("Tante", loc=3)
    assert augm == "Tanee"


def test8():
    augm = drop_n_next_twice("Tante", loc=4)
    assert augm == "Tanee"
