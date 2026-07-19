# 控制rsa6000
import logging
import time
from typing import Literal, Optional, Union

from pyinsts.instrument_drivers import BaseInstrument


# 定义instrument类，连接instrument频谱仪
class Rsa6000(BaseInstrument):
    def __init__(self, address: Optional[str] = None, config_path="config.yaml", model: str = "RSA6265"):
        super().__init__(address=address, config_path=config_path, model=model)


    def set_clear_status(self) -> None:
        """
        清除仪器输出缓存区
        :return:
        """
        self.write('*CLS')
        logging.info('清除仪器缓存')

    def set_preset(self) -> None:
        """
        复位
        :return:
        """
        self.write('*RST', opc=True)
        logging.info('复位')

    def set_rename_window(self, old_name: str, new_name: str) -> None:
        """
        重命名窗口
        :param old_name:
        :param new_name:
        :return:
        """
        self.set_window(old_name)   # 切换到旧窗口
        self.write(f'INST:SCR:REN "{new_name}"')
        logging.info(f'重命名窗口: {old_name} -> {new_name}')

    def set_window(self, window: str = 'Spectrum') -> None:
        """
        选择窗口
        :param window:
        :return:
        """
        self.write(f'INST:SCR:SEL "{window}"')
        logging.info(f'选择窗口: {window}')

    def query_window(self) -> str:
        """
        查询当前窗口名称
        :return:
        """
        name = self.write(f'INST:SCR:SEL?')
        logging.info(f'查询当前窗口名称: {name}')
        return name
    # todo 重构到当前位置

    def set_abort_meas(self) -> None:
        """
        中止测量
        :return:
        """
        self.write('ABOR')
        logging.info('中止测量')

    def set_run_cont(self) -> None:
        """
        设置仪器为连续运行模式
        :return:
        """
        self.write('INIT:CONT OFF')
        self.write('INIT:CONT ON')
        logging.info('设置仪器为连续运行模式')

    def set_run_single(self) -> None:
        """
        设置仪器为单次运行模式
        """
        self.write('INIT:CONT OFF')
        self.write('INIT:IMM', check_complete=True)
        logging.info('设置仪器为单次运行模式')

    def set_to_load(self) -> None:
        """
        切换为手动操作
        :return:
        """
        self.write(f'SYST:COMM:INT:REM OFF')
        logging.info('切换为手动操作')

    def set_err_disp(self, switch: Literal["ON", 'OFF']) -> None:
        """
        设置错误消息显示
        :param switch:
        :return:
        """
        self.write(f'SYST:ERR:DISP {switch}')
        logging.info(f'设置错误消息显示: {switch}')

    def set_freq_center(self, freq: Union[int, float], unit: Literal['GHz', 'MHz', 'kHz', 'Hz']) -> None:
        """
        设置中心频率
        :param unit:
        :param freq:
        :return:
        """
        self.write(f'SENSE:FREQ:CENT {freq}{unit}')
        logging.info(f'设置中心频率: {freq}{unit}')

    def set_mark_on(self, x: int) -> None:
        self.write(f'CALC:MARK{x}:STAT ON')
        logging.info(f'设置mark{x}为开启')

    def set_mark_freq(self, x: int, freq: Union[int, float], unit: Literal['GHz', 'MHz', 'kHz', 'Hz']) -> None:
        """
        设置mark频率
        :param x: 1,2,3,4,5,6,7
        :param unit:
        :param freq:
        :return:
        """
        if unit == 'GHz':
            freq = freq * 1e9
        elif unit == 'MHz':
            freq = freq * 1e6
        elif unit == 'kHz':
            freq = freq * 1e3
        elif unit == 'Hz':
            freq = freq * 1
        self.write(f'CALC:MARK{x}:X {freq}')
        logging.info(f'设置mark{x}频率: {freq}')

    def query_marker_x(self, x: int, unit: Literal['GHz', 'MHz', 'kHz', 'Hz']) -> float:
        """
        查询marker频率
        :param x:1,2,3,4,5,6,7
        :param unit:
        :return:
        """
        marker_value = self.query(f'CALC:MARK{x}:X?')
        marker_value = float(marker_value.rstrip("\n"))
        if unit == 'GHz':
            marker_value = marker_value / 1e9
        elif unit == 'MHz':
            marker_value = marker_value / 1e6
        elif unit == 'kHz':
            marker_value = marker_value / 1e3
        elif unit == 'Hz':
            marker_value = marker_value / 1
        return marker_value

    def query_marker_y(self, x: int) -> float:
        """
        读取mark值
        :param x: 1,2,3,4,5,6,7
        :return:
        """
        marker_value = self.query(f'CALC:MARK{x}:Y?')
        marker_value = float(marker_value.rstrip("\n"))
        return marker_value

    def set_save_csv_png(self, filename: str) -> None:
        """
        存csv与png
        :param filename: 文件名需包含路径，'Z:\\DATA\\186_5514\\186_5514_SIOA201P8_GND_REF300_12000_+35'
        :return:
        """

        # self.write('FORM:DEXP:HEAD ON')
        # self.write('FORM:DEXP:TRAC ALL')

        self.write(f'MMEM:NAME "{filename}.png"')
        self.write('HCOP:IMM')

        self.write('FORMat:DEXPort:FORMat CSV')  # CSV格式
        self.write(f'MMEM:STOR1:TRAC 1,"{filename}.csv"')
        logging.info('save_csv_png 运行完成')

    def set_mark_all_off(self) -> None:
        """
        关闭所有mark
        :return:
        """
        self.write('CALC:MARK:AOFF')
        logging.info('关闭所有mark')

    def set_auto_search_off(self) -> None:
        """
        auto_search关闭
        :return:
        """
        self.write(f'SENS:ADJ:CONF:FREQ:AUT:STAT OFF')
        logging.info('auto_search关闭')

    def set_all_markers_off(self) -> None:
        """
        所有marke关闭
        :return:
        """
        self.write(f'CALC1:MARK:AOFF')
        logging.info('all markers关闭')

    def set_trace_smoothing_state(self, trace: int, switch: Literal['ON', 'OFF']) -> None:
        """
        设置trace smoothing开启关闭
        :param trace:
        :param switch:
        :return:
        """
        self.write(f'DISP:TRAC{trace}:SMO {switch}')
        logging.info(f'设置trace{trace} smoothing: {switch}')

    def set_trace_smoothing_value(self, trace: int, value: float = 1.5) -> None:
        """
        设置trace smoothing值
        :param trace:
        :param value:
        :return:
        """
        self.write(f'DISP:TRAC{trace}:SMO ON')
        self.write(f'DISP:TRAC{trace}:SMO:APER {value}')
        logging.info(f'设置trace{trace} smoothing值: {value}')


