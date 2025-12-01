from gray_code.ilds import Halton, VdCorput, vdc_i


def test_vdc() -> None:
    assert vdc_i(1, 2, 10) == 512


def test_vdcorput() -> None:
    vgen = VdCorput(2, 10)
    vgen.reseed(0)
    assert vgen.pop() == 512


def test_halton() -> None:
    hgen = Halton([2, 3], [11, 7])
    hgen.reseed(0)
    assert hgen.pop() == [1024, 729]
