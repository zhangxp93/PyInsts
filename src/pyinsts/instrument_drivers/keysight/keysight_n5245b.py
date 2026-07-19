# N5245b矢量网络分析仪，频率10MHz~50Ghz
import os
import logging
import time

from pyinsts.instrument_drivers import BaseInstrument

# 定义N5242b类，连接N5242b信号源分析仪
# Keysight N52xxB系列网络分析仪帮助文档: https://helpfiles.keysight.com/csg/N52xxB/help.htm#t=Home.htm

class KeysightN5245B(BaseInstrument):
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "N5245B"):
        super().__init__(address=address, config_path=config_path, model=model)

    def set_parameter(self):
        """
        设置读取TRACE
        :return:
        """
        self.write('CALC:PAR:MNUM 1')
        time.sleep(0.001)

    def query_marker(self):
        """
        设置读取MARKER
        :return:
        """
        marker_value = self.query('CALC:MARK:Y?')
        return marker_value

    def set_settings_trace(self, trace: int):
        """
        选择trace
        :return:
        """
        self.write(f'CALC:PAR:MNUM {trace}')

    def query_trace_y(self):
        """
        读取trace y的数据
        :return:
        """
        value = self.query('CALC:DATA? FDATA')
        return value

    def query_trace_x(self):
        """
        读取trace x的数据
        :return:
        """
        value = self.query('CALC:X?')
        return value

    def set_power_level(self, power):
        """
        标准模式，设置power_level功率
        :param power:
        :return:
        """
        self.write(f'SOUR:POW {power}')

    def set_save_png_csv_s2p(self,file_path: str, png: bool = True, csv: bool = True, s2p: bool = True):
        """
        保存图片和csv文件
        :param file_path: 保存路径
        :param png: 是否保存图片
        :param csv: 是否保存csv
        :param s2p: 是否保存s2p
        :return:
        """
        folder_dir = os.path.dirname(file_path) # 获取文件夹路径
        # 检测文件夹是否存在，不存在就创建
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
            logging.info('文件夹已创建')
        else:
            logging.info('文件夹已存在')

        if png:
            self.write(f'HCOPY:FILE "{file_path}.png"') # 保存图片
        if csv:
            self.write(f'MMEM:STOR:DATA "{file_path}.csv","CSV Formatted Data","Displayed","DB",-1') # 保存csv
        if s2p:
            self.write(f'CALC:MEAS:DATA:SNP:PORT:SAVE "1,2","{file_path}.s2p"') # 保存s2p

    def set_channl_alL(self):
        """
        扫描所有通道
        :return:
        """
        self.write('INIT:CONT OFF')
        self.write('TRIG:SCOP ALL')

        # self.write('ABOR')
        self.write('INIT:IMM')
        self.write('INIT:CONT ON')






if __name__ == '__main__':
    # addr = 'USB0::0x2A8D::0x2B01::MY58422180::0::INSTR'
    addr = 'TCPIP0::172.16.30.77::inst0::INSTR'
    n5245b = KeysightN5245B(addr)
    n5245b.set_channl_alL()
    # n5245b.query('opc?')
    # n5245b.set_power_level(-10)

    # n5245b.set_parameter()
    # value = n5245b.query_marker()
    # a = value.split(',')
    # b = float(a[0])
    # print(b)
    # n5245b.set_settings_trace(3)
    # x = n5245b.query_trace_x().split(',')
    # y = n5245b.query_trace_y()
    # n5245b.set_save_png_csv_s2p(f'Y:\\11111111111\\3')

    n5245b.close()
    # print(y)
