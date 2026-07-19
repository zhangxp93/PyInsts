"""
硬件接口包

提供统一的设备接口抽象，便于实现不同硬件驱动的一致性和可互换性。
"""

from .communication_interface import CommunicationInterface
from .device_interface import DeviceInterface

__all__ = ['CommunicationInterface', 'DeviceInterface'] 