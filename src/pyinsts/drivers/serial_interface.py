"""
串口通信接口实现

基于pyserial库实现的串口通信接口，用于与通过串口连接的设备进行通信。
"""

import time
from typing import Any, Dict, Optional, List, Tuple
import serial
from serial.tools import list_ports

from pyinsts.drivers.interfaces import CommunicationInterface

class SerialInterface(CommunicationInterface):
    """
    串口通信接口
    
    基于pyserial库实现的串口通信接口，提供了与串口设备通信的能力。
    """
    
    def __init__(self, port: str = None, baudrate: int = 9600, 
                 bytesize: int = 8, parity: str = 'N', 
                 stopbits: float = 1, timeout: float = 1.0,
                 xonxoff: bool = False, rtscts: bool = False,
                 dsrdtr: bool = False):
        """
        初始化串口通信接口
        
        Args:
            port: 串口名称
            baudrate: 波特率
            bytesize: 数据位数
            parity: 校验位 ('N'=无校验, 'E'=偶校验, 'O'=奇校验)
            stopbits: 停止位数 (1, 1.5, 2)
            timeout: 读取超时时间(秒)
            xonxoff: 是否启用软件流控
            rtscts: 是否启用RTS/CTS硬件流控
            dsrdtr: 是否启用DSR/DTR硬件流控
        """
        self._port = port
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._timeout = timeout
        self._xonxoff = xonxoff
        self._rtscts = rtscts
        self._dsrdtr = dsrdtr
        self._serial = None
        
    def open(self) -> bool:
        """
        打开串口连接
        
        Returns:
            连接是否成功打开
        
        Raises:
            serial.SerialException: 串口打开失败
        """
        try:
            if not self._port:
                # 如果没有指定端口，尝试自动检测第一个可用串口
                ports = self.list_available_ports()
                if not ports:
                    raise ValueError("未找到可用串口")
                self._port = ports[0].device
                
            if self.is_open():
                return True
                
            self._serial = serial.Serial(
                port=self._port,
                baudrate=self._baudrate,
                bytesize=self._bytesize,
                parity=self._parity,
                stopbits=self._stopbits,
                timeout=self._timeout,
                xonxoff=self._xonxoff,
                rtscts=self._rtscts,
                dsrdtr=self._dsrdtr
            )
            
            # 给设备一点时间进行初始化
            time.sleep(0.1)
            return True
            
        except serial.SerialException as e:
            print(f"打开串口失败: {e}")
            self._serial = None
            return False
            
    def close(self) -> bool:
        """
        关闭串口连接
        
        Returns:
            关闭是否成功
        """
        if self._serial and self._serial.is_open:
            try:
                self._serial.close()
                self._serial = None
                return True
            except serial.SerialException as e:
                print(f"关闭串口失败: {e}")
                return False
        return True
        
    def is_open(self) -> bool:
        """
        检查串口连接是否打开
        
        Returns:
            连接是否已打开
        """
        return self._serial is not None and self._serial.is_open
        
    def read(self, size: int = 1, timeout: Optional[float] = None) -> bytes:
        """
        从串口读取数据
        
        Args:
            size: 要读取的字节数
            timeout: 读取超时时间（秒），None表示使用默认超时设置
            
        Returns:
            读取到的数据字节
            
        Raises:
            TimeoutError: 读取超时
            IOError: 读取错误
        """
        if not self.is_open():
            raise IOError("串口未打开")
            
        original_timeout = None
        try:
            if timeout is not None:
                original_timeout = self._serial.timeout
                self._serial.timeout = timeout
                
            data = self._serial.read(size)
            
            if not data and timeout is not None:
                raise TimeoutError(f"读取超时 (timeout={timeout}s)")
                
            return data
            
        except serial.SerialTimeoutException:
            raise TimeoutError(f"读取超时 (timeout={timeout or self._timeout}s)")
        except serial.SerialException as e:
            raise IOError(f"读取错误: {e}")
        finally:
            if original_timeout is not None:
                self._serial.timeout = original_timeout
                
    def write(self, data: bytes) -> int:
        """
        向串口写入数据
        
        Args:
            data: 要写入的数据字节
            
        Returns:
            成功写入的字节数
            
        Raises:
            IOError: 写入错误
        """
        if not self.is_open():
            raise IOError("串口未打开")
            
        try:
            return self._serial.write(data)
        except serial.SerialException as e:
            raise IOError(f"写入错误: {e}")
            
    def flush(self) -> bool:
        """
        刷新串口缓冲区
        
        Returns:
            刷新操作是否成功
        """
        if not self.is_open():
            return False
            
        try:
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()
            return True
        except serial.SerialException:
            return False
            
    def get_settings(self) -> Dict[str, Any]:
        """
        获取串口的当前设置
        
        Returns:
            包含串口设置的字典
        """
        settings = {
            "port": self._port,
            "baudrate": self._baudrate,
            "bytesize": self._bytesize,
            "parity": self._parity,
            "stopbits": self._stopbits,
            "timeout": self._timeout,
            "xonxoff": self._xonxoff,
            "rtscts": self._rtscts,
            "dsrdtr": self._dsrdtr
        }
        
        if self.is_open():
            # 获取实际的串口设置
            serial_settings = {
                "port": self._serial.port,
                "baudrate": self._serial.baudrate,
                "bytesize": self._serial.bytesize,
                "parity": self._serial.parity,
                "stopbits": self._serial.stopbits,
                "timeout": self._serial.timeout,
                "xonxoff": self._serial.xonxoff,
                "rtscts": self._serial.rtscts,
                "dsrdtr": self._serial.dsrdtr
            }
            settings.update(serial_settings)
            
        return settings
        
    def set_settings(self, settings: Dict[str, Any]) -> bool:
        """
        更新串口设置
        
        Args:
            settings: 包含要更新的设置的字典
            
        Returns:
            设置更新是否成功
        """
        was_open = self.is_open()
        
        # 关闭串口以应用设置
        if was_open:
            self.close()
            
        # 更新设置
        if "port" in settings:
            self._port = settings["port"]
        if "baudrate" in settings:
            self._baudrate = settings["baudrate"]
        if "bytesize" in settings:
            self._bytesize = settings["bytesize"]
        if "parity" in settings:
            self._parity = settings["parity"]
        if "stopbits" in settings:
            self._stopbits = settings["stopbits"]
        if "timeout" in settings:
            self._timeout = settings["timeout"]
        if "xonxoff" in settings:
            self._xonxoff = settings["xonxoff"]
        if "rtscts" in settings:
            self._rtscts = settings["rtscts"]
        if "dsrdtr" in settings:
            self._dsrdtr = settings["dsrdtr"]
            
        # 如果之前是打开的，重新打开
        if was_open:
            return self.open()
            
        return True
        
    @staticmethod
    def list_available_ports() -> List[serial.tools.list_ports_common.ListPortInfo]:
        """
        列出所有可用的串口
        
        Returns:
            可用串口列表
        """
        return list(list_ports.comports())
        
    def send_command(self, command: bytes, 
                     response_size: int = 0, 
                     timeout: Optional[float] = None,
                     retry: int = 3,
                     retry_delay: float = 0.5) -> bytes:
        """
        发送命令并等待响应
        
        Args:
            command: 命令字节序列
            response_size: 期望的响应字节数，0表示不等待响应
            timeout: 响应超时时间（秒）
            retry: 重试次数
            retry_delay: 重试延迟时间（秒）
            
        Returns:
            接收到的响应数据
            
        Raises:
            TimeoutError: 超时无响应
            IOError: 通信错误
        """
        if not self.is_open():
            raise IOError("串口未打开")
            
        # 清除现有缓冲区
        self.flush()
        
        # 尝试最多retry次
        for attempt in range(retry):
            try:
                # 发送命令
                self.write(command)
                
                # 如果不需要响应，直接返回
                if response_size <= 0:
                    return b''
                    
                # 等待响应
                return self.read(response_size, timeout)
                
            except (TimeoutError, IOError) as e:
                # 最后一次尝试失败则抛出异常
                if attempt == retry - 1:
                    raise
                    
                # 否则等待后重试
                time.sleep(retry_delay)
                
        # 这里正常不会执行到，因为最后一次失败会在循环内抛出异常
        return b'' 