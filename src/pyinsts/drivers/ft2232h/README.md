# FT2232H 驱动模块

## 项目概述

FT2232H 驱动模块是一个用于控制 FTDI FT2232H 芯片的 Python 库。FT2232H 是一款高速 USB 2.0 到串行接口转换芯片，支持多种协议，包括 SPI、I2C、JTAG 等。本模块基于 MPSSE 模式提供了简单易用的 API，方便开发者快速实现对 FT2232H 芯片的 GPIO 控制和 SPI 通信操作。

## 主要功能

- 设备初始化与配置（MPSSE模式、时钟分频器）
- 时钟频率设置（可配置，默认1MHz）
- 低字节/高字节引脚控制（高/低电平设置）
- CS 信号（片选）控制（支持低位D3默认和高字节C0-C7）
- SPI 全双工通信
- SPI 单向发送
- SPI 批量发送（每帧独立CS周期）
- SPI 数据读取
- 状态检测灯控制
- 引脚状态读取与解析
- FTDI设备搜索

## 安装依赖

本模块依赖于 `ftd2xx` 库，可通过以下命令安装：

```bash
pip install ftd2xx
```

## 使用示例

### 基本初始化

```python
from pyinsts.drivers.ft2232h.ft2232h import Ft2232h, ft2232h_search
import logging

# 设置日志级别
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 搜索已连接的FTDI设备
ft2232h_search()

# 初始化设备，端口号为1，时钟频率为1MHz
ft2232h = Ft2232h(port=1, clock_freq=1)
```

### 引脚控制

```python
# 设置低字节引脚置高
ft2232h.set_gpios_low(0, 1)  # 将D0、D1引脚置高（低字节）

# 设置高字节引脚置高
ft2232h.set_gpios_high(0, 1)  # 将C0、C1引脚置高（高字节）

# 重置所有低字节引脚为低电平
ft2232h.set_all_gpios_low()

# 重置所有高字节引脚为低电平
ft2232h.set_all_gpios_high()

# 读取当前引脚状态
current_low = ft2232h.get_current_gpios_low()   # 读取低字节状态
current_high = ft2232h.get_current_gpios_high()  # 读取高字节状态
```

### CS片选控制

```python
# 使用默认CS引脚(D3)
ft2232h.set_cs(value=True)   # CS拉高
ft2232h.set_cs(value=False)  # CS拉低

# 使用高字节CS引脚(C2)
ft2232h.set_cs_1(cs_high_pin=2, value=True)   # C2拉高
ft2232h.set_cs_1(cs_high_pin=2, value=False)  # C2拉低
```

### SPI 通信

```python
# SPI双工传输
data_to_send = [0x29, 0x07, 0x20, 0x81]
result = ft2232h.set_spi_transfer(
    cs_high_pin=None,   # 使用默认CS引脚
    start_cs=False,     # 开始传输时不拉高CS
    stop_cs=True,       # 结束传输时拉高CS
    write_data=data_to_send,
    read_length=len(data_to_send)
)

# SPI单向发送（不接收）
ft2232h.set_spi_write(
    cs_high_pin=None,
    start_cs=False,
    stop_cs=True,
    write_data=[0x0A, 0x0B]
)

# SPI批量发送（每帧独立CS周期）
ft2232h.set_spi_write_all(
    write_data=[0x29, 0x07, 0x20, 0x81, 0x29, 0x07, 0x20, 0x82],
    frame_size=4  # 每帧4字节
)

# 发送十六进制字符串格式的数据
data_list = ["29072081"]
results = ft2232h.set_send_spi_hex(
    cs_high_pin=None,
    start_cs=False,
    stop_cs=True,
    data_list=data_list
)

# 关闭设备
ft2232h.close_device()
```

## API 文档

### 初始化

#### `Ft2232h(port, clock_freq=1)`
- `port` (int): 设备端口号
- `clock_freq` (int): 时钟频率（MHz），默认为1MHz

### CS片选控制

