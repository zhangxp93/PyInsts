"""
ft2232h 类
初始化设备
设置时钟分频器
设置CS引脚（片选信号）状态
设置检测灯状态
设置BD5为输出并置高
根据输入的引脚号（D7~D0），将对应引脚置高。
SPI双工传输
SPI单发传输

作者：zhangxp
日期：2025-04-19
"""

import logging
import time
from pathlib import Path
# 添加项目根目录到 Python 路径
import sys
import os
from typing import Optional
# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ftd2xx as ftd


class Ft2232h:
    def __init__(self, port:int,clock_freq=1):
        """
        初始化FT2232H设备
        :param port: 设备端口号
        :param clock_freq: 时钟频率MHz
        """
        self.device = self._init_device(port, clock_freq)

    def _init_device(self, port:int, clock_freq:int):
        """初始化FT2232H设备"""
        try:
            device = ftd.open(port)  # 打开设备
            device.resetDevice()  # 重置设备
            device.setUSBParameters(65536, 65536)  # 设置USB参数，传输缓冲区大小
            device.setChars(False, 0, False, 0)  # 设置字符模式，禁用特殊字符处理
            device.setTimeouts(5000, 5000)  # 设置超时
            device.setLatencyTimer(16)  # 设置延迟计时器
            device.setBitMode(0, 0x02)  # 进入MPSSE模式

            # 设置时钟分频器
            # clock_divisor = 29  # 对应1MHz
            clock_divisor = int((60 / (2 * clock_freq)) - 1)
            device.write(bytes([0x86, clock_divisor & 0xFF, (clock_divisor >> 8) & 0xFF]))

            # 关闭时钟分频5
            device.write(bytes([0x8A]))
            logging.info(f"设备端口{port}初始化完成")
            return device
        except Exception as e:
            logging.error(f"设备端口{port}初始化失败: {e}")
            raise


    def set_cs_1(self, cs_high_pin:Optional[int]=None, value:bool=False):
        """
        cs拉高拉低时间有问题
        设置CS引脚（片选信号）状态
        :param cs_high_pin: CS引脚号，范围0-7，对应C0-C7，默认为低位(D3)
        :param value: True表示高电平，False表示低电平
        """
        try:
            # self.device.write(bytes([0x80, 0x00, 0x0B]))  # 需要先默认设置 DO D1 D3为输出，D2为输入
            if cs_high_pin is None:
                cs_high_pin = 3 #默认低位
            
                if value:
                    self.device.write(bytes([0x80, 0x08, 0x0B]))  # CS高
                else:
                    self.device.write(bytes([0x80, 0x00, 0x0B]))  # CS低
                # logging.debug(f"默认CS设置为: {'高' if value else '低'}")
            else:
                
                
                # 验证引脚号是否有效
                if cs_high_pin < 0 or cs_high_pin > 7:
                    raise ValueError(f"引脚号 {cs_high_pin} 超出范围，应在 0~7 之间")
                    
                # 读取当前高字节引脚状态
                current_state = self.get_current_gpios_high()
                
                # 根据value设置CS引脚状态，同时保持其他引脚状态不变
                if value:
                    # 将对应引脚置高
                    new_state = current_state | (1 << cs_high_pin)
                else:
                    # 将对应引脚置低
                    new_state = current_state & ~(1 << cs_high_pin)
                    
                # 发送新的状态，所有引脚设为输出模式
                pin_direction = 0xFF  # 所有引脚设为输出
                self.device.write(bytes([0x82, new_state, pin_direction]))
                
                logging.info(f"高位CS(C{cs_high_pin})设置为: {'高' if value else '低'}")
        except Exception as e:
            logging.error(f"设置CS失败: {e}")
            raise

    def set_cs(self, cs_high_pin: Optional[int] = None, value: bool = False):
        """
        设置CS引脚（片选信号）状态
        :param cs_high_pin: CS引脚号，范围0-7，对应C0-C7，默认为低位(D3)
        :param value: True表示高电平，False表示低电平
        """
        if value:
            self.device.write(bytes([0x80, 0x08, 0x0B]))  # CS高
        else:
            self.device.write(bytes([0x80, 0x00, 0x0B]))  # CS低

    def set_status_detection(self, value):
        """
        设置检测灯状态，同时保持其他引脚状态不变
        
        :param value: True表示低电平亮，False表示高电平灭
        """
        try:
            # 先读取当前所有引脚状态
            current_state = self.get_current_gpios_low()
            print('current_state')
            # 根据value设置检测灯状态，同时保持其他引脚状态不变
            if value:
                # 设置检测灯亮（D7置0），其他位保持不变
                new_state = current_state & 0x7F  # 0x7F = 01111111
                print(current_state,0x7F)
            else:
                # 设置检测灯灭（D7置1），其他位保持不变
                new_state = current_state | 0x80  # 0x80 = 10000000
                print(current_state,0x80,hex(new_state))
                
            # 发送新的状态，保持方向寄存器不变
            self.device.write(bytes([0x80, new_state, 0x8B]))
            logging.debug(f"检测灯设置为: {'亮' if value else '灭'}，其他引脚状态保持不变")
        except Exception as e:
            logging.error(f"设置检测灯失败: {e}")
            raise




    def set_gpios_low(self, *pins):
        """
        根据输入的引脚号（D7~D0），将对应引脚置低。

        :param device: FT2232H设备对象
        :param pins: 要置高引脚号（可变参数，范围0~7）
        """

        # 校验输入的引脚号是否合法
        for pin in pins:
            if pin < 0 or pin > 7:
                raise ValueError(f"引脚号 {pin} 超出范围，应在 0~7 之间")

        # 计算引脚状态，使用位操作设置指定引脚为高
        pin_state = 0
        for pin in pins:
            pin_state |= (1 << pin)  # 通过左移将对应引脚置高,通过按位或操作（|=），将 pin 对应的位设置为 1，并保留其他位的值不变。

        # 计算引脚方向（所有引脚设为输出）
        pin_direction = 0xFF  # 0xFF 表示所有 8 位引脚为输出

        # 发送命令：0x82 用于设置高 8 位引脚的状态
        command = [0x80, pin_state, pin_direction]
        # print(hex(pin_state))
        self.device.write(bytes(command))

        # 打印调试信息
        hex_state = format(pin_state, '02x')
        logging.info(f"引脚 {pins} 已置高，对应状态: 0x{hex_state}")

    def set_gpios_high(self, *pins):
        """
        根据输入的引脚号（D7~D0），将对应引脚置高。

        :param device: FT2232H设备对象
        :param pins: 要置高引脚号（可变参数，范围0~7）
        """
        
        # 校验输入的引脚号是否合法
        for pin in pins:
            if pin < 0 or pin > 7:
                raise ValueError(f"引脚号 {pin} 超出范围，应在 0~7 之间")

        # 计算引脚状态，使用位操作设置指定引脚为高
        pin_state = 0
        for pin in pins:
            pin_state |= (1 << pin)  # 通过左移将对应引脚置高,通过按位或操作（|=），将 pin 对应的位设置为 1，并保留其他位的值不变。

        # 计算引脚方向（所有引脚设为输出）
        pin_direction = 0xFF  # 0xFF 表示所有 8 位引脚为输出,0x00表示所有引脚为输入

        # 发送命令：0x82 用于设置高 8 位引脚的状态
        command = [0x82, pin_state, pin_direction]
        # print(hex(pin_state))
        self.device.write(bytes(command))

        # 打印调试信息
        hex_state = format(pin_state, '02x')
        logging.info(f"引脚 {pins} 已置高，对应状态: 0x{hex_state}")
        logging.info(f"接收到的16进制数据: {[hex(x) for x in command]}")

    
    def set_all_gpios_low(self):
        """
        将所有低字节引脚(D0-D7)设置为低电平
        """
        try:
            # 直接发送命令设置所有引脚为低
            pin_state = 0x00
            pin_direction = 0xFF  # 所有引脚设为输出
            command = [0x80, pin_state, pin_direction]
            self.device.write(bytes(command))
            
            # 更新状态
            self.pin_state = pin_state
            
            logging.info("所有低字节引脚已设置为低电平")
            
            return True
        except Exception as e:
            logging.error(f"设置所有引脚为低失败: {e}")
            raise

    def set_all_gpios_high(self):
        """
        将所有高字节引脚(D0-D7)设置为低电平
        """
        try:
            # 直接发送命令设置所有引脚为低
            pin_state = 0x00
            pin_direction = 0xFF  # 所有引脚设为输出
            command = [0x82, pin_state, pin_direction]
            self.device.write(bytes(command))
            
            # 更新状态
            self.pin_state = pin_state
            
            logging.info("所有高字节引脚已设置为低电平")
            
            return True
        except Exception as e:
            logging.error(f"设置所有引脚为高失败: {e}")
            raise
        

    def get_current_gpios_low(self):
        """
        读取并解析当前引脚状态
        
        :return: 当前引脚状态（8位整数，每位代表一个引脚）
        """
        try:
            # 发送命令获取当前低字节引脚状态
            self.device.write(bytes([0x81]))
            
            # 读取响应（1字节）
            response = self.device.read(1)
            
            if response and len(response) > 0:
                self.pin_state = response[0]
                hex_state = format(self.pin_state, '02x')   # 十六进制
                bin_state = format(self.pin_state, '08b')   # 二进制
                
                # 解析每个引脚的状态
                pins_status = []
                for pin in range(8):
                    state = "高" if (self.pin_state & (1 << pin)) else "低"
                    pins_status.append(f"D{pin}:{state}")
                
                # 以表格形式显示
                status_str = " | ".join(pins_status)
                
                # 记录所有状态信息
                logging.info(f"低字节当前引脚状态: 0x{hex_state} (十六进制)")
                logging.info(f"低字节引脚状态: {status_str}")
                logging.info(f"低字节二进制状态: {bin_state} (D7->D0)")
            else:
                logging.warning("读取低字节引脚状态失败，没有收到响应")
                self.pin_state = 0
                
            return self.pin_state
        except Exception as e:
            logging.error(f"读取引脚状态失败: {e}")
            raise

    def get_current_gpios_high(self):
        """
        读取并解析当前引脚状态
        
        :return: 当前引脚状态（8位整数，每位代表一个引脚）
        """
        try:
            # 发送命令获取当前低字节引脚状态
            self.device.write(bytes([0x83]))
            
            # 读取响应（1字节）
            response = self.device.read(1)
            
            if response and len(response) > 0:
                self.pin_state = response[0]
                hex_state = format(self.pin_state, '02x')
                bin_state = format(self.pin_state, '08b')
                
                # 解析每个引脚的状态
                pins_status = []
                for pin in range(8):
                    state = "高" if (self.pin_state & (1 << pin)) else "低"
                    pins_status.append(f"D{pin}:{state}")
                
                # 以表格形式显示
                status_str = " | ".join(pins_status)
                
                # 记录所有状态信息
                logging.info(f"高字节当前引脚状态: 0x{hex_state} (十六进制)")
                logging.info(f"高字节引脚状态: {status_str}")
                logging.info(f"高字节二进制状态: {bin_state} (D7->D0)")
            else:
                logging.warning("读取高字节引脚状态失败，没有收到响应")
                self.pin_state = 0
                
            return self.pin_state
        except Exception as e:
            logging.error(f"读取高字节引脚状态失败: {e}")
            raise


    def set_spi_transfer(self,
                         cs_high_pin:Optional[int]=None,
                         start_cs:bool=False, 
                         stop_cs:bool=True,
                         write_data:list=None, 
                         read_length:int=None) -> list:
        """
        SPI双工传输
        :param cs_high_pin: CS引脚号，范围0-7，对应C0-C7，默认为低位(D3)
        :param start_cs: 是否拉高CS
        :param stop_cs: 是否拉低CS
        :param write_data: 发送数据
        :param read_length: 读取数据长度
        :return: 返回读取的16进制数据list
        """
        try:
            cs_high = [0x80, 0x08, 0x0B]
            cs_low = [0x80, 0x00, 0x0B]

            # clk初始电平为低，0x31,上升沿接收，下降沿发送。通信协议模式0：CPOL= 0，CPHA=0。
            if stop_cs:
                self.device.write(bytes(cs_low + [0x31, len(write_data) - 1, 0x00] + write_data + cs_high))  # 发送数据
            elif start_cs:
                self.device.write(bytes(cs_high + [0x31, len(write_data) - 1, 0x00] + write_data + cs_low))  # 发送数据
            logging.info(f"发送的16进制数据: {[hex(x) for x in write_data]}")
            data = self.device.read(read_length)  # 读取数据
            logging.info(f"接收到的16进制数据: {[hex(x) for x in data]}")
            return list(map(hex, data))
        except Exception as e:
            logging.error(f"SPI传输失败: {e}")
            raise


    def set_spi_write(self, 
                      cs_high_pin:Optional[int]=None, 
                      start_cs:bool=False, 
                      stop_cs:bool=True, 
                      write_data:list=None) -> None:
        """SPI单向发送数据（不接收数据）
        :param cs_high_pin: CS引脚号，范围0-7，对应C0-C7，默认为低位(D3)
        :param start_cs: 是否拉高CS
        :param stop_cs: 是否拉低CS
        :param write_data: 发送数据
        """
        try:
            cs_high = [0x80, 0x08, 0x0B]
            cs_low = [0x80, 0x00, 0x0B]
            if stop_cs:
                self.device.write(bytes(cs_low+ [0x11, len(write_data) - 1, 0x00] + write_data + cs_high))  # 发送数据
            elif start_cs:
                self.device.write(bytes(cs_high + [0x11, len(write_data) - 1, 0x00] + write_data + cs_low))  # 发送数据
            logging.info(f"发送的16进制数据: {[hex(x) for x in write_data]}")
        except Exception as e:
            logging.error(f"SPI传输失败: {e}")
            raise

    def set_spi_write_all(self,
                          cs_high_pin: Optional[int] = None,
                          start_cs: bool = False,
                          stop_cs: bool = True,
                          write_data: list = None,
                          frame_size: int = 4) -> None:
        """SPI批量单向发送数据（不接收数据），每个帧有独立CS周期"""
        if not write_data or len(write_data) % frame_size != 0:
            logging.warning("SPI批量发送数据为空或长度不对齐，请检查！")
            return

        try:
            cs_high = [0x80, 0x08, 0x0B]
            cs_low = [0x80, 0x00, 0x0B]

            combined_frame = []
            num_frames = len(write_data) // frame_size  # 计算需要写的帧数

            for idx in range(num_frames):
                chunk = write_data[idx * frame_size:(idx + 1) * frame_size]
                data_len = len(chunk) - 1

                # ✅ 开始cs
                if start_cs:
                    combined_frame.extend(cs_high)
                else:
                    combined_frame.extend(cs_low)

                # ✅ 每帧固定动作：拉低CS → 发MPSSE命令 → 发数据
                combined_frame.extend(
                    [0x11, data_len & 0xFF, (data_len >> 8) & 0xFF])
                combined_frame.extend(chunk)

                # ✅ 结束cs
                if stop_cs:
                    combined_frame.extend(cs_high)
                else:
                    combined_frame.extend(cs_low)

            self.device.write(bytes(combined_frame))
            logging.info(
                f"SPI批量发送完成: {num_frames}帧, 每帧{frame_size}B, 总{len(write_data)}B")
            logging.info(
                f"发送的16进制数据: {[hex(x) for x in combined_frame]}")

        except Exception as e:
            logging.error(f"SPI批量传输失败: {e}")
            raise

    def get_spi_read(self, 
                    cs_high_pin:Optional[int]=None, 
                    start_cs:bool=False, 
                    stop_cs:bool=True, 
                    read_length:int=None) -> list:
        """
        SPI读取数据
        :param cs_high_pin: CS引脚号，范围0-7，对应C0-C7，默认为低位(D3)
        :param read_length: 读取数据长度
        """
        try:
            self.set_cs(cs_high_pin=cs_high_pin,value=start_cs)  # 拉高CS
            data = self.device.read(read_length)  # 读取数据
            logging.info(f"接收到的16进制数据: {[hex(x) for x in data]}")
            self.set_cs(cs_high_pin=cs_high_pin,value=stop_cs)  # 拉低CS
            return data
        except Exception as e:
            logging.error(f"SPI读取失败: {e}")
            raise

    def split_hex_string(self, hex_string:str) -> list:
        """将十六进制字符串分割为字节列表"""
        if len(hex_string) % 2 != 0:
            raise ValueError("十六进制字符串长度必须为偶数")
        byte_pairs = [hex_string[i:i + 2] for i in range(0, len(hex_string), 2)]
        return [int(pair, 16) for pair in byte_pairs]

    def set_send_spi_hex(self,
                         cs_high_pin:Optional[int]=None, 
                         start_cs:bool=False, 
                         stop_cs:bool=True, 
                         data_list:list=None) -> list:
        """
        发送16进制list数据
        :param cs_high_pin: CS引脚号，范围0-7，对应C0-C7，默认为低位(D3)
        :param start_cs: 是否拉高CS
        :param stop_cs: 是否拉低CS
        :param data_list: 发送数据列表
        :return: 返回读取的16进制数据list
        """
        get_data_list = []
        try:
            for data in data_list:
                data_to_send = self.split_hex_string(data)
                logging.info(f"准备发送的16进制数据: {[hex(x) for x in data_to_send]}")
                # 示例调用
                data_received = self.set_spi_transfer(
                    cs_high_pin=cs_high_pin, 
                    start_cs=start_cs, 
                    stop_cs=stop_cs, 
                    write_data=data_to_send, 
                    read_length=len(data_to_send))  # 收发双工
                logging.info(f"接收到16进制数据: {data_received}")
                get_data_list.append(data_received)
            return get_data_list
        except Exception as e:
            logging.error(f"程序执行失败: {e}")

    def close_device(self):
        """关闭设备"""
        self.device.close()


