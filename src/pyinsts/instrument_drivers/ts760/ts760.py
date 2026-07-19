import socket
import time
from typing import Literal

from pyinsts.data import load_config


class Ts760:
    def __init__(self, server_ip:str=None, config_path="config.yaml",server_port=8000):
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
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(1)    # 增加延时防止连接错误
        max_attempts = 10
        self.server_ip = self.server_ip
        self.server_port = self.server_port

        # 尝试连接到服务器
        self._connect_to_server(max_attempts)

    def _connect_to_server(self, max_attempts:int=10):
        attempt = 0
        while attempt < max_attempts:
            try:
                # 创建 socket 对象
                time.sleep(0.5) # 增加延时防止连接错误
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.settimeout(1)    # 增加延时防止连接错误
                self.client_socket.connect((self.server_ip, self.server_port))
                self.client_socket.send(b"*IDN?")
                response = self.client_socket.recv(1024)
                if response:
                    print(f"收到响应：{response.decode('utf-8')},连接成功")
                    return
                else:
                    raise Exception("没有收到响应")
            except Exception as e:
                print(f"尝试连接失败：{e}，将在2秒后重试...")
                attempt += 1
                time.sleep(2)
        print(f"达到最大尝试次数 {max_attempts}，连接失败。")

    def set_to_load(self):
        """
        切换到本地控制,界面锁定模式将取消
        :return:
        """
        self._connect_to_server()
        self.client_socket.send(f'%GL'.encode('utf-8'))
        time.sleep(0.01)

    def set_to_remote(self):
        """
        切换到远程控制,界面锁定模式将恢复
        :return:
        """
        self._connect_to_server()
        self.client_socket.send(f'%RM'.encode('utf-8'))
        time.sleep(0.01)

    def set_cool(self, value:Literal[0,1]):
        """
        设置制冷压缩机
        :param value: 0，停止制冷压缩机,停止后不具备低温测试功能；1，启动制冷压缩机。
        :return:
        """
        self._connect_to_server()
        self.client_socket.send(f'COOL {value}'.encode('utf-8'))
        time.sleep(0.01)

    def query_cool(self):
        """
        查询制冷压缩机状态
        :return:0，停止制冷压缩机,停止后不具备低温测试功能；1，运行制冷压缩机。
        """
        self._connect_to_server()
        self.client_socket.send(b'COOL?')
        response = self.client_socket.recv(128)
        return response.decode('utf-8').strip()

    def set_setn(self, value):
        """
        设定工作温区为高温
        :param value: 0，高温；1，常温；2，低温。
        :return:
        """
        self._connect_to_server()
        command = f"SETN {value}".encode('utf-8')
        self.client_socket.send(command)

    def query_dut_temp(self):
        """
        查询dut温度
        :return:
        """
        self._connect_to_server()
        self.client_socket.send(b"TMPD?")
        response = self.client_socket.recv(128)
        response = response.decode('utf-8').strip()
        time.sleep(0.1)

        print(f"DUT温度为：{response}")
        return response



    def query_step_temp(self):
        """
        查看当前设定温度值
        :return:
        """
        self._connect_to_server()
        self.client_socket.send(b"SETP?")
        response = self.client_socket.recv(30)
        time.sleep(0.001)
        print(f"当前设定温度为：{response.decode('utf-8')}")

    def query_set_setp(self):
        # 查看当前设定温度值
        self._connect_to_server()
        self.client_socket.send(b"SETP?")
        response = self.client_socket.recv(30)
        time.sleep(0.001)
        set_temp = float(response.decode('utf-8'))
        print(f"当前温度已设置为：{set_temp}")
        return set_temp

    def set_temp(self, setp):
        """
        设定温度,nn有效值为对应温区有效值，手动界面需配合SETN命令使用
        :param setp:
        :return:
        """
        self._connect_to_server()
        if setp <= 0:
            self.client_socket.send(b"SETN 2")
            command = f"SETP {setp}".encode('utf-8')
            self.client_socket.send(command)
            print(f"当前设定温度值为：{setp}")
        if setp >= 35:
            self.client_socket.send(b"SETN 0")
            command = f"SETP {setp}".encode('utf-8')
            self.client_socket.send(command)
            print(f"当前设定温度值为：{setp}")
        else:
            self.client_socket.send(b"SETN 1")
            command = f"SETP {setp}".encode('utf-8')
            self.client_socket.send(command)
            print(f"当前设定温度值为：{setp}")

    def set_flow_on_off(self, on_off:Literal[1,0]):
        """
        设置吹气开关
        :param on_off: 0关闭,1打开
        :return:
        """
        self._connect_to_server()
        self.client_socket.send(f'FLOW {on_off}'.encode('utf-8'))

    def set_flwm(self, value: int):
        """
        设置吹气流量
        :param value: 设定流量nn有效数字4-18,单位为SCFM(1SCFM=28.3L/min)
        :return:
        """
        self._connect_to_server()
        self.client_socket.send(f'FLWM {value}'.encode('utf-8'))
        time.sleep(0.01)

    def set_soak(self, value: int):
        """
        设定温度保持时间，nn=1-9999秒
        :param value: nn=1-9999秒
        :return:
        """
        self._connect_to_server()
        self.client_socket.send(f'SOAK {value}'.encode('utf-8'))
        time.sleep(0.01)

    def set_head(self, value:Literal[0,1]):
        """
        设定head升降
        :param value: 0,1
        :return:
        """
        self._connect_to_server()
        self.client_socket.send(f'HEAD {value}'.encode('utf-8'))
        time.sleep(0.01)

    

    def close(self):
        self.client_socket.close()
        print("关闭仪器")
        time.sleep(0.1)

    def __enter__(self):
        """进入上下文时自动连接"""
        self._connect_to_server()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时自动断开连接"""
        self.close()






if __name__ == '__main__':
    ts760 = Ts760(server_ip='172.16.30.202')
    for _ in range(10000):
        ts760.set_temp(25)
        ts760.query_dut_temp()

    ts760.set_to_load()