class Rsa6000Sp(Rsa6000):
    def __init__(self, address: Optional[str] = None, config_path="config.yaml", model: str = "RSA6252"):
        super().__init__(address=address, config_path=config_path, model=model)

    def set_select_sp(self) -> None:
        """
        选择频谱模式窗口
        :return:
        """
        self.write('INST SAN')
        logging.info('选择频谱模式窗口')

    def set_freq_span(self, span: float, unit: Literal['GHz', 'MHz', 'kHz', 'Hz']) -> None:
        """
        设置span带宽
        :param unit:
        :param span:
        :return:
        """
        self.write(f'FREQ:SPAN {span}{unit}')
        logging.info(f'设置span带宽: {span}{unit}')

    def set_freq_span_full(self) -> None:
        """
        设置full span带宽

        :return:
        """
        self.write(f'SENS:FREQ:SPAN:FULL')
        logging.info(f'设置full span带宽')

    def set_peak_search(self) -> None:
        """
        peak search
        :return:
        """
        self.write(f'CALC:MARK:MAX')
        logging.info('设置峰值搜索')

    def set_continuous_peak(self, on_off: Literal['ON', 'OFF']) -> None:
        """
        自动peak开关:ON,OFF
        :param on_off:
        :return:
        """
        self.write(f'CALCulate1:MARKer1:MAXimum:AUTO {on_off}')
        logging.info(f'设置自动peak开关: {on_off}')

    def set_ref_level(self, value: float) -> None:
        """
        参考功率
        :param value:
        :return:
        """
        self.write(f'DISPlay:WINDow1:TRACe1:Y:SCALe:RLEVel {value}')
        logging.info(f'设置参考功率: {value}')

    def set_range_scal(self, value: float) -> None:
        """
        range
        :param value:
        :return:
        """
        self.write(f'DISP:WINDow1:SUBW:TRAC1:Y:SCAL {value}')
        logging.info(f'range范围: {value}')

    def set_rbw(self, set_rbw: float, unit: Literal['MHz', 'kHz', 'Hz']) -> None:
        """
        设置rbw
        :param unit:
        :param set_rbw:
        :return:
        """
        self.write(f'SENS:BAND:RES {set_rbw}{unit}')
        logging.info(f'设置rbw: {set_rbw}{unit}')

    def set_rbw_auto(self, ) -> None:
        """
        设置rbw auto
        :return:
        """
        self.write(f'SENS:BAND:RES:AUTO ON ')
        logging.info(f'设置rbw auto')

    def set_mkr_type(self, on_off: Literal['ON', 'OFF']) -> None:
        """
        设置norm delta
        :param on_off:
        :return:
        """
        self.write(f'CALC:DELT:STAT {on_off}')
        logging.info(f'设置norm delta: {on_off}')

    def query_delta_mkr_y(self, x: int) -> float:
        """
        查询delta mkr 功率
        :return:
        """
        delta_mkr_value = self.query(f'CALC:DELT{x}:Y?')
        return delta_mkr_value

    def query_delta_mkr_x(self, x: int, unit: Literal['GHz', 'MHz', 'kHz', 'Hz']) -> float:
        """
        查询delta mkr 频率
        :return:
        """
        delta_mkr_value = float(self.query(f'CALC:DELT{x}:X?'))
        if unit == 'GHz':
            delta_mkr_value = delta_mkr_value / 1e9
        elif unit == 'MHz':
            delta_mkr_value = delta_mkr_value / 1e6
        elif unit == 'kHz':
            delta_mkr_value = delta_mkr_value / 1e3
        return delta_mkr_value

    def set_mark_delt(self, x, freq: float, unit: Literal['MHz', 'kHz', 'Hz']) -> None:
        """
        :param x:
        :param freq:offset频率
        :param unit:单位
        :return:
        """
        self.write(f'CALC1:DELT{x}:STAT ON')
        self.write(f'CALC1:DELT{x}:X {freq}{unit}')
        logging.info(f'设置mark{x}的offset频率: {freq}{unit}')

    def set_peak_auto(self, on_off: Literal['ON', 'OFF']) -> None:
        """
        自动peak开关:ON,OFF
        :param on_off:
        :return:
        """
        self.write(f'CALCulate1:MARKer1:MAXimum:AUTO {on_off}')
        logging.info(f'设置自动peak开关: {on_off}')

    def set_mark_del_on(self, x) -> None:
        self.write(f'CALC1:DELT{x}:STAT ON')
        logging.info(f'设置mark{x}的offset频率为开启')

    def set_mark_to_center(self) -> None:
        self.write(f'CALC:MARK1:FUNC:CENT')
        logging.info('设置mark1为中心频率')

    def set_mark_del(self, x, freq: float, unit: Literal['MHz', 'kHz', 'Hz']) -> None:
        """
        :param x:
        :param freq:offset频率
        :param unit:单位
        :return:
        """
        self.write(f'CALC1:DELT{x}:STAT ON')
        time.sleep(0.01)
        self.write(f'CALC1:DELT{x}:X {freq}{unit}')
        logging.info(f'设置mark{x}的offset频率: {freq}{unit}')


if __name__ == '__main__':
    freq_set = 0.9
    rsa6252 = Rsa6000Sp(config_path="config.yaml", model="RSA6252")
    # fsv3030.set_freq_center(7.68, 'GHz')
    rsa6252.set_mark_all_off()
    rsa6252.set_run_single()
    rsa6252.set_mark_on(1)
    rsa6252.set_mark_del_on(1)
    # fsv3030.timeout = 0.1