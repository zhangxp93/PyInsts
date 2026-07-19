from typing import  Literal

import time
import logging

from pyinsts.instrument_drivers import BaseInstrument


class KeysightN9030B(BaseInstrument):
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "N9030B"):
        super().__init__(address=address, config_path=config_path, model=model)

        self.model = model
    def set_mode_spectrum_analyzer(self, mode:Literal["SAN"]):
        """
        设置频谱模式
        :param mode:
        :return:
        """
        self.write(f'CONF:{mode}; *WAI')  # 设置后使用 *WAI 等待命令执行完成 {mode}')

    def set_freq(self, freq:float, unit:Literal['GHz', 'MHz', 'kHz', 'Hz']):
        """
        设置频率
        :param unit:
        :param freq:
        :return:
        """

        self.write(f'SENS:FREQ {freq}{unit}')
        logging.info(f'设置频率: {freq}{unit}')

    def set_freq_cent(self, freq:float, unit:Literal['GHz', 'MHz', 'kHz', 'Hz']):
        """
        设置中心频率
        :param unit:
        :param freq:
        :return:
        """

        self.write(f'FREQ:CENT {freq}{unit}',True)
        logging.info(f'设置中心频率: {freq}{unit}')


    def set_freq_span(self, freq:float , unit:Literal['GHz', 'MHz', 'kHz', 'Hz']):
        """
        设置频谱的跨度 (span)，单位为 GHz
        :param unit:
        :param freq:
        :return:
        """

        self.write(f'FREQ:SPAN {freq}{unit}; *WAI')  # 设置后使用 *WAI 等待命令执行完成

        logging.info(f'已设置频谱跨度为: {freq}{unit}')


    def set_freq_span_max(self):
        """
        设置频谱的跨度 (span)为最大
        :return:
        """
        self.write(f'FREQ:SPAN MAX; *WAI')  # 设置后使用 *WAI 等待命令执行完成
        time.sleep(0.001)  # 稍作延迟以确保指令被正确执行
        logging.info(f'已设置频谱跨度为max')

    def set_freq_start(self, freq: float, unit:Literal['GHz', 'MHz', 'kHz', 'Hz']):
        """
        设置开始频率
        :param unit:
        :param freq:
        :return:
        """

        self.write(f'FREQ:STAR {freq}{unit}')
        logging.info(f'设置起始频率: {freq}{unit}')


    def set_freq_stop(self, freq: float, unit:Literal['GHz', 'MHz', 'kHz', 'Hz']):
        """
        设置截止频率
        :param unit:
        :param freq:
        :return:
        """

        self.write(f'FREQ:STOP {freq}{unit}')
        logging.info(f'设置结束频率: {freq}{unit}')


    def set_ref_level(self, level: float):
        """
        设置参考电平 (Reference Level)
        :param level: 参考电平值，单位 dBm
        :return:
        """

        self.write(f'DISP:WIND:TRAC:Y:RLEV {level}dBm')  # 设置参考电平
        logging.info(f'已设置参考电平为: {level} dBm')


    def set_auto_tune(self):
        """
        自动设置参考电平
        :return:
        """

        self.write('SENS:FREQ:TUNE:IMM; *WAI')  # 设置后使用 *WAI 等待命令执行完成
        logging.info('已设置自动调频')

    def set_rbw(self, rbw: float, unit:Literal['MHz', 'kHz', 'Hz']):
        """
        设置分辨带宽 (Resolution Bandwidth, RBW)
        :param rbw: 分辨带宽值
        :param unit:
        :return:
        """
        self.write(f'BAND:RES {rbw}{unit}; *WAI')  # 设置后使用 *WAI 等待命令执行完成
        logging.info(f'已设置分辨带宽为: {rbw}{unit}')


    def set_rbw_auto(self):
        """
        设置自动rbw
        :return:
        """
        try:
            self.write('BWID:AUTO ON')  # 设置 RBW 为自动模式并等待
            logging.info('已将分辨率带宽设置为自动模式')
        except Exception as e:
            logging.error(f"设置 RBW 时发生错误: {e}")


    def set_vbw(self, vbw: float, unit:Literal['MHz', 'kHz', 'Hz']):
        """
        设置视频带宽 (Video Bandwidth, VBW)
        :param vbw: 视频带宽值
        :param unit: 带宽的单位，默认是 Hz（可选 kHz, MHz）
        :return:
        """

        try:
            # 构建 SCPI 命令
            self.write(f'BAND:VID {vbw}{unit}; *WAI')  # 设置后使用 *WAI 等待命令执行完成
            logging.info(f'已设置视频带宽为: {vbw} {unit}')
        except Exception as e:
            logging.error(f"设置视频带宽时发生错误: {e}")

    def set_vbw_auto(self):
        """
        自动设置vbw
        :return:
        """

        try:
            self.write('BAND:VID AUTO; *WAI')  # 设置 VBW 为自动模式并等待
            logging.info('已将视频带宽设置为自动模式')
        except Exception as e:
            logging.error(f"设置 VBW 时发生错误: {e}")


    def set_peak_search(self):
        """
        peak search
        :return:
        """
        self.instrument.write(f"CALC:MARK1:MAX:PEAK")
        logging.info('执行peak search')
    def set_next_peak(self):
        """
        next peak
        :return:
        """
        self.write(f"CALC:MARK1:MAX:NEXT")
        logging.info('执行next peak')

    def set_marker_freq(self, frequency: float,unit: Literal['GHz', 'MHz', 'kHz', 'Hz'] = 'Hz', mark_number: int = 1):
        """
        设置指定mark标记的频率
        :param unit:
        :param frequency: 频率值
        :param mark_number: 标记编号，默认为 1
        :return:
        """
        try:
            self.write(f'CALC:MARK{mark_number}:FREQ {frequency}{unit}; *WAI')  # 设置指定标记的频率并等待
            logging.info(f'已将标记{mark_number}的频率设置为: {frequency}{unit}')
        except Exception as e:
            logging.error(f"设置标记{mark_number}频率时发生错误: {e}")

    def set_mark_delt_on(self, x):
        """
        开启delt标记
        :param x:
        :return:
        """
        self.write(f"CALC:MARK{x}:MODE DELT")
        logging.info(f'开启delt标记: MARK{x}')

    def set_mark_all_off(self):
        """
        关闭所有mark
        :return:
        """
        self.write(f"CALC:MARK:AOFF")
        logging.info('关闭所有标记')


    def set_mark_del_freq(self, mark_number: int, freq:float, unit: Literal['GHz', 'MHz', 'kHz', 'Hz']):
        """
        delt频率
        :param unit:
        :param mark_number:1,2,3
        :param freq:
        :return:
        """

        self.write(f"CALC:MARK{mark_number}:X {freq}{unit}")
        logging.info(f'设置MARK{mark_number}的delt频率为: {freq}{unit}')


    def query_mark_delta_x(self, mark_number: int, unit: Literal['GHz', 'MHz', 'kHz', 'Hz']):
        """
        读取mark delt
        :param mark_number:
        :param unit:
        :return:
        """
        value = self.query(f'CALC:MARK{mark_number}:X?')
        if unit == 'GHz':
            value = float(value) / 1e9
        elif unit == 'MHz':
            value = float(value) / 1e6
        elif unit == 'kHz':
            value = float(value) / 1e3
        elif unit == 'Hz':
            value = float(value)
        logging.info(f'读取MARK{mark_number}的偏移频率: {value}{unit}')
        return value, unit


    def query_mark_x_freq(self, mark_number: int, unit: Literal['GHz', 'MHz', 'kHz', 'Hz']):
        """
        读取mark频率
        :param mark_number:
        :param unit:
        :return: 返回频率值和单位
        """

        value = self.query(f"CALC:MARK{mark_number}:X?")
        if unit == 'GHz':
            value = float(value.replace("\n", "").replace("\r", "")) / 1e9  # 删除字符串中的换行符和回车符
        elif unit == 'MHz':
            value = float(value.replace("\n", "").replace("\r", "")) / 1e6
        elif unit == 'kHz':
            value = float(value.replace("\n", "").replace("\r", "")) / 1e3
        elif unit == 'Hz':
            value = float(value.replace("\n", "").replace("\r", ""))
        logging.info(f'读取MARK频率为:{value}{unit}')
        return value, unit


    def query_mark_y_power(self):
        """
        读取mark功率,单位dBm
        :return:
        """
        value = self.query(f"CALC:MARK:Y?")
        value = float(value.replace("\n", "").replace("\r", ""))  # 删除字符串中的换行符和回车符
        logging.info(f'读取MARK频率为:{value} dBm')
        return value

    def set_peak_search_continuous_on(self):
        """
        设置peak search连续最终打开
        :return:
        """
        self.write(f"CALC:MARK:CPS ON")
        logging.info(f'set_peak_search_continuous 成功')

    def set_mark_to_cf(self,mark_number: int = 1):
        """
        将指定mark设置到中心频率
        :param mark_number:
        :return:
        """
        self.write(f"CALC:MARK{mark_number}:CENT")
        logging.info(f'CALC:MARK{mark_number}:CENT 成功')


    def save_png(self, file_path):
        """
        保存数据图片和csv文件
        :param file_path:
        :return:
        """
        self.write(f'MMEM:STOR:TRAC:DATA TRACE1, "{file_path}.csv"; *WAI')
        self.write(f'MMEM:STOR:SCR "{file_path}.PNG"; *WAI')

        logging.info(f'保存屏幕截图到: {file_path}.PNG')

        time.sleep(1)

    def set_single(self):
        """
        单次运行
        :return:
        """
        self.write(f"INIT:CONT 0")
        logging.info(f'set_single 成功')


    def set_cont(self):
        """
        连续运行
        :return:
        """
        self.write(f"INIT:CONT 1")
        logging.info(f'set_cont 成功')

    def set_cal_all(self):
        """
        自校准all
        :return:
        """
        self.write(f"*CAL?",True)
        logging.info(f'自校准all 成功')

    def close(self):
        """
        关闭仪器端口
        :return:
        """
        self.close()
        logging.info(f'关闭频谱仪{self.model}端口')


