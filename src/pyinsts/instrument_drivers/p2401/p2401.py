"""
p2401.py

该模块定义了一个用于控制P2401精密电源的Python类P2401。
通过该类，用户可以设置电压和电流、读取电压和电流值、开启和关闭输出等操作。
"""

from typing import Literal

import logging


import pyvisa
import pyvisa.constants
import time

from pyinsts.instrument_drivers import BaseInstrument


# 定义2401类，连接2401精密电源
class P2401(BaseInstrument):
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "P2401"):
        """
        设置2401仪器地址，连接2401精密电源
        :param address:
        """
        super().__init__(address=address, config_path=config_path, model=model)
        self._ren()

    def _ren(self):
        # 设置ren
        self.rm.visalib.gpib_control_ren(self.instrument.session,pyvisa.constants.VI_GPIB_REN_ASSERT)
    def set_voltage(self, voltage):
        """
        设置电压,单位V
        :param voltage:
        :return:
        """
        self.write(f'SOUR:VOLT:LEV {voltage}')
        logging.info(f'设置2401电压为{voltage}V')
        time.sleep(0.001)

    def set_curr_limit(self, curr_limit:float,unit:Literal['A','mA']='A'):
        """
        设置限流,单位A
        :param curr_limit:
        :param unit:
        :return:
        """
        if unit == 'A':
            self.write(f'SENS:CURR:PROT {curr_limit}')
        elif unit == 'mA':
            self.write(f'SENS:CURR:PROT {curr_limit/1000}')
        time.sleep(0.001)

    def query_volt(self):
        """
        读取电压v
        :return:
        """
        volt_curr = self.query('MEAS?')
        volt_curr = volt_curr.split(',')
        volt1 = [volt_curr[i] for i in range(0, len(volt_curr), 5)]
        volt1 = [float(i) for i in volt1]
        time.sleep(0.001)
        return volt1

    def query_curr(self):
        """
        读取电流uA
        :return:
        """
        volt_curr = self.query('MEAS?')
        print('电流', volt_curr)
        volt_curr = volt_curr.split(',')
        curr1 = [volt_curr[i] for i in range(1, len(volt_curr), 5)]

        curr1 = [float(i) * 1e6 for i in curr1]
        time.sleep(0.001)
        return curr1

    def set_output_on(self):
        """
        设置输出开
        :return:
        """
        self.write('OUTP ON')
        time.sleep(0.001)

    def set_output_off(self):
        """
        设置输出关
        :return:
        """
        self.write('OUTP OFF')
        time.sleep(0.001)



class P2401SetMeas(P2401):
    def __init__(self, instrument_address: str = None, config_path="config.yaml"):
        super().__init__(config_path="config.yaml")
    def meas_vt_curr(self, vt_list: list[float], curr_limit: float, unit:Literal['A','mA']='mA'):
        """
        测试vt电流
        :param unit:
        :param vt_list: 测试电压，列表[0,1,2,3]
        :param curr_limit: 限流mA
        :return: 电压列表和电流列表
        """

        self.set_curr_limit(curr_limit,unit)
        meas_vt_list = []
        meas_curr_list = []
        try:
            for vt in vt_list:
                # 设置电压并读取电流
                time.sleep(0.01)
                self.set_voltage(vt)
                self.set_output_on()
                time.sleep(0.1)
                curr = self.query_curr()
                meas_vt_list.append(vt)
                meas_curr_list.append(curr)
                time.sleep(0.01)

            # 最后将电压设置为0并关闭输出
            self.set_voltage(0)
            time.sleep(0.01)
            self.set_output_off()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.close()

        return meas_vt_list,meas_curr_list

if __name__ == '__main__':
    # p2401 = P2401(address='GPIB0::24::INSTR')
    p2401 = P2401(address="USB0::0x05E6::0x2612::4102646::INSTR")
    # p2401.meas_volt_curr([0, 1, 2, 3], 0.1)
    p2401.set_output_on()
    vt_curr = p2401.query_curr()
    print(vt_curr)
    p2401.set_output_off()
    # p2401.close()
