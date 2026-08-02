import pytest
from pyinsts.instrument_drivers import KeysightN9020B, KeysightE8257D

N9020B_SIM_ADDRESS = "USB::0x2A8D::0x1D0B::MY55480186::INSTR;@sim"
E8257D_SIM_ADDRESS = "USB::0x0957::0x0501::MY45470200::INSTR;@sim"


def test_n9020b_sim_connection():
    with KeysightN9020B(address=N9020B_SIM_ADDRESS, model="N9020B") as n9020b:
        assert "Keysight" in n9020b.idn
        assert "N9020B" in n9020b.idn
        n9020b.set_freq_cent(1.0, "GHz")
        n9020b.set_rbw_auto()
        n9020b.set_peak_search()
        power = n9020b.query_mark_y_power()
        assert float(power) == -12.50


def test_e8257d_sim_connection():
    with KeysightE8257D(address=E8257D_SIM_ADDRESS, model="E8257D") as e8257d:
        assert "Keysight" in e8257d.idn
        assert "E8257D" in e8257d.idn
        e8257d.set_freq(1.5, "GHz")
        e8257d.set_power(-5)
        e8257d.set_output("ON")
