[**简体中文**](https://github.com/zhangxp93/PyInst/blob/main/README.md) | [**English**](https://github.com/zhangxp93/PyInst/blob/main/README_en.md)

<div align="center">
  <h1>🚀 PyInsts</h1>
  <p><strong>基于 PyVISA 的仪器自动化控制封装库 (支持 Windows, macOS, Linux)</strong></p>

  [![PyPI Version](https://img.shields.io/pypi/v/pyinsts.svg)](https://pypi.org/project/pyinsts/)
  [![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyinsts.svg)](https://pypi.org/project/pyinsts/)
  [![License](https://img.shields.io/github/license/zhangxp93/PyInst.svg)](https://github.com/zhangxp93/PyInst/blob/main/LICENSE)
</div>

---

`pyinsts` 是一个轻量级、健壮的 Python 仪器控制封装库。它基于 `PyVISA`，针对射频和电子测试实验室中常用的频谱分析仪、信号源等仪器进行了高层 SCPI 指令封装，支持 USB、GPIB、TCP/IP (LAN) 等多种物理连接。

## ✨ 核心特性

- 🔌 **统一基类封装**：底层自动管理 `ResourceManager` 句柄，提供健壮的 `write` 与 `query` 操作。
- 🔄 **自动连接重试**：内置 3 次连接重试机制，自动规避短暂的硬件握手超时。
- ⏳ **高效同步阻塞**：提供 `wait_opc()` 机制，相比硬编码 `time.sleep` 更安全，避免截图或大跨度扫频时的竞态问题。
- 🗂 **灵活配置加载**：支持通过外部 `config.yaml` 或 `config.json` 自动解析和分配仪器的物理地址（如 VISA 资源地址）。
- 📝 **开箱即用日志**：内置彩色日志流（依赖 `colorlog`），方便调试 SCPI 指令交互。

---

## 📦 安装方法

除了安装本库之外，确保你的系统已正确配置 VISA 后台驱动（如 National Instruments NI-VISA 或 Keysight IO Libraries Suite）。

```bash
# 推荐使用 pip 直接安装
pip install pyinsts
```

---

## ⚙️ 仪器地址配置文件示例

本库支持通过配置文件集中管理仪器的 VISA 地址。默认在驱动类的同级目录下寻找 `config.yaml` 或 `config.json`。

在你的项目目录下创建 `config.yaml`：

```yaml
instruments:
  N9020B: "USB0::0x2A8D::0x1D0B::MY55480186::INSTR"  # Keysight 频谱仪地址
  FSWP: "TCPIP0::192.168.1.100::inst0::INSTR"         # R&S 信号分析仪地址
```

---

## 🚀 快速开始 (Quick Start)

下面是控制 Keysight N9020B 频谱仪并设置参数的简单示例：

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

## 📟 目前支持的仪器型号

本库正在持续更新中，目前已完成对以下仪器的 SCPI 核心指令封装：

| 厂商 (Manufacturer) | 仪器类型 (Type) | 驱动类名 (Class) | 验证型号 (Tested Models) |
| :--- | :--- | :--- | :--- |
| **Keysight (Agilent)** | 信号/频谱分析仪 (Signal Analyzer) | `N9020b` | N9020B, N9030B |
| **Rohde & Schwarz** | 信号源/相位噪声分析仪 (Phase Noise Analyzer) | `Fswp` | FSWP |

---

## 🏷 更新日志与贡献

- 想要提交 Bug 或 Feature Request？请前往 [GitHub Issues](https://github.com/zhangxp93/PyInst/issues)
- 历史版本迭代记录详见 [CHANGELOG.md](https://github.com/zhangxp93/PyInst/blob/main/CHANGELOG.md)

## 📄 开源协议

本项目采用 [MIT License](https://github.com/zhangxp93/PyInst/blob/main/LICENSE) 开源协议。