#### `set_cs(cs_high_pin=None, value=False)`
设置CS引脚（片选信号）状态（简化版，仅控制默认D3引脚）
- `cs_high_pin` (int, 可选): CS引脚号，范围0-7，对应C0-C7，默认为低位(D3)
- `value` (bool): True表示高电平，False表示低电平

#### `set_cs_1(cs_high_pin=None, value=False)`
设置CS引脚状态（完整版，支持高字节C0-C7引脚，会读取当前状态后按位操作）
- `cs_high_pin` (int, 可选): CS引脚号，范围0-7，对应C0-C7，默认为低位(D3)
- `value` (bool): True表示高电平，False表示低电平

### 引脚控制

#### `set_gpios_low(*pins)`
将指定的低字节引脚(D0-D7)置高
- `pins` (int): 要设置的引脚号（0-7），对应D0-D7

#### `set_gpios_high(*pins)`
将指定的高字节引脚(C0-C7)置高
- `pins` (int): 要设置的引脚号（0-7），对应C0-C7

#### `set_all_gpios_low()`
将所有低字节引脚(D0-D7)设置为低电平

#### `set_all_gpios_high()`
将所有高字节引脚(C0-C7)设置为低电平

#### `set_status_detection(value)`
设置检测灯状态（D7引脚），同时保持其他引脚状态不变
- `value` (bool): True表示低电平亮，False表示高电平灭

### 状态读取

#### `get_current_gpios_low()`
读取当前低字节引脚状态，返回8位整数，并输出详细日志

#### `get_current_gpios_high()`
读取当前高字节引脚状态，返回8位整数，并输出详细日志

### SPI通信

#### `set_spi_transfer(cs_high_pin=None, start_cs=False, stop_cs=True, write_data=None, read_length=None)`
SPI双工传输（同时收发）
- `cs_high_pin` (int, 可选): CS引脚号
- `start_cs` (bool): 是否拉高CS
- `stop_cs` (bool): 是否拉低CS
- `write_data` (list): 发送数据
- `read_length` (int): 读取数据长度
- 返回: 读取的16进制数据列表

#### `set_spi_write(cs_high_pin=None, start_cs=False, stop_cs=True, write_data=None)`
SPI单向发送数据（不接收）
- 参数同上，但不返回数据

#### `set_spi_write_all(cs_high_pin=None, start_cs=False, stop_cs=True, write_data=None, frame_size=4)`
SPI批量单向发送数据，每个帧有独立CS周期
- `write_data` (list): 发送数据，长度必须为frame_size的整数倍
- `frame_size` (int): 每帧字节数，默认4

#### `get_spi_read(cs_high_pin=None, start_cs=False, stop_cs=True, read_length=None)`
SPI读取数据
- `read_length` (int): 读取数据长度
- 返回: 读取的数据列表

#### `set_send_spi_hex(cs_high_pin=None, start_cs=False, stop_cs=True, data_list=None)`
发送16进制字符串列表数据（双工模式）
- `data_list` (list): 十六进制字符串列表，如 ["29072081"]
- 返回: 接收到的16进制数据列表

### 工具函数

#### `split_hex_string(hex_string)`
将十六进制字符串分割为字节列表
- `hex_string` (str): 十六进制字符串
- 返回: 字节列表

#### `close_device()`
关闭设备连接

#### `ft2232h_search()`（模块级函数）
搜索已连接的FTDI FT2232H设备，打印设备列表

## SPI模式说明

本模块使用 MPSSE SPI Mode 0（CPOL=0, CPHA=0）：
- CLK初始电平为低
- 上升沿接收数据，下降沿发送数据
- 命令字节：`0x31`（双工）、`0x11`（单发）

## 注意事项

1. 使用前确保正确安装了 FTDI 芯片的驱动程序（D2XX驱动）
2. 确保设备已正确连接并且端口号正确
3. 设置引脚时注意不要超出有效范围（0-7）
4. 在程序结束时记得调用 `close_device()` 方法关闭设备
5. SPI批量发送时，`write_data` 长度必须为 `frame_size` 的整数倍
6. `set_cs_1` 方法会先读取当前引脚状态再操作，适合需要保持其他引脚状态的场景

## 作者信息

作者：zhangxp  
日期：2025-04-19