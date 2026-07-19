# E8257D信号源，频率250KHz~40Ghz
from typing import Literal

import pyvisa
import time

from pyinsts.instrument_drivers import BaseInstrument


# 定义E8257d类，连接E8257d信号源分析仪
class KeysightE8257D(BaseInstrument):
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "E8257D"):
        super().__init__(address=address, config_path=config_path, model=model)

    def set_freq(self, freq:float, unit:Literal['Hz', 'kHz', 'MHz', 'GHz']):
        """
        设置频率
        :param freq: 0.1
        :param unit: 频率单位
        :return:
        """
        self.write(f'FREQ {freq}{unit}')
        time.sleep(0.001)


    def query_freq(self):
        freq = self.query(f'FREQ:OFF?')
        return freq

    def set_power(self, power=-10):
        """
        设置功率大小
        :param power: 设置功率大小
        :return:
        """
        self.write(f'POW {power}')
        time.sleep(0.001)

    def set_output(self, output:Literal['ON', 'OFF']):
        """
        设置输出开关
        :param output: ON,OFF
        :return:
        """
        self.write(f'OUTP {output}')
        time.sleep(0.001)




if __name__ == '__main__':
    E8257d = KeysightE8257D(config_path="config.yaml")
    E8257d.set_freq(1, 'GHz')
    E8257d.set_power(0)
    E8257d.close()
