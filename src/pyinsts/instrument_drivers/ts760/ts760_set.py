import time
from typing import Literal

from pyinsts.data import load_config
from pyinsts.instrument_drivers import Ts760


class Ts760Set:
    def __init__(self, server_ip:str=None, config_path="config.yaml",server_port=8000):
        self.ts760 = None
        if server_ip:
            self.server_ip = server_ip
            self.server_port = server_port
        else:
            self.config = load_config(config_path)
            # 明确从 TS760 配置中提取 server_ip 和 server_port
            self.ts760_config = self.config.get("instruments_address", {}).get("TS760", {})
            self.server_ip = self.ts760_config.get("server_ip")  # 使用子键
            self.server_port = self.ts760_config.get("server_port")  # 使用子键
            print("ip:",self.server_ip,"port:",self.server_port)
            if not self.ts760_config:
                raise ValueError("仪器地址未在配置文件中找到")
        self.ts760 = Ts760(self.server_ip, self.server_port)
    def set_temp(self, set_temp=25, run_flwm:int=6, test_flwm:int=4, time_sleep:int=50):
        # 设置温度,设置地址
        print('temp:', set_temp)
        with self.ts760:
            self.ts760.set_temp(set_temp)   # 温度设置
        with self.ts760:
            self.ts760.set_flwm(run_flwm)  # 设置吹气流量
        with self.ts760:
            self.ts760.set_soak(9999)   # 温度保持时间
        with self.ts760:
            self.ts760.set_flow_on_off(1)   # 打开吹气

        while True:
            with self.ts760:
                temp = self.ts760.query_dut_temp()  # 读取dut温度
            temp = float(temp)
            time.sleep(1)
            with self.ts760:
                query_set_temp = self.ts760.query_set_setp()
            if query_set_temp != set_temp:
                print('温度设置错误')
                with self.ts760:
                    self.ts760.set_temp(set_temp)
            temp = float(temp)
            if set_temp - 0.5 <= temp <= set_temp + 0.5:
                print('温度已达到')
                with self.ts760:
                    self.ts760.set_flwm(test_flwm)  # 设置吹气流量
                time_sleep = time_sleep
                for i in range(time_sleep):
                    time.sleep(1)
                    print(f'等待{time_sleep - i}s')
                self.ts760.close()
                while True:
                    with self.ts760:
                        temp = self.ts760.query_dut_temp()  # 读取dut温度
                    temp = float(temp)
                    time.sleep(1)
                    if set_temp - 0.5 <= temp <= set_temp + 0.5:
                        temperature1 = '+' + str(set_temp) if set_temp > 0 else str(set_temp)
                        # 开始测试
                        print('测试温度', temperature1)
                        time.sleep(0.1)
                        time_sleep = 5
                        for i in range(time_sleep):
                            time.sleep(1)
                            print(f'等待{time_sleep - i}s')
                        break
                    else:
                        time_sleep = 5
                        for i in range(time_sleep):
                            time.sleep(1)
                            print(f'等待{time_sleep - i}s')
                break

    def set_flow_on_off(self, on_off: Literal[1, 0]):
        """

        :param on_off:  0关闭,1打开
        :return:
        """
        with self.ts760:
            self.ts760.set_flow_on_off(on_off)

    def set_head(self, value: Literal[0, 1]):
        """
        设定head升降:0升，1降
        :param value: 0,1
        :return:
        """
        with self.ts760:
            self.ts760.set_head(value)

    def set_to_load(self):
        with self.ts760:
            self.ts760.set_to_load()




if __name__ == '__main__':
    temperature_list = [25]
    ts760set = Ts760Set(config_path="config.yaml")
    ts760set.set_temp(set_temp=temperature_list[0], run_flwm=6, test_flwm=4)
