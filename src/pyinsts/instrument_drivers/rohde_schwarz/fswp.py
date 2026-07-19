import logging
from typing import Literal
import time
from .fsv3030 import FSV3030Sp, FSV3030Base


# 定义Fswp类，连接Fswp信号源分析仪
class FswpSp(FSV3030Sp):
    """
    继承Fsv3030Sp类
    频谱模式
    """
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "FSWP-26"):
        super().__init__(address=address, config_path=config_path, model=model)
        self.set_window(window='Spectrum')  # 设置窗口为频谱模式


class FswpPN(FSV3030Base):
    """
    相噪模式
    """
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "FSWP-26"):
        super().__init__(address=address, config_path=config_path, model=model)
        # self.set_window(window='Phase Noise')  # 设置窗口为相噪模式

    def set_auto_search_freq_start_stop(self, start_freq, stop_freq):
        """
        设置自动搜索开始截至频率范围
        :param start_freq:
        :param stop_freq:
        :return:
        """
        self.write(f'SENS:ADJ:CONF:FREQ:LIM:LOW {start_freq}GHz')
        self.write(f'SENS:ADJ:CONF:FREQ:LIM:HIGH {stop_freq}GHz')
        logging.info(f'设置自动搜索频率范围: {start_freq}GHz 到 {stop_freq}GHz')

    def query_signal(self) -> bool:
        """
        查询有无信号输入
        :return:
        """
        value = self.query('STAT:QUES:PNO:COND?').strip()
        if value == '0':
            value = True
        else:
            value = False
        return value

    def set_xcorr_factor(self,value:int):
        """
        设置互相关系数,数字越大扫面完一次的时间越久
        :param value:
        :return:
        """
        self.write(f'SENS:SWE:XFAC {value}')
        logging.info(f'设置互相关系数为{value}')

    def set_scaling(self,top:int,bottom:int):
        """
        设置互相关系数,数字越大扫面完一次的时间越久
        :param top:
        :param bottom:
        :return:
        """
        self.write(f'DISP:WIND1:TRAC:Y:SCAL:AUTO OFF')
        self.write(f'DISP:WIND1:TRAC:Y:SCAL:RLEV {top}')
        self.write(f'DISP:WIND1:TRAC:Y:SCAL:RLEV:LOW {bottom}')
        logging.info(f'设置scaling,top:{top},bottom:{bottom}')

    def set_select_pn(self) -> None:
        """
        选择相噪模式窗口
        :return:
        """
        self.write('INST PNO')
        logging.info('选择相噪模式窗口')

    def set_marker_x(self, mark, offset, unit:Literal['MHz', 'kHz', 'Hz']) -> None:
        """
        设置marker
        :param unit:
        :param mark:
        1,2,3,4,5,6,7
        :param offset:1K,10K,100K,1M,10M,20M,100M
        :return:
        """
        self.write(f'CALC:MARK{mark} ON')  # 打开marker
        self.write(f'DISP:MTAB ON')  # 显示marker表
        self.write(f'CALC:MARK{mark}:X {offset}{unit}')
        time.sleep(0.01)
        logging.info(f'设置marker{mark}的偏移量: {offset}{unit}')

    def set_freq_offset_range(self, 
                              start_offset: float, star_unit: Literal['MHz', 'kHz', 'Hz'], 
                              stop_offset: float, stop_unit: Literal['MHz', 'kHz', 'Hz']) -> None:
        """
        设置频率偏移范围
        :param start_offset: 起始频率偏移
        :param star_unit: 起始频率单位
        :param stop_offset: 结束频率偏移
        :param stop_unit: 结束频率单位
        :return:
        """
        self.write(f'SENS:FREQ:STAR {start_offset}{star_unit}')
        self.write(f'SENS:FREQ:STOP {stop_offset}{stop_unit}')
        logging.info(f'设置频率偏移范围: {start_offset}{star_unit} 到 {stop_offset}{stop_unit}')

    def query_rms(self,range=1) -> float:
        """
        读取积分抖动rms,fs
        :return: jitter_value or -99 if error occurs
        """
        try:
            jitter_value = float(self.query(f'FETC:RANG{range}:PNO1:RMS?')) * 1e15
            logging.info(f'jitter时间：{jitter_value}')
            return jitter_value
        except Exception as e:
            logging.error(f'读取jitter失败: {e}')
            return -99

    def set_dc_power_switch(self, switch:Literal['ON', 'OFF']) -> None:
        """
        设置DC POWER
        :param switch:ON,OFF
        :return:
        """
        self.write(f'SOUR:VOLT {switch}')
        logging.info(f'设置DC POWER: {switch}')

    def set_dc_supply_volt(self, volt:float) -> None:
        """
        设置DC voltage supply
        :param volt:电压值
        :return:
        """
        self.write(f'SOUR:VOLT:POW:LEV:AMPL {volt}')
        logging.info(f'设置DC voltage supply: {volt}')

    def set_vtune(self, vt:float) -> None:
        """
        设置vt电压
        :param vt:
        :return:
        """
        self.write(f'SOUR:VOLT:CONT:LEV:AMPL {vt}')
        logging.info(f'设置vt电压: {vt}')

    def query_freq_cent(self, unit:Literal['GHz', 'MHz', 'kHz', 'Hz']) -> float:
        """
        查询频率
        :param unit:
        :return:
        """
        freq = float(self.query(f'FREQ:CENT?'))
        if unit == 'GHz':
            freq = freq / 1e9
        elif unit == 'MHz':
            freq = freq / 1e6
        elif unit == 'kHz':
            freq = freq / 1e3
        elif unit == 'Hz':
            freq = freq / 1
        logging.info(f'查询频率: {freq}{unit}')
        return freq

    def query_singal_power(self) -> float:
        power = float(self.query(f'POW:RLEV?'))
        logging.info(f'查询信号功率: {power}')
        return power


    def set_signal_source_freq(self, freq:float, unit:Literal['GHz', 'MHz', 'kHz', 'Hz']) -> None:
        """
        设置源频率，GHz
        :param unit:
        :param freq:
        :return:
        """
        self.write(f'SOUR:GEN:FREQ {freq}{unit}')
        logging.info(f'设置源频率: {freq}{unit}')

    def set_signal_source_pow(self, power:float) -> None:
        """
        设置源功率，dBm
        :return:
        """
        self.write(f'SOUR:GEN:LEV {power}')
        logging.info(f'设置源功率: {power}')

    def set_signal_source_switch(self, switch:Literal['ON', 'OFF']) -> None:
        """
        设置源功率开关,ON,OFF
        :return:
        """
        self.write(f'SOUR:GEN:STAT {switch}',check_complete=True)
        logging.info(f'设置源功率开关: {switch}')

    def query_singal_level(self):
        """
        读取singal_level
        :return:
        """
        singal_level = self.query(f"POW:RLEV?")
        return singal_level

    def query_trace(self, trace:int=1):
        """
        vco模式读取trac1,GHZ
        :return:
        """
        get_value = self.query(f"TRAC{trace}? TRACE1")
        get_value = get_value.split(',')
        freq_offset = [get_value[i] for i in range(0, len(get_value), 2)]   # 0为起始索引，2为步长
        value = [get_value[i] for i in range(1, len(get_value), 2)]
        freq_offset = [float(item)  for item in freq_offset]
        value = [float(item) for item in value]
        return freq_offset,value

    def query_trace1(self, trace:int=1):
        """
        vco模式读取trac1,GHZ
        :return:
        """
        get_value = self.query(f"TRAC{trace}? TRACE1")
        get_value = get_value.split(',')
        # get_value = [get_value[i] for i in range(0, len(get_value), 2)]   # 0为起始索引，2为步长
        get_value = [float(item) for item in get_value]
        get_value = {get_value[i]: get_value[i+1] for i in range(0, len(get_value), 2)}
        return get_value