if __name__ == '__main__':
    n9030b = KeysightN9030B(address="USB0::0x2A8D::0x1D0B::MY55480187::INSTR", model='N9030B')
    n9030b.set_rbw_auto()
    # n9030b.set_cal_all()
    # y1 = n9030b.query_mark_y_power()
    # for i in range(100):
    #     time.sleep(1)
    #     i += 1
    #     print(f"{i}:y1")
    # n9030b.set_cont()
    # time.sleep(5)
    # n9030b.set_single()
    # keysight_sp.set_freq_start(19)
    # keysight_sp.set_freq_stop(25)
    # keysight_sp.set_mark_aoff()  # 开始前关闭所有marker
    # keysight_sp.set_rbw(100000)
    # time.sleep(1)
    # keysight_sp.set_peak_search()
    # keysight_sp.set_mark_to_cf()
    # keysight_sp.set_freq_span(10)
    # keysight_sp.set_rbw(3000)
    # time.sleep(4)
    # keysight_sp.set_peak_search()
    # freq = keysight_sp.query_mark_x_freq()
    # power = keysight_sp.query_mark_y_power()
    # print(freq, power)

    # 杂散1
    # keysight_sp.set_freq_start(freq * 7/8 - 1.2)
    # keysight_sp.set_freq_stop(freq + 1.2)
    # keysight_sp.set_rbw(1000)
    # time.sleep(2)
    # keysight_sp.set_peak_search()
    # freq = keysight_sp.query_mark_x_freq()
    # keysight_sp.set_mark_del_on(1)
    # keysight_sp.set_next_peak()
    # # keysight_sp.set_mark_del_freq(1, freq*1000*7/8-freq*1000)
    # za_freq1 = (keysight_sp.query_mark_delt_x(1)) / 1000
    # za_power1 = keysight_sp.query_mark_y_power()
    # print(za_freq1, za_power1)



    # keysight_sp.set_freq_cent(freq_set/1000)  # 设置中文频率
    # # 鉴相杂散
    # keysight_sp.set_freq_span(0.5)
    # keysight_sp.set_rbw(3000)
    # time.sleep(2)
    # keysight_sp.set_peak_search()
    # freq = keysight_sp.query_mark_x_freq()
    # print(freq)
    # keysight_sp.set_mark_del_on(1)
    # keysight_sp.set_mark_del_freq(1,-200)
    # za_freq1 = keysight_sp.query_mark_delt_x(1)
    # za_power1 = keysight_sp.query_mark_y_power()
    # keysight_sp.save_png(f"{freq_set}_-200M")
    # keysight_sp.set_mark_del_freq(1, 200)
    # za_freq2 = keysight_sp.query_mark_delt_x(1)
    # za_power2 = keysight_sp.query_mark_y_power()
    # keysight_sp.save_png(f"{freq_set}_+200M")
    # print(za_freq1,za_power1)
    # print(za_freq2,za_power2)
    #
    # # # # 小数杂散
    # keysight_sp.set_mark_aoff()
    # keysight_sp.set_freq_span(0.00001)
    # keysight_sp.set_rbw(100)
    # time.sleep(5)
    # keysight_sp.set_peak_search()
    # freq = keysight_sp.query_mark_x_freq()
    # print(freq)
    # keysight_sp.set_mark_del_on(1)
    # keysight_sp.set_mark_del_freq(1, -0.0008)
    # xza_freq1 = keysight_sp.query_mark_delt_x(1)
    # xza_power1 = keysight_sp.query_mark_y_power()
    # keysight_sp.save_png(f"{freq_set}_-800Hz")
    # keysight_sp.set_mark_del_freq(1, 0.0008)
    # xza_freq2 = keysight_sp.query_mark_delt_x(1)
    # xza_power2 = keysight_sp.query_mark_y_power()
    # keysight_sp.save_png(f"{freq_set}_800Hz")
    # print(za_freq1, za_power1)
    # print(za_freq2, za_power2)



    # keysight_sp.set_peak_search_continuous_on()
    # freq = keysight_sp.query_mark_x_freq()
    # power = keysight_sp.query_mark_y_power()
    # print(freq,power)
    # keysight_sp.save_png('SIV111')

    # keysight_sp.set_ref_level(10)
    # # 主频设置
    # keysight_sp.set_freq_span('max')
    # time.sleep(1)
    # keysight_sp.set_mark_to_cf()
    # keysight_sp.set_freq_span(0.1)
    # time.sleep(0.5)
    # keysight_sp.set_mark_to_cf()
    # time.sleep(1)
    # frequency_1 = keysight_sp.query_mark_x_freq()
    # mark_power_1 = keysight_sp.query_mark_y_power()
    # print(frequency_1)
    # print(mark_power_1)
    # if frequency_1 * 2 < 40:
    #     # 二次谐波
    #     keysight_sp.set_freq_cent(frequency_1*2)
    #     time.sleep(0.5)
    #     keysight_sp.set_mark_to_cf()
    #     time.sleep(1)
    #     frequency_2 = keysight_sp.query_mark_x_freq()
    #     mark_power_2 = keysight_sp.query_mark_y_power()
    #     print(frequency_2)
    #     print(mark_power_2)
    # else:
    #     frequency_2 = -99
    #     mark_power_2 = -99
    #     print(frequency_2)
    #     print(mark_power_2)
    #     print('频率超过40G')
    #
    # if frequency_1*3 < 40:
    #     # 三次谐波
    #     keysight_sp.set_freq_cent(frequency_1 * 3)
    #     time.sleep(0.5)
    #     keysight_sp.set_mark_to_cf()
    #     time.sleep(1)
    #     frequency_3 = keysight_sp.query_mark_x_freq()
    #     mark_power_3 = keysight_sp.query_mark_y_power()
    #     print(frequency_3)
    #     print(mark_power_3)
    #     keysight_sp.close()
    # else:
    #     frequency_3 = -99
    #     mark_power_3 = -99
    #     print(frequency_3)
    #     print(mark_power_3)
    #     print('频率超过40G')
    # keysight_sp.close()