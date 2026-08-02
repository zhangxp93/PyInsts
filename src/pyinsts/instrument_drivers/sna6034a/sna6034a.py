# 控制zna
import logging
import time
from typing import Literal, Optional, Union


from pyinsts.instrument_drivers import BaseInstrument


# 定义instrument类，连接instrument频谱仪
class Sna6034a(BaseInstrument):
    def __init__(self, address: Optional[str] = None, config_path="config.yaml", model: str = "SNA6034A"):
        super().__init__(address=address, config_path=config_path, model=model)

    def set_clear_status(self) -> None:
        """
        清除仪器输出缓存区
        :return:
        """
        self.write('*CLS')
        logging.info('清除仪器缓存')

    def set_preset(self) -> None:
        """
        复位
        :return:
        """
        self.write('*RST', opc=True)
        logging.info('复位')

    def set_trace(self, trace):
        """
        设置TRACE
        :return:
        """
        self.write(f'CALC:PAR:SEL "{trace}"')

    def query_marker(self):
        """
        设置读取MARKER
        :param x: 1,2,3,....
        :return:
        """
        marker_value = self.query('CALC:MARK:Y?')
        return marker_value

    def set_arbitrary_power(self, port, power_offset):
        """
        功率补偿，增加减小dB
        :param port:
        :param power_offset:
        :return:
        """
        self.write(f'SOUR:POW{port}:OFFS {power_offset}, ONLY;')

    def set_power(self, power):
        """
        设置功率
        :param power:
        :return:
        """
        self.write(f"SOUR:POW {power}")

    def save_csv_png(self, filename):
        """
        存csv与png
        :param filename: 文件名需包含路径，'Z:\\DATA\\186_5514\\186_5514_SIOA201P8_GND_REF300_12000_+35'
        :return:
        """
        self.write(f'MMEMory:STORe:FDATa "{filename}.csv"')
        self.write(f'MMEMory:STORe:IMAGe "{filename}.png"')
        print('save_csv_png 运行完成')
    def close(self):
        super().close()




if __name__ == '__main__':
    from pyinsts.data import setup_logging
    setup_logging()
    sna6034a =Sna6034a(address='TCPIP0::172.16.30.196::inst0::INSTR')
    sna6034a.save_csv_png(f'U-disk0/3840/1')