def ft2232h_search():
    """搜索FT2232H设备"""
    # 获取所有FTDI设备的设备ID列表
    devices = ftd.listDevices()

    if devices:
        print("已找到以下FTDI设备：")
        for device in devices:
            print(device)
    else:
        print("未找到任何FTDI设备。")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    # ft2232h_search()
    start_time = time.time()
    ft2232h = Ft2232h(1)
    ft2232h.set_all_gpios_high()

    # 10G
    # ft2232h.set_gpios_high(0)
    # ft2232h.set_gpios_low(1,2)

    # 18
    # ft2232h.set_gpios_high(1,2,4,5)
    # ft2232h.set_gpios_low( 2)

    # 17.4
    ft2232h.set_gpios_high(1, 2, 5, 6)
    ft2232h.set_gpios_low(0,1)


    # 跳频时间
    # ft2232h.set_gpios_high(0,2,3,4)  # 12
    # ft2232h.set_gpios_high(0,5)  # 13.6

    # 跳频时间 10~19.6
    # ft2232h.set_gpios_high(0, 4) # 10G 312.5M
    # ft2232h.set_gpios_high(1, 2, 3, 5)  # 19.6G 612.5M

    # 跳频时间 16~17.6
    # ft2232h.set_gpios_high(4)  # 16
    # ft2232h.set_gpios_high(2,5)  # 17.6

    # ft2232h.set_all_gpios_low()
    # ft2232h.set_gpios_high(0, 4, 5)  # 20
    # ft2232h.set_gpios_high(1, 2, 4, 5)  # 22
    # ft2232h.set_gpios_high(0, 3, 4, 5)  # 23.2
    # ft2232h.set_gpios_high(0, 2, 3, 4, 5)  # 24.8
    # ft2232h.set_gpios_high( 1, 2, 3, 4, 5)  # 25.2

    # ft2232h.set_gpios_high(0, 4, 5)  # 20
    # ft2232h.set_gpios_high(0, 1, 2, 4, 5)  # 22.4
    # ft2232h.set_gpios_high(1, 2, 4, 5)  # 22
    # ft2232h.set_gpios_high(0, 4, 5)  # 20

    # time.sleep(1)
    # ft2232h.set_gpios_low(0, 1)
    # ft2232h.set_gpios_high(5)  # 13.6


    # ft2232h.set_gpios_low(1)
    # ft2232h.set_gpios_high(0,4,5) #120
    # ft2232h.set_all_gpios_low()
    # ft2232h.set_gpios_low(0)
    # for i in range(1):
    #     ft2232h.set_pins_low(7)
    #     ft2232h.set_pins_low(0,1)
    # ft2232h.set_all_pins_high()
    # ft2232h.set_all_gpios_low()
    # # 获取当前状态
    # current_state_low = ft2232h.get_current_pin_low()
    print("第一次重置完成")
    # current_state_high = ft2232h.get_current_pin_high()
    # logging.info(f"当前状态: {current_state_low} {current_state_high}")
    # data_list_a = ["29072081"]
    # data = [0x0A]
    # ft2232h.set_spi_transfer(start_cs=False, stop_cs=True, write_data=data, read_length=len(data))
    # ft2232h.set_send_spi_hex(cs_high_pin=2, start_cs=False, stop_cs=True, data_list=data_list_a)
    # data_list_b = ["29072082"]
    # send_spi_data_b(data_list_b)
    # send_spi_data_a(data_list_a)
    # send_gpio_a(4,5,2) #b通950
    # send_gpio_a(0) #a通900
    # ft2232h.set_status_detection(False)
    # ft2232h.device.write(bytes([0x80, 0x00, 0x8b]))
    # ft2232h.get_current_pin_low()
    end_time = time.time()
    logging.info(f"程序运行时间: {end_time - start_time} 秒")


