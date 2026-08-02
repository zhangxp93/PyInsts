# 控制N1914A子程序，未完成
from typing import Literal

import time

from pyinsts.instrument_drivers import BaseInstrument


class KeysightN1914A(BaseInstrument):
    def __init__(self, address: str = None, config_path="config.yaml",
                 model: str = "N1914A"):
        super().__init__(address=address, config_path=config_path, model=model)

    def set_freq(self, freq, unit:Literal["Hz", "kHz", "MHz", "GHz"]):
        """
        设置频率GHz
        :param unit:
        :param freq:
        :return:
        """
        self.write(f'SENS:FREQ {freq}{unit}')

    def query_power(self):
        """
        读取功率
        :return:
        """
        power = float(self.query(f'FETC?'))
        time.sleep(0.01)
        return power

    def close(self):
        super().close()
        pass


if __name__ == '__main__':
    addr_u8487a = "USB0::0x2A8D::0xA618::MY62270005::0::INSTR"
    addr_u2022xa = "USB0::0x2A8D::0x7F18::MY60100009::INSTR"
    addr_n1914a = "USB0::0x0957::0x5518::MY56440029::INSTR"
    n1914a = KeysightN1914A(addr_n1914a)
    power1 = n1914a.query_power()
    print(power1)
    n1914a.close()
