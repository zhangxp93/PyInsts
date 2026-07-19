"""
控制E5052B子程序
"""

import logging
import time
from typing import Literal

from pyinsts.instrument_drivers import BaseInstrument


# 定义E5052b类，连接E5052b信号源分析仪
class KeysightE5052B(BaseInstrument):
    def __init__(self, address: str = None, config_path="config.yaml",model:str = "E5052B"):
        super().__init__(address=address, config_path=config_path, model=model)

    def set_input_port(self, downconverter:Literal['ON','OFF'], rf_input:Literal['DCON','DIR']):
        """
        设置E5052b输入端口
        :param downconverter:ON开启下变频，OFF关闭下变频；
        :param rf_input:DCON下变频，DIR E5052b；
        """
        self.write(f"SENS:DCON {downconverter}")
        self.write(f"SENS:DCON:INP {rf_input}")

    def set_trigger_mode(self, mode:Literal['FP','PN','SP','TR']):
        """
        设置E5052B触发模式，测试模式。
        :param mode:
        FP:Frequency Power;
        PN:Phase Noise;
        SP:Spectrum Monitor;
        TR:Transient;
        BB:Baseband Noise;
        AM:AM Noise;
        PS:Segment PN;
        :return:
        """
        self.write(f"TRIG:MODE {mode}1")
        time.sleep(0.01)
        logging.info(f'成功触发E5052B,触发模式:{mode}')


    def set_display_meas_view(self, view:Literal['FP','PN','SP','TR']):
        """
        显示E5052B测量视图
        :param view:
        FP:Frequency Power;
        PN:Phase Noise;
        SP:Spectrum Monitor;
        TR:Transient;
        BB:Baseband Noise;
        AM:AM Noise;
        PS:Segment PN;
        :return:
        """
        self.write(f"DISP:WIND:ACT {view}1")

    def set_dc_power_output(self, value:Literal['ON','OFF']):
        """
        设置set_dc_power_output开关
        :param value: ON,OFF
        :return:
        """
        self.write(f"SOUR:VOLT:POW:LEV:STAT {value}")

    def set_dc_control_output(self, value:Literal['ON','OFF']):
        """
        设置dc_control_output开关
        :param value: ON,OFF
        :return:
        """
        self.write(f"SOUR:VOLT:CONT:LEV:STAT {value}")

    def query_fp_trace(self, trace: int):
        """
        读取fp模式trace数据
        :param trace:1,2,3,4
        :return:
        """
        value = self.query(f"CALC:FP:TRAC{trace}:DATA:FDATA?")
        return value

    def set_dc_power_voltage(self, value: float):
        """
        设置set_dc_power_voltage 电压
        :param value: ON,OFF
        :return:
        """
        self.write(f"SOUR:VOLT:POW:LEV:AMPL  {value}")

    def set_fp_frequency_band(self, band):
        """
        设置频率band
        :param band:
        band3:3G-10G
        band4:9G-26.5G
        :return:
        """
        self.write(f"SENS:FP:FBAN BAND{band}")

    def set_fp_nominal_frequency(self, freq):
        """
        fp模式设置nominal频率,HZ
        :param freq:
        :return:
        """
        self.write(f"SENS:FP:DCON:FREQ {freq}")

    def set_pn_nominal_frequency(self, freq):
        """
        pn模式设置nominal频率
        :param freq:
        :return:
        """
        self.write(f"SENS:pn:DCON:FREQ {freq}")

    def set_sp_center_frequency(self, center):
        """
        sp模式设置中心频率,单位Hz
        :param center:
        :return:
        """
        self.write(f"SENS:SP:FREQ:CENT {center}")

    def query_sp_marker(self, marker):
        """
        读取marker值
        :param marker:
        :return:
        """
        value = self.query(f"CALC:SP:TRAC:MARK{marker}:Y?")
        time.sleep(0.01)
        return value

    def query_pn_carrier_freq(self):
        """
        读取pn模式下频率
        :return:
        """
        value = self.query(f"CALC:PN:DATA:CARR?")
        value = float(value.split(',')[0]) / 1e9
        time.sleep(0.01)
        return value

    def query_pn_carrier_power(self):
        """
        读取pn模式下功率
        :return:
        """
        value = self.query(f"CALC:PN:DATA:CARR?")
        value = float(value.split(',')[1])
        time.sleep(0.01)
        return value

    def query_pn_marker(self, marker):
        """
        读取相位噪声maker
        :return:
        """
        value = self.query(f"CALC:PN:TRAC:MARK{marker}:Y?")
        time.sleep(0.001)
        return float(value)

    def set_pn_marker(self, marker, value):
        """
        设置相位噪声maker
        :return:
        """
        value = self.write(f"CALC:PN:TRAC:MARK{marker} {value}")
        time.sleep(0.001)
        return float(value)

    def set_pn_marker_on(self, marker):
        """
        设置相位噪声maker
        :return:
        """
        value = self.write(f"CALC:PN:TRAC:MARK{marker}:STAT ON")
        time.sleep(0.001)
        return float(value)

    def set_dc_control_voltage(self, voltage):
        """
        设置vt电压,已等待
        :param voltage:
        :return:
        """
        self.write(f"SOUR:VOLT:CONT:LEV:AMPL {voltage}")
        time.sleep(1)

    def set_carrier_search(self):
        self.write(f"SENS:PN:DCON:SSE:EXEC")
        time.sleep(0.01)

    def set_pn_frequency_band(self, band:Literal[1,2,3,4,5,6]):
        """
        设置E5052B频率band
        :param band:
        band1:1M-41M
        band2:39M-101M
        band3:99M-1.5G
        band4:250M-7G
        band5:3G-10G
        band6:9G-26.5G
        :return:
        """
        self.write(f"SENS:PN:FBAN BAND{band}")
        time.sleep(0.01)

    def set_save_csv_png(self,path:str):
        """
        保存csv与图片
        :param path:
        :return:
        """
        self.write(f"MMEMory:PN1:TRAC:STOR '{path}.csv'")
        self.write(f"MMEMory:STORe:IMAGe '{path}.png'")




