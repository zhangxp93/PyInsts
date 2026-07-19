[**简体中文**](https://github.com/zhangxp93/PyInst/blob/main/README.md) | [**English**](https://github.com/zhangxp93/PyInst/blob/main/README_en.md)

<div align="center">
  <h1>🚀 PyInsts</h1>
  <p><strong>PyVISA-based Instrument Automation Control Wrapper Library (Supports Windows, macOS, Linux)</strong></p>

  [![PyPI Version](https://img.shields.io/pypi/v/pyinsts.svg)](https://pypi.org/project/pyinsts/)
  [![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyinsts.svg)](https://pypi.org/project/pyinsts/)
  [![License](https://img.shields.io/github/license/zhangxp93/PyInst.svg)](https://github.com/zhangxp93/PyInst/blob/main/LICENSE)
</div>

---

`pyinsts` is a lightweight, robust Python library for instrument automation control. Built on top of `PyVISA`, it provides high-level SCPI command wrappers for common instruments used in RF and electronics testing laboratories, supporting USB, GPIB, and TCP/IP (LAN) connectivity.

## ✨ Features

- 🔌 **Unified Base Class**: Automatically manages the `ResourceManager` session and provides robust `write` and `query` operations.
- 🔄 **Auto-reconnection Retry**: Built-in 3-retry mechanism for connection failures to gracefully handle temporary hardware handshake timeouts.
- ⏳ **Efficient Synchronization**: Provides `wait_opc()` to query `*OPC?`, which blocks the Python execution until commands are complete, preventing race conditions during screenshots or wide-span frequency sweep configurations.
- 🗂 **Flexible Configurations**: Automatically loads and parses VISA resource addresses from external `config.yaml` or `config.json`.
- 📝 **Out-of-the-box Logging**: Built-in colorized console logger (powered by `colorlog`) for easier SCPI command tracing and debugging.

---

## 📦 Installation

Ensure that you have installed the VISA backend driver (e.g., National Instruments NI-VISA or Keysight IO Libraries Suite) on your system.

```bash
# Install via pip
pip install pyinsts
```

---

## ⚙️ Instrument Address Configuration Example

This library supports managing VISA addresses in a centralized configuration file. It looks for `config.yaml` or `config.json` in the directory of the inherited instrument class by default.

Create a `config.yaml` in your project folder:

```yaml
instruments:
  N9020B: "USB0::0x2A8D::0x1D0B::MY55480186::INSTR"  # Keysight Spectrum Analyzer Address
  FSWP: "TCPIP0::192.168.1.100::inst0::INSTR"         # R&S Signal/Phase Noise Analyzer Address
```

---

## 🚀 Quick Start

Here is a simple example of controlling a Keysight N9020B spectrum analyzer using the context manager:

```python
import logging
from pyinsts.instrument_drivers.keysight.n9020b import N9020b
from pyinsts.common.log_data import setup_logging

# 1. 初始化日志输出（支持控制台彩色显示）
setup_logging(log_level=logging.INFO)

# 2. 建立仪器连接（若不传入 address，则自动从 config.yaml 读取 model='N9020B' 的配置）
# 支持使用 context manager 自动关闭连接句柄
config_path = 'D:\\config.yaml'
try:
  with N9020b(config_path=config_path, model="N9020B") as spec_analyser:
    # 设置中心频率为 1 GHz
    spec_analyser.set_freq_cent(1, "GHz")

    # 将分辨率带宽 (RBW) 设置为自动
    spec_analyser.set_rbw_auto()

    # 触发一次 Peak Search
    spec_analyser.set_peak_search()

    # 查询当前 Marker1 的功率值
    power = spec_analyser.query_mark_y_power()
    print(f"当前信号峰值功率为: {power} dBm")

except Exception as e:
  print(f"仪器操作过程中发生错误: {e}")
```

---

## 📟 Supported Instrument Models

This library is actively maintained. The following instrument SCPI models are currently supported:

| Manufacturer | Instrument Type | Driver Class | Tested Models |
| :--- | :--- | :--- | :--- |
| **Keysight (Agilent)** | Signal/Spectrum Analyzer | `N9020b` | N9020B, N9030B |
| **Rohde & Schwarz** | Phase Noise / Signal Analyzer | `Fswp` | FSWP |

---

## 🏷 Changelog & Contribution

- Want to report a bug or submit a feature request? Please visit [GitHub Issues](https://github.com/zhangxp93/PyInst/issues)
- Detailed version iteration logs can be found in [CHANGELOG.md](https://github.com/zhangxp93/PyInst/blob/main/CHANGELOG.md)

## 📄 License

This project is licensed under the [MIT License](https://github.com/zhangxp93/PyInst/blob/main/LICENSE).