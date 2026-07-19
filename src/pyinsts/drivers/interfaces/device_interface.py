"""
设备接口抽象模块

此模块定义了所有硬件设备驱动必须实现的抽象接口。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class DeviceInterface(ABC):
    """设备接口抽象类
    
    定义了所有硬件设备驱动必须实现的方法。
    """
    
    @abstractmethod
    def initialize(self):
        """初始化设备
        
        执行设备的初始化过程，包括打开连接、设置默认配置等。
        
        Returns:
            bool: 初始化成功返回True，否则返回False
        """
        pass
        
    @abstractmethod
    def configure(self, config: Dict[str, Any]):
        """配置设备
        
        根据提供的配置参数配置设备。
        
        Args:
            config (Dict[str, Any]): 配置参数字典
            
        Returns:
            bool: 配置成功返回True，否则返回False
            
        Raises:
            ValueError: 配置参数无效
        """
        pass
        
    @abstractmethod
    def reset(self):
        """重置设备
        
        将设备重置为初始状态。
        
        Returns:
            bool: 重置成功返回True，否则返回False
        """
        pass
        
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """获取设备状态
        
        Returns:
            Dict[str, Any]: 设备状态信息字典
        """
        pass 