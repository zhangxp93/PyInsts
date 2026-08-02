import pytest
from pyinsts.instrument_drivers import (
    DM34461A,
    KeysightE36312A,
    KeysightE5052B,
    KeysightE8257D,
    KeysightN1914A,
    KeysightN5245B,
    KeysightN9020B,
    KeysightN9030A,
    KeysightN9030B,
    FSV3030Sp,
    FswpPN,
    Zna43,
    Th1963,
    P2401,
    Rsa6000,
    Sna6034a,
)


def test_sim_dm34461a():
    with DM34461A(address="USB::0x2A8D::0x1301::MY53000200::INSTR;@sim", model="34461A") as inst:
        assert "34461A" in inst.idn


def test_sim_e36312a():
    with KeysightE36312A(address="USB::0x2A8D::0x1102::MY58000100::INSTR;@sim", model="E36312A") as inst:
        assert "E36312A" in inst.idn


def test_sim_e5052b():
    with KeysightE5052B(address="GPIB::17::INSTR;@sim", model="E5052B") as inst:
        assert "E5052B" in inst.idn


def test_sim_e8257d():
    with KeysightE8257D(address="USB::0x0957::0x0501::MY45470200::INSTR;@sim", model="E8257D") as inst:
        assert "E8257D" in inst.idn


def test_sim_n1914a():
    with KeysightN1914A(address="USB::0x0957::0x2B17::MY51000100::INSTR;@sim", model="N1914A") as inst:
        assert "N1914A" in inst.idn


def test_sim_n5245b():
    with KeysightN5245B(address="GPIB::16::INSTR;@sim", model="N5245B") as inst:
        assert "N5245B" in inst.idn


def test_sim_n9020b():
    with KeysightN9020B(address="USB::0x2A8D::0x1D0B::MY55480186::INSTR;@sim", model="N9020B") as inst:
        assert "N9020B" in inst.idn


def test_sim_n9030a():
    with KeysightN9030A(address="USB::0x2A8D::0x1A0A::MY53000100::INSTR;@sim", model="N9030A") as inst:
        assert "N9030A" in inst.idn


def test_sim_n9030b():
    with KeysightN9030B(address="USB::0x2A8D::0x1A0B::MY54000100::INSTR;@sim", model="N9030B") as inst:
        assert "N9030B" in inst.idn


def test_sim_fsv3030():
    with FSV3030Sp(address="USB::0x0AAD::0x0119::100001::INSTR;@sim", model="FSV3030") as inst:
        assert "FSV3030" in inst.idn


def test_sim_fswp():
    with FswpPN(address="TCPIP::192.168.1.100::inst0::INSTR;@sim", model="FSWP") as inst:
        assert "FSWP" in inst.idn


def test_sim_zna43():
    with Zna43(address="TCPIP::192.168.1.105::inst0::INSTR;@sim", model="ZNA43") as inst:
        assert "ZNA43" in inst.idn


def test_sim_th1963():
    with Th1963(address="USB::0x0483::0x7540::TH19630001::INSTR;@sim", model="TH1963") as inst:
        assert "TH1963" in inst.idn


def test_sim_p2401():
    with P2401(address="USB::0x1234::0x5678::P24010001::INSTR;@sim", model="P2401") as inst:
        assert "P2401" in inst.idn


def test_sim_rsa6000():
    with Rsa6000(address="GPIB::1::INSTR;@sim", model="RSA6000") as inst:
        assert "RSA6000" in inst.idn


def test_sim_sna6034a():
    with Sna6034a(address="TCPIP::192.168.1.110::inst0::INSTR;@sim", model="SNA6034A") as inst:
        assert "SNA6034A" in inst.idn
