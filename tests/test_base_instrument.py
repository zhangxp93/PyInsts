import pyinsts
from pyinsts.instrument_drivers import FSV3030Sp

FSV3030_SIM_ADDRESS = "USB::0x0AAD::0x0119::100001::INSTR;@sim"


def test_package_version():
    assert pyinsts.__version__ == "0.1.0"


def test_sim_connection_idn():
    inst = FSV3030Sp(address=FSV3030_SIM_ADDRESS, model="FSV3030")
    try:
        assert "Rohde&Schwarz" in inst.idn
        assert "FSV3030" in inst.idn
    finally:
        inst.close()


def test_context_manager_closes_connection():
    with FSV3030Sp(address=FSV3030_SIM_ADDRESS, model="FSV3030") as inst:
        assert inst.instrument is not None
        assert "FSV3030" in inst.idn

    assert inst.instrument is None
    assert inst.rm is None


def test_write_and_query_via_sim():
    with FSV3030Sp(address=FSV3030_SIM_ADDRESS, model="FSV3030") as inst:
        inst.write("*CLS")
        idn = inst.query("*IDN?")
        assert "FSV3030" in idn
