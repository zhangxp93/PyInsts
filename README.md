[**简体中文**](https://github.com/zhangxp93/PyInst/blob/main/README.md) | [**English**](https://github.com/zhangxp93/PyInst/blob/main/README_en.md)

<div align="center">
  <h1>🚀 PyInsts</h1>
  <p><strong>基于 PyVISA 的仪器自动化控制封装库 (支持 Windows, macOS, Linux)</strong></p>

  [![PyPI Version](https://img.shields.io/pypi/v/pyinsts.svg)](https://pypi.org/project/pyinsts/)
  [![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyinsts.svg)](https://pypi.org/project/pyinsts/)
  [![License](https://img.shields.io/github/license/zhangxp93/PyInst.svg)](https://github.com/zhangxp93/PyInst/blob/main/LICENSE)
</div>

---

`pyinsts` 是一个轻量级、健壮的 Python 仪器控制封装库。它基于 `PyVISA`，针对射频和电子测试实验室中常用的频谱分析仪、信号源、网络分析仪、电源、万用表等仪器进行了高层 SCPI 指令封装，同时支持底层的串口与硬件接口通信。

## ✨ 核心特性与架构

- 🏗 **模块化设计**：
  - `instrument_drivers/`: 存放 SCPI 仪器驱动及基类 `baseinstrument.py`，驱动类可直接从 `pyinsts.instrument_drivers` 统一导出使用。
  - `drivers/`: 存放底层硬件通信协议封装（如 `serial_interface.py`, `ft2232h` 等）。
  - `instrument/sim/`: 存放无实体硬件测试所需的仿真配置文件。
- 🔄 **自动连接重试**：内置连接重试机制，自动规避短暂的硬件握手超时。
- ⏳ **高效同步阻塞**：提供 `wait_opc()` 机制，相比硬编码 `time.sleep` 更安全，避免截图或扫频时的竞态问题。
- 🗂 **灵活配置加载**：支持通过外部 `config.yaml` 或 `config.json` 自动解析和分配仪器的物理地址（如 VISA 资源地址）。
- 📝 **开箱即用日志**：内置彩色日志流（依赖 `colorlog`），方便调试 SCPI 指令交互。

---

## 📦 安装方法

确保你的系统已配置 VISA 后台驱动（如 NI-VISA 或 Keysight IO Libraries Suite）。

```bash
pip install pyinsts
```

---

## ⚙️ 仪器地址配置文件示例

本库支持通过配置文件集中管理仪器的 VISA 地址。默认寻找 `config.yaml` 或 `config.json`。

在你的项目目录下创建 `config.yaml`：

```yaml
instruments:
  N9020B: "USB0::0x2A8D::0x1D0B::MY55480186::INSTR"  # Keysight 频谱仪地址
  E5052B: "GPIB0::17::INSTR"                         # Keysight 信号源分析仪地址
  FSWP-26: "TCPIP0::192.168.1.100::inst0::INSTR"     # R&S 信号分析仪地址
```

---

## 🚀 快速开始 (Quick Start)

下面是控制 Keysight N9020B 频谱仪并设置参数的示例：

```python
import logging
from pyinsts.instrument_drivers import KeysightN9020B
from pyinsts.data.log_data import setup_logging

# 1. 初始化日志输出（支持控制台彩色显示）
setup_logging(log_level=logging.INFO)

# 2. 建立仪器连接（若不传入 address，则自动从 config.yaml 读取 model='N9020B' 的配置）
config_path = 'config.yaml'
try:
    with KeysightN9020B(config_path=config_path, model="N9020B") as spec_analyser:
        # 设置中心频率为 1 GHz
        spec_analyser.set_freq_cent(1, "GHz")

        # 将分辨率带宽 (RBW) 设置为自动
        spec_analyser.set_rbw_auto()

        # 触发 Peak Search
        spec_analyser.set_peak_search()

        # 查询当前 Marker1 的功率值
        power = spec_analyser.query_mark_y_power()
        print(f"当前信号峰值功率为: {power} dBm")

except Exception as e:
    print(f"仪器操作过程中发生错误: {e}")
```

---

## 📟 目前支持的仪器型号矩阵

支持的驱动类均支持从 `pyinsts.instrument_drivers` 直接导入：

| 厂商 (Manufacturer) | 仪器类型 (Type) | 驱动类名 (Class) | 验证型号 (Tested Models) |
| :--- | :--- | :--- | :--- |
| **Keysight / Agilent** | 信号/频谱分析仪 | `KeysightN9020B` | N9020B |
| **Keysight / Agilent** | 信号/频谱分析仪 | `KeysightN9030A`, `KeysightN9030B` | N9030A, N9030B |
| **Keysight / Agilent** | 信号源分析仪 | `KeysightE5052B` | E5052B |
| **Keysight / Agilent** | 模拟信号发生器 | `KeysightE8257D` | E8257D |
| **Keysight / Agilent** | 矢量网络分析仪 | `KeysightN5245B` | N5245B |
| **Keysight / Agilent** | 直流电源 | `KeysightE36312A` | E36312A |
| **Keysight / Agilent** | 射频功率计 | `KeysightN1914A` | N1914A |
| **Keysight / Agilent** | 数字万用表 | `DM34461A` | 34461A |
| **Rohde & Schwarz** | 频谱/信号分析仪 | `FSV3030Sp` | FSV3030 |
| **Rohde & Schwarz** | 信号/相噪分析仪 | `FswpSp` (频谱模式), `FswpPN` (相噪模式) | FSWP-26 / FSWP |
| **同惠 (Tonghui)** | 数字万用表 | `Th1963` | TH1963 |
| **其他设备 (Others)** | 源表 / 测量单元 | `P2401` | P2401 |
| **其他设备 (Others)** | 温控箱单元 | `Ts760` | TS760 |

---

## 🏷 更新日志与贡献

- 想要提交 Bug 或 Feature Request？请前往 [GitHub Issues](https://github.com/zhangxp93/PyInst/issues)
- 历史版本迭代记录详见 [CHANGELOG.md](https://github.com/zhangxp93/PyInst/blob/main/CHANGELOG.md)

## 📄 开源协议

本项目采用 [MIT License](https://github.com/zhangxp93/PyInst/blob/main/LICENSE) 开源协议。
