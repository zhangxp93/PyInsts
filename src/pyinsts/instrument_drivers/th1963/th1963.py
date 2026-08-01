# 控制TH1963子程序
from typing import Literal

from pyinsts.instrument_drivers import BaseInstrument



# 定义TH1963类，连接TH1963数字万用表
class Th1963(BaseInstrument):
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "TH1963"):
        super().__init__(address=address, config_path=config_path, model=model)

    def query_voltage_dc(self):
        """
        读取电压V
        :return:
        """
        volt = self.query(f"MEAS:VOLT:DC?")
        return float(volt)

    def query_curr_dc(self,unit:Literal["nA","uA","mA","A"]):
        """
        读取直流电流uA
        :return:
        """
        self.write(f"CONF:CURR:DC 0.0001")
        self.write(f"CURR:DC:NPLC 1")
        curr_dc = self.query(f"READ?")
        if unit == "nA":
            curr_dc = float(curr_dc)*1e9
        if unit == "uA":
            curr_dc = float(curr_dc) * 1e6
        if unit == "mA":
            curr_dc = float(curr_dc) * 1e3
        return curr_dc

    def get_measurements(self, current_unit: Literal["nA","uA","mA","A"]):
        """同时获取电压和电流"""
        curr = self.query_curr_dc(current_unit)
        volt = self.query_voltage_dc()
        return {
            'current': curr,
            'voltage': volt
        }

    def set_local(self):
        """
        设置本地模式
        """
        self.write("SYST:LOC")

if __name__ == '__main__':

    
    th1963 = Th1963(config_path="config.yaml")
    # 一次获取多个测量值
    results = th1963.get_measurements('uA')
    print(f"电流: {results['current']} uA")
    print(f"电压: {results['voltage']} V")
    

