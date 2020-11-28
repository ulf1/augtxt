from augtxt.typo import pressed_shiftalt


def test1():
    augm = pressed_shiftalt("Onkel", loc=2)
    assert augm in ("OnKel", "On˚el", "Onel")
