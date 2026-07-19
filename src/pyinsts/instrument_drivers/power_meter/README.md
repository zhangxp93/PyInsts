[**简体中文**](README.md)

<div align="center">
 <h1>
 <strong>功率计SCPI命令</strong>
 </h1>
<h5>
  <strong>适用于 Windows、MacOs、Linux</strong><br>
</h5>
</div><br>

___

- **基于pyvisa库对仪器进行控制，支持USB、GPIB、TCP/IP等连接方式。**
- **KeySight SCPI**
- **R&S SCPI**


## 必要依赖库安装
PyVISA 是一个用于控制和通信仪器的 Python 库,使用下面的代码安装:

```
pip install pyvisa
```


## 适用型号
|        型号        |  
|:----------------:|
| Keysight N1914A  |
| Keysight U2022XA |
| Keysight U8487A  |


## 快速开始
```python
from common import PowerMeter # 导入频谱仪自定义类

# 创建频谱仪对象
power_meter = PowerMeter(config_path="config.yaml", power_meter_mode="U2022XA")
power_meter.set_freq(1, "GHz")  # 设置频率
power = power_meter.query_power()
```


## 🏷[更新日志](CHANGE_LOG.md)