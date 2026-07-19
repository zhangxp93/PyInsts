"""
通信接口模块

定义了设备通信接口的抽象基类，为各种通信方式（如串口、I2C、SPI等）提供统一的接口。
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union, List, Tuple

class CommunicationInterface(ABC):
    """
    通信接口抽象基类
    
    为不同类型的设备通信方式提供统一的抽象接口。所有具体的通信接口实现
    （如串口、I2C、SPI等）都应继承此类并实现其抽象方法。
    """
    
    @abstractmethod
    def open(self) -> bool:
        """
        打开通信连接
        
        Returns:
            打开操作是否成功
        """
        pass
        
    @abstractmethod
    def close(self) -> bool:
        """
        关闭通信连接
        
        Returns:
            关闭操作是否成功
        """
        pass
        
    @abstractmethod
    def is_open(self) -> bool:
        """
        检查通信连接是否打开
        
        Returns:
            连接是否已打开
        """
        pass
        
    @abstractmethod
    def read(self, size: int = 1, timeout: Optional[float] = None) -> bytes:
        """
        从通信接口读取数据
        
        Args:
            size: 要读取的字节数
            timeout: 读取超时时间（秒），None表示使用默认超时设置
            
        Returns:
            读取到的数据字节
            
        Raises:
            TimeoutError: 读取超时
            IOError: 读取错误
        """
        pass
        
    @abstractmethod
    def write(self, data: bytes) -> int:
        """
        向通信接口写入数据
        
        Args:
            data: 要写入的数据字节
            
        Returns:
            成功写入的字节数
            
        Raises:
            IOError: 写入错误
        """
        pass
        
    @abstractmethod
    def flush(self) -> bool:
        """
        刷新通信缓冲区
        
        Returns:
            刷新操作是否成功
        """
        pass
        
    @abstractmethod
    def get_settings(self) -> Dict[str, Any]:
        """
        获取通信接口的当前设置
        
        Returns:
            包含通信设置的字典
        """
        pass
        
    @abstractmethod
    def set_settings(self, settings: Dict[str, Any]) -> bool:
        """
        更新通信接口设置
        
        Args:
            settings: 包含要更新的设置的字典
            
        Returns:
            设置更新是否成功
        """
        pass 