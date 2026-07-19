import serial
import time

class Pico2:
    def __init__(self, port="/dev/cu.usbmodem2101", baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.running = False
        self.pin = None

    def connect(self, pin=25):
        """连接设备并初始化指定引脚"""
        try:
            self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=1)
            self.pin = pin
            # 初始化引脚
            response = self.send_command(f"INIT {pin}")
            print(response)
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.send_command("EXIT")  # 发送退出命令给Pico
            time.sleep(0.1)  # 等待Pico处理命令
            self.ser.close()
            self.running = False
            print("已断开连接")

    def send_command(self, command):
        if self.ser and self.ser.is_open:
            self.ser.write(f"{command}\n".encode())
            response = self.ser.readline()
            return response.decode().strip()
        return None

    def start_blink(self, interval=0.2, times=10):
        """
        开始LED闪烁
        :param interval: 闪烁间隔时间（秒）
        :param times: 运行时间（秒）
        """
        if not self.ser:
            if not self.connect():
                return
        self.running = True
        start_times = time.time()
        try:
            while self.running:
                response = self.send_command("ON")
                print(response)
                time.sleep(interval)
                
                response = self.send_command("OFF")
                print(response)
                time.sleep(interval)
                run_times = time.time() - start_times
                if run_times > times:
                    self.disconnect()
                    break
        except Exception as e:
            print(f"运行时错误: {e}")
        finally:
            self.disconnect()

    def stop_blink(self):
        self.running = False


if __name__ == "__main__":
    # 示例：使用不同的引脚
    addr = "/dev/cu.usbserial-210"
    addr1 = "/dev/cu.usbserial-2101"
    pico = Pico2(addr)
    # 使用引脚15进行闪烁
    pico.connect(pin=2)  
    pico.start_blink(interval=0.5, times=10)