class FswpVcoChar(FSV3030Base):
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "FSWP-26"):
        super().__init__(address=address, config_path=config_path, model=model)


    def set_dc_power_switch(self, switch:Literal['ON', 'OFF']) -> None:
        """
        设置DC POWER
        :param switch:ON,OFF
        :return:
        """
        self.write(f'SOUR:VOLT {switch}')
        logging.info(f'设置DC POWER: {switch}')

    def set_dc_supply_volt(self, volt:float) -> None:
        """
        设置DC voltage supply
        :param volt:电压值
        :return:
        """
        self.write(f'SOUR:VOLT:POW:LEV:AMPL {volt}')
        logging.info(f'设置DC voltage supply: {volt}')

    def set_vtune(self, vt:float) -> None:
        """
        设置vt电压
        :param vt:
        :return:
        """
        self.write(f'SOUR:VOLT:CONT:LEV:AMPL {vt}')
        logging.info(f'设置vt电压: {vt}')

    def set_smooth_state(self, wind:int, trace:int, switch:Literal['ON', 'OFF']) -> None:
        """
        设置频谱平滑状态
        :param wind:
        :param trace:
        :param switch:
        :return:
        """
        self.write(f'DISP:WIND{wind}:TRAC{trace}:SMO:STAT {switch}')
        logging.info(f'设置平滑状态: 窗口{wind}，轨迹{trace}，平滑{switch}')

    def set_sweep_vt(self, start_vt:float, stop_vt:float, step_vt:float, init_time:float=0, point_time:float=0, freq_res:float=1e3) -> None:
        """
        设置vco模式,vt电压扫描值等
        :param start_vt: 起始电压
        :param stop_vt: 结束电压
        :param step_vt: 步长；
        :param init_time: 初始时间
        :param point_time: 测量点时间
        :param freq_res: 频率分辨率
        :return:
        """
        meas_points = int((stop_vt - start_vt) / step_vt) + 1
        self.write(f'CONF:VCO:SWE:STAR {start_vt}') # 设置起始电压
        self.write(f'CONF:VCO:SWE:STOP {stop_vt}') # 设置结束电压
        self.write(f'CONF:VCO:SWE:POIN {meas_points}') # 设置测量点数
        self.write(f'CONF:VCO:SWE:DEL:INIT {init_time}') # 设置初始时间
        self.write(f'CONF:VCO:SWE:DEL {point_time}') # 设置测量点时间
        self.write(f'CONF:VCO:SWE:FCO {freq_res}KHz') # 频率分辨率

    def query_freq(self, trace:int=1) -> list[float]:
        """
        vco模式读取trac1,GHZ
        :return:
        """
        freq = self.query(f"TRAC{trace}? TRACE1")
        freq = freq.split(',')
        freq = [freq[i] for i in range(1, len(freq), 2)]
        freq = [float(item) / 1e9 for item in freq]
        return freq

    def query_vt(self, trace:int=1) -> list[float]:
        """
        vco模式读取trac1
        :return:
        """
        vt = self.query(f"TRAC{trace}? TRACE1")
        vt = vt.split(',')
        vt = [vt[i] for i in range(0, len(vt), 2)]
        vt = [float(item) for item in vt]
        return vt

    def query_power(self, trace:int=2) -> list[float]:
        """
        vco模式读取trac2
        :return:
        """
        power = self.query(f"TRAC{trace}? TRACE1")
        power = power.split(',')
        power = [power[i] for i in range(1, len(power), 2)]
        power = [float(item) for item in power]
        return power

    def query_sen(self, trace:int=3) -> list[float]:
        """
        vco模式读取trac3,调谐灵敏度
        :return:
        """
        sen = self.query(f"TRAC{trace}? TRACE1")
        sen = sen.split(',')
        sen = [sen[i] for i in range(1, len(sen), 2)]
        sen = [float(item) / 1e6 for item in sen]
        return sen

    def query_icc(self, trace:int=4) -> list[float]:
        """
        vco模式读取trac4
        :return:
        """
        icc = self.query(f"TRAC{trace}? TRACE1")
        icc = icc.split(',')
        icc = [icc[i] for i in range(1, len(icc), 2)]
        icc = [float(item) / 1e6 for item in icc]
        return icc

    def set_freq_search_range(self, freq_start, freq_stop, unit:Literal['GHz', 'MHz', 'kHz', 'Hz']) -> None:
        self.write(f"ADJ:CONF:FREQ:LIM:LOW {freq_start}{unit}")
        self.write(f"ADJ:CONF:FREQ:LIM:HIGH {freq_stop}{unit}")

    def set_sweep_time(self,sweep_time:float):
        self.write(f"CONF:VCO:SWE:DEL:POIN {sweep_time}")



