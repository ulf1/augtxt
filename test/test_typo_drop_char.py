from augtxt.typo import drop_char


def test1():
    augm = drop_char("Straße", loc=0)
    assert augm == "traße"


def test2():
    augm = drop_char("Straße", loc=1)
    assert augm == "Sraße"


def test3():
    augm = drop_char("Straße", loc=2)
    assert augm == "Staße"


def test4():
    augm = drop_char("Straße", loc=3)
    assert augm == "Strße"


def test5():
    augm = drop_char("Straße", loc=4)
    assert augm == "Strae"


def test6():
    augm = drop_char("Straße", loc=5)
    assert augm == "Straß"


def test7():
    augm = drop_char("Straße", loc=0, keep_case=True)
    assert augm == "Traße"


def test8():
    augm = drop_char("Straße", loc=0, keep_case=True)
    assert augm == "Traße"
