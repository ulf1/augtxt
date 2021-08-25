from augtxt.typo import pressed_shiftalt
import augtxt.keyboard_layouts as kbl


def test1():
    augm = pressed_shiftalt("Onkel", loc=2)
    assert augm in ("OnKel", "On˚el", "Onel")


def test2():
    augm = pressed_shiftalt("Onkel", loc=2, keymap=kbl.qwertz_de)
    assert augm in ("OnKel", "Onĸel", "On&el")