if __name__ == '__main__':
    addr = "USB0::0x0957::0x1F01::MY11111::0::INSTR"
    e5052b = KeysightE5052B(config_path="../e5052b/config.yaml", model="E5052B")
    # freq = 11700
    # if freq < 9600:
    #     e5052b.set_pn_frequency_band(5)
    #     e5052b.set_pn_nominal_frequency(freq * 1e6)
    # else:
    #     e5052b.set_pn_frequency_band(6)
    #     e5052b.set_pn_nominal_frequency(freq * 1e6)

    # path = f"F:\\053\\053_10G_1V"
    # e5052b.set_save_csv_png(path)


    # path = f"F:\\SMPL8812SL9\\11.6G"
    # e5052b.set_save_csv_png(path)

    # e5052b.set_pn_marker_on(8)
    # e5052b.set_pn_marker(8, 20000)
    # e5052b.set_pn_marker_on(2)
    # e5052b.set_pn_marker(2, 10000)
    # e5052b.set_pn_marker_on(3)
    # e5052b.set_pn_marker(3, 40000)
    # e5052b.set_pn_marker_on(4)
    # e5052b.set_pn_marker(4, 100000)
    # e5052b.set_pn_marker_on(5)
    # e5052b.set_pn_marker(5, 1000000)
    # e5052b.set_pn_marker_on(6)
    # e5052b.set_pn_marker(6, 10000000)
    # e5052b.set_pn_marker_on(7)
    # e5052b.set_pn_marker(7, 4000)

    # print(e5052b.query_pn_carrier_power())
    # vt = 4
    # e5052b.set_dc_control_voltage(vt)
    # if vt % 1 == 0:
    #     e5052b.set_carrier_search()
    #     time.sleep(8)
    #     # 读取频率
    #     freq = e5052b.query_pn_carrier_freq()
    #     print(freq)

    # e5052b.set_trigger_mode('PN')
    # e5052b.set_dc_power_output('ON')
    # e5250b.set_dc_control_output('OFF')
    # freq = e5052b.query_fp_trace(1)
    # print(freq)
    e5052b.close()