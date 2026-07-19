import time
import serial
import serial.tools.list_ports


class UartSerial:
    """
    串口控制类
    :param port: 串口端口
    :param baudrate: 波特率
    :param bytesize: 数据位
    :param parity: 校验位
    :param stopbits: 停止位
    :param timeout: 超时时间
    """
    def __init__(self, port, baudrate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1):
        # 初始化串口参数
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.ser = None
        self._open()

    def _open(self):
        # 打开串口
        try:
            self.ser = serial.Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
            print(f"连接到: {self.ser.name}")
        except serial.SerialException as e:
            print(f"发生错误: {e}")

    def send_data(self, hex_data):
        # 准备要发送的16进制数据
        bytes_data = bytes(hex_data)  # 修改: 确保 hex_data 是一个整数列表
        # 写入数据到串口
        if self.ser and self.ser.is_open:
            self.ser.write(bytes_data)
            print(f"已发送的数据（16进制）: {[hex(byte) for byte in hex_data]}")

    def read_data(self, size=7):
        # 读取响应数据
        if self.ser and self.ser.is_open:
            response = self.ser.read(size)  # 读取最多size个字节的数据
            if response:
                # 将接收到的字节数据转换为16进制表示
                hex_response = [hex(b) for b in response]
                print(f"接收到的数据（16进制）: {hex_response}")
            else:
                print("没有接收到数据")

    def close(self):
        # 关闭串口
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("串口已关闭")


def uart_search():
    # 获取所有可用串口的列表
    ports = serial.tools.list_ports.comports()

    # 打印每个端口的信息
    for port in ports:
        print(f"设备: {port.device}")
        print(f"名称: {port.name}")
        print(f"描述: {port.description}")
        print(f"硬件ID: {port.hwid}")
        print("-" * 40)

if __name__ == "__main__":
    uart_search()

# 示例使用
if __name__ == "__main__":
    # 创建SerialCommunication对象，设置串口参数
    comm = UartSerial(port='COM5', baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
    data1 = [0x55, 0x06, 0x01, 0x00, 0x00]
    data2 = [0x1F, 0x40]
    freq = 8000 # 发送频率
    # freq_list = [round(f, 2) for f in np.arange(8000, 10000.1, 1)]
    freq_list = [8000]
    # while True:
    for freq in freq_list:
        freq = int(freq)
        print('测试频率',freq)
        freq = hex(freq)[2:]
        data3 = [0xAA]
        data = data1 + [int(freq[i:i+2], 16) for i in (0, 2)] + data3  # 修改: 将 freq 转换为整数列表
        comm.send_data(data)
        comm.read_data()
        time.sleep(1)
    comm.close()