class FswpSpotNoiseTune(FSV3030Base):
    def __init__(self, instrument_address):
        super().__init__(instrument_address)

    def query_phase(self, trace:int) -> list[float]:
        phase = self.query(f"TRAC1? TRACE{trace}")
        phase = phase.split(',')
        phase = [phase[i] for i in range(1, len(phase), 2)]
        phase[-1] = phase[-1].rstrip("\n")
        return phase

    def query_phase_vt(self, trace:int) -> list[float]:
        phase_vt = self.query(f"TRAC1? TRACE{trace}")
        phase_vt = phase_vt.split(',')
        phase_vt = [phase_vt[i] for i in range(0, len(phase_vt), 2)]
        return phase_vt


if __name__ == '__main__':
    # addr_fswp = 'TCPIP0::172.16.30.132::inst0::INSTR'
    # addr_fswp_1 = "USB0::0x0AAD::0x011F::101936::0::INSTR"
    # addr_fswp = 'USB0::0x0AAD::0x011F::101380::INSTR'

    addr_fswp = 'USB0::0x0AAD::0x011F::101380::INSTR'
    pn = FswpPN(address=addr_fswp,model= 'FSWP26')
    # a = pn.query_signal()
    a = pn.query_marker_y(1)
    print(a)
    pn.set_run_single()
    a = pn.query_marker_y(1)
    print(a)
    # vco = FswpVcoChar('USB0::0x0AAD::0x011F::101380::INSTR')
    # vco.set_window('Phase Noise 2')
    # vco.set_run_single()
    # a = vco.query_freq()
    # print(a)

    # pn.set_marker_x(1, 1000, unit='Hz')  # 100Hz

    addr_fswp = 'USB0::0x0AAD::0x0290::101071::0::INSTR'
    # fswp = Fswp('USB0::0x0AAD::0x0290::101071::0::INSTR')
    pn = FswpPN(address=addr_fswp,model= 'FSPN26')
    pn.set_marker_x(1, 1000, unit='Hz')  # 100Hz

