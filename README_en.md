[**简体中文**](https://github.com/zhangxp93/PyInst/blob/main/README.md) | [**English**](https://github.com/zhangxp93/PyInst/blob/main/README_en.md)

<div align="center">
  <h1>🚀 PyInsts</h1>
  <p><strong>PyVISA-based Instrument Automation Control Wrapper Library (Supports Windows, macOS, Linux)</strong></p>

  [![PyPI Version](https://img.shields.io/pypi/v/pyinsts.svg)](https://pypi.org/project/pyinsts/)
  [![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyinsts.svg)](https://pypi.org/project/pyinsts/)
  [![License](https://img.shields.io/github/license/zhangxp93/PyInst.svg)](https://github.com/zhangxp93/PyInst/blob/main/LICENSE)
</div>

---

`pyinsts` is a lightweight, robust Python library for instrument automation control. Built on top of `PyVISA`, it provides high-level SCPI command wrappers for spectrum analyzers, signal generators, network analyzers, power supplies, multimeters, and other instruments commonly used in RF and electronics testing labs, while also supporting low-level serial and hardware interface communications.

## ✨ Core Features & Architecture

- 🏗 **Modular Design**:
  - `instrument_drivers/`: Stores SCPI instrument drivers and the base class `baseinstrument.py`. Driver classes are exported directly from `pyinsts.instrument_drivers`.
  - `drivers/`: Stores low-level hardware communication protocol wrappers (e.g., `serial_interface.py`, `ft2232h`).
  - `instrument/sim/`: Stores simulation configuration files for hardware-free automated testing.
- 🔄 **Auto-reconnection Retry**: Built-in connection retry mechanism to gracefully handle temporary hardware handshake timeouts.
- ⏳ **Efficient Synchronization**: Provides `wait_opc()` to query `*OPC?`, blocking execution until commands complete, preventing race conditions during screenshots or sweeping.
- 🗂 **Flexible Configurations**: Automatically loads and parses VISA resource addresses from external `config.yaml` or `config.json`.
- 📝 **Out-of-the-box Logging**: Built-in colorized console logger (powered by `colorlog`) for easier SCPI command tracing and debugging.

---

## 📦 Installation

Ensure that you have installed the VISA backend driver (e.g., National Instruments NI-VISA or Keysight IO Libraries Suite) on your system.

```bash
pip install pyinsts
```

---

## ⚙️ Instrument Address Configuration Example

This library supports managing VISA addresses in a centralized configuration file. It looks for `config.yaml` or `config.json` by default.

Create a `config.yaml` in your project folder:

```yaml
instruments:
  N9020B: "USB0::0x2A8D::0x1D0B::MY55480186::INSTR"  # Keysight Spectrum Analyzer Address
  E5052B: "GPIB0::17::INSTR"                         # Keysight Signal Source Analyzer Address
  FSWP-26: "TCPIP0::192.168.1.100::inst0::INSTR"     # R&S Signal Analyzer Address
```

---

## 🚀 Quick Start

Here is a simple example of controlling a Keysight N9020B spectrum analyzer:

```python
import logging
from pyinsts.instrument_drivers import KeysightN9020B
from pyinsts.data.log_data import setup_logging

# 1. Initialize logging (supports colorized console output)
setup_logging(log_level=logging.INFO)

# 2. Establish connection (automatically reads N9020B address from config.yaml if no address parameter is passed)
config_path = 'config.yaml'
try:
    with KeysightN9020B(config_path=config_path, model="N9020B") as spec_analyser:
        # Set center frequency to 1 GHz
        spec_analyser.set_freq_cent(1, "GHz")

        # Enable auto Resolution Bandwidth (RBW)
        spec_analyser.set_rbw_auto()

        # Trigger Peak Search
        spec_analyser.set_peak_search()

        # Query Marker1 Y power value
        power = spec_analyser.query_mark_y_power()
        print(f"Marker1 Peak Power: {power} dBm")

except Exception as e:
    print(f"Error during instrument operations: {e}")
```

---

## 📟 Supported Instrument Models Matrix

All driver classes can be directly imported from `pyinsts.instrument_drivers`:

| Manufacturer | Instrument Type | Driver Class | Tested Models |
| :--- | :--- | :--- | :--- |
| **Keysight / Agilent** | Signal/Spectrum Analyzer | `KeysightN9020B` | N9020B |
| **Keysight / Agilent** | Signal/Spectrum Analyzer | `KeysightN9030A`, `KeysightN9030B` | N9030A, N9030B |
| **Keysight / Agilent** | Signal Source Analyzer | `KeysightE5052B` | E5052B |
| **Keysight / Agilent** | Analog Signal Generator | `KeysightE8257D` | E8257D |
| **Keysight / Agilent** | Vector Network Analyzer | `KeysightN5245B` | N5245B |
| **Keysight / Agilent** | DC Power Supply | `KeysightE36312A` | E36312A |
| **Keysight / Agilent** | RF Power Meter | `KeysightN1914A` | N1914A |
| **Keysight / Agilent** | Digital Multimeter | `DM34461A` | 34461A |
| **Rohde & Schwarz** | Spectrum/Signal Analyzer | `FSV3030Sp` | FSV3030 |
| **Rohde & Schwarz** | Signal / Phase Noise Analyzer | `FswpSp` (Spectrum), `FswpPN` (Phase Noise) | FSWP-26 / FSWP |
| **Tonghui** | Digital Multimeter | `Th1963` | TH1963 |
| **Others** | Source Measure Unit | `P2401` | P2401 |
| **Others** | ThermoStream / Temp Chamber | `Ts760` | TS760 |

---

## 🏷 Changelog & Contribution

- Want to report a bug or submit a feature request? Please visit [GitHub Issues](https://github.com/zhangxp93/PyInst/issues)
- Detailed version iteration logs can be found in [CHANGELOG.md](https://github.com/zhangxp93/PyInst/blob/main/CHANGELOG.md)

## 📄 License

This project is licensed under the [MIT License](https://github.com/zhangxp93/PyInst/blob/main/LICENSE).