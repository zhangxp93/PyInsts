# 控制e36312a子程序
import logging
from typing import Literal

from pyinsts.instrument_drivers import BaseInstrument


# 定义e36312a类，连接e36312a电源
class KeysightE36312A(BaseInstrument):
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "E36312A"):
        super().__init__(address=address, config_path=config_path, model=model)

        self.set_clear_status()

    def set_clear_status(self) -> None:
        """
        清除仪器输出缓存区
        :return:
        """
        self.write('*CLS')
        logging.info('清除仪器缓存')

    def set_channel(self, channel):
        """
        设置通道
        :param channel:
        P6V:1
        P25V:2
        N25V:3
        :return:
        """
        self.write(f"INST CH{channel}")
        logging.info(f"成功选择{self.model}通道CH{channel}")

    def set_volt(self, voltage):
        """
        设置instrument电压
        :param voltage:
        :return:
        """
        self.write(f"VOLT {voltage}")
        logging.info(f"成功设置{self.model}电压为{voltage}V")

    def set_curr(self, set_current):
        """
        设置instrument限流电流,A
        :param set_current:
        :return:
        """
        self.write(f"CURR {set_current}")
        logging.info(f"成功设置{self.model}限流电流为{set_current}A")

    def query_curr(self, ch: Literal[1,2,3], unit: Literal['mA', 'A'] = 'mA'):
        """
        设置instrument限流电流
        :param unit:
        :param ch:
        P6V:CH1
        P25V:CH2
        N25V:CH3
        :return:
        """
        try:
            if unit == 'mA':
                curr = float(self.query(f"MEAS:CURR? CH{ch}")) * 1000
            else:
                curr = float(self.query(f"MEAS:CURR? CH{ch}"))
            return curr
        except Exception as e:
            logging.error(f'读取电流失败：{e}')
            return -99

    def query_volt(self, ch):
        """
        读取设置电压
        :param ch:
        P6V:CH1
        P25V:CH2
        N25V:CH3
        :return:
        """
        query_volt = float(self.query(f"MEAS:VOLT? CH{ch}"))
        return query_volt

    def set_output(self, switch:Literal[0,1]):
        """
        打开E36312开关设置
        :return:
        """
        self.write(f"OUTP {switch}")
        logging.info(f"成功设置{self.model}输出开关为{switch}")



class KeysightE36312ASetMeas(KeysightE36312A):
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "E36312A"):
        super().__init__(address=address, config_path=config_path, model=model)

    def set_volt_curr(self, switch:Literal[0,1], ch:Literal[1,2,3], volt:float, curr: float):
        """
        instrument设置电压、限流电流
        :param switch: 设置电源开关
        :param ch: 选择设置通道
        :param volt: 设置电压值
        :param curr: 设置限流值A
        :return:
        """
        self.set_channel(str(ch))
        if volt is not None:
            self.set_volt(volt)
        if curr is not None:
            self.set_curr(curr)
        self.set_output(switch)

    def set_on_off(self, switch:Literal[0,1], ch:Literal[1,2,3]):
        """
        instrument设置电压、限流电流
        :param switch: 设置电源开关
        :param ch: 选择设置通道
        :return:
        """
        self.set_channel(str(ch))
        self.set_output(switch)

    def meas_volt_curr(self, switch:Literal[0,1], ch:Literal[1,2,3]):
        """
        instrument测量电压、电流
        :param switch: 设置电源开关
        :param ch: 选择设置通道
        :return: 返回测试的电压值V,电流值mA
        """
        self.set_channel(str(ch))
        self.set_output(switch)
        return self.query_volt(str(ch)), self.query_curr(ch, 'mA')


    
if __name__ == '__main__':
    # e36312a = E36312aSetMeas(config_path="E:\\PycharmProjects\\RFChipTest\\config\\instrument_drivers\\instr_config.yaml",)
    from src.pyinsts.data import setup_logging
    setup_logging()
    e36312a = KeysightE36312ASetMeas(address='USB0::0x2A8D::0x1102::MY61002582::INSTR', model='E36312A')
    # instrument.set_volt_curr(0,2,6,0.3)
    # a = instrument.meas_volt_curr(1,1)
    # instrument.set_output(0)

    a = e36312a.query_curr(3)
    b = e36312a.query_volt(3)
    print(a)
    print(b)
    e36312a.close()
    # print(a)


