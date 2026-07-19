# 硬件接口定义

硬件接口定义模块提供了统一的设备接口抽象，便于实现不同硬件驱动的一致性和可互换性。

## 模块内容

本模块包含以下主要接口定义：

- `communication_interface.py`: 定义通信接口抽象类，用于规范不同通信方式（如SPI、I2C、UART等）的接口
- `device_interface.py`: 定义设备接口抽象类，用于规范不同硬件设备的控制接口

## 接口说明

### 通信接口

通信接口抽象类定义了所有通信驱动必须实现的方法：

```python
from abc import ABC, abstractmethod

class CommunicationInterface(ABC):
    @abstractmethod
    def open(self):
        """打开连接"""
        pass
        
    @abstractmethod
    def close(self):
        """关闭连接"""
        pass
        
    @abstractmethod
    def transfer(self, data, timeout=None):
        """数据传输"""
        pass
        
    @property
    @abstractmethod
    def is_connected(self):
        """连接状态"""
        pass
```

### 设备接口

设备接口抽象类定义了所有硬件设备驱动必须实现的方法：

```python
from abc import ABC, abstractmethod

class DeviceInterface(ABC):
    @abstractmethod
    def initialize(self):
        """初始化设备"""
        pass
        
    @abstractmethod
    def configure(self, config):
        """配置设备"""
        pass
        
    @abstractmethod
    def reset(self):
        """重置设备"""
        pass
        
    @abstractmethod
    def get_status(self):
        """获取设备状态"""
        pass
``` 