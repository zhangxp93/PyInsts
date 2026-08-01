import logging
from typing import Literal, Optional

from pyinsts.instrument_drivers import BaseInstrument


class PowerMeter(BaseInstrument):
    def __init__(self, address: Optional[str] = None, config_path: str = "config.yaml", model: str = "N1914A"):
        """
        功率计类
        :param address: 仪器VISA地址，如果提供，则优先使用此地址。
        :param config_path: 配置文件路径，用于查找仪器地址（如果address未提供）。
        :param model: 仪器型号，用作在配置文件中查找地址的键。
        """
        super().__init__(address=address, config_path=config_path, model=model)
        logging.info(f"PowerMeter instance created for model {model}")

    def set_freq(self, freq: float, unit: Literal["Hz", "kHz", "MHz", "GHz"]):
        """
        设置频率
        :param unit:
        :param freq:
        :return:
        """
        self.write(f'SENS:FREQ {freq}{unit}')

    def query_power(self) -> float:
        """
        读取功率
        :return: float, a power value
        """
        power_str = self.query(f'FETC?')
        return float(power_str)



if __name__ == '__main__':
    n1914a = PowerMeter(config_path="config.yaml",model="N1914A")
    n1914a.set_freq(20,'GHz')
    power = n1914a.query_power()
    print(power)

