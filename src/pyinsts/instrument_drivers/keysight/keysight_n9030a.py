from typing import  Literal

import time
import logging

from .keysight_n9030b import KeysightN9030B


class KeysightN9030A(KeysightN9030B):
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "N9030A"):
        super().__init__(address=address, config_path=config_path, model=model)

        self.model = model




if __name__ == '__main__':
    addr_n9030a = "TCPIP0::K-N9030A-10593::inst0::INSTR"
    n9030a = KeysightN9030A(addr_n9030a)
    n9030a.set_freq_cent(20,'GHz')
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