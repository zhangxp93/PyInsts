import logging
import time

import pyvisa
from types import TracebackType
from typing import Callable, Optional, Type
import os
import inspect
from functools import wraps

from pyvisa import VisaIOError

from pyinsts.data import load_config


def handle_instrument_error(func: Callable) -> Callable:
    """仪器操作错误处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"{args[0].model} {func.__name__}失败: {e}")
            raise

    return wrapper


class BaseInstrument:
    """基础仪器控制类"""

    def __init__(self, address: Optional[str] = None, config_path: str = "config.yaml",
                 model: str = "E5052B"):
        """初始化仪器连接

        Args:
            address: 仪器地址，例如："USB0::0x0957::0x0E09::MY47402409::0::INSTR"
            config_path: 配置文件路径
            model: 仪器型号
        """
        # 设置基本属性
        self.model = model
        self.address = self._get_instrument_address(address, config_path)
        
        # 设置默认超时参数

        self.opc_timeout = 100  # 默认OPC超时时间100秒


        self.opc_poll_interval = 0.01  # 默认OPC轮询间隔0.01秒

        # 连接仪器
        self.idn = self._connect_instrument()

    # def __del__(self):
    #     """
    #     del的调用时机不确定，依赖于Python的垃圾回收机制。
    #     :return:
    #     """
    #     self.close()


    def _get_instrument_address(self, address: str, config_path: str) -> str:
        """获取仪器地址

        优先使用传入的地址，否则从配置文件读取
        支持.yaml和.json格式的配置文件
        """
        if address:
            return address

        # 处理配置文件路径
        if not os.path.isabs(config_path):
            # 获取继承类的文件所在目录
            derived_class_file = inspect.getmodule(self.__class__).__file__
            derived_class_dir = os.path.dirname(
                os.path.abspath(derived_class_file))
            config_path = os.path.join(derived_class_dir, config_path)

        # 如果没有指定扩展名，先尝试.yaml，再尝试.json
        if not os.path.splitext(config_path)[1]:
            yaml_path = config_path + '.yaml'
            json_path = config_path + '.json'
            
            if os.path.exists(yaml_path):
                config_path = yaml_path
            elif os.path.exists(json_path):
                config_path = json_path
                
        config = load_config(config_path)
        address = config.get("instruments_address", {}).get(self.model)
        if not address:
            raise ValueError(f"未找到{self.model}的仪器地址配置")

        return address

    def __enter__(self) -> "BaseInstrument":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        self.close()
        return False

    @handle_instrument_error
    def _connect_instrument(self) -> Optional[str]:
        """建立仪器连接，返回仪器标识"""
        max_retries = 3  # 最大重试次数

        retry_count = 0
        
        while retry_count < max_retries:
            try:
                print(f"型号:{self.model}, 地址:{self.address}")
                
                # ==== 处理模拟仪器的后端配置 ====
                rm_backend = ""  # 默认无特殊后端
                actual_address = self.address
                
                if "@sim" in self.address:
                    parts = self.address.split(";")
                    actual_address = parts[0]
                    
                    # 尝试通过项目结构自动定位对应的 yaml
                    # 获取 baseinstrument.py 所在目录: src/pyinsts/instrument_drivers
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    # 模拟配置目录在 src/pyinsts/instrument/sim
                    sim_dir = os.path.join(os.path.dirname(base_dir), "instrument", "sim")
                    # 推断 yaml 名称 (e.g. FSV3030 -> Fsv3030.yaml)
                    yaml_name = self.model[:1].upper() + self.model[1:].lower() + ".yaml"
                    yaml_path = os.path.join(sim_dir, yaml_name)
                    
                    if os.path.exists(yaml_path):
                        rm_backend = f"{yaml_path}@sim"
                    else:
                        rm_backend = "@sim"
                        
                if rm_backend:
                    self.rm = pyvisa.ResourceManager(rm_backend)
                else:
                    self.rm = pyvisa.ResourceManager()
                    
                self.instrument = self.rm.open_resource(actual_address)
                
                if rm_backend:
                    self.instrument.write_termination = '\n'
                    self.instrument.read_termination = '\n'

                self.instrument.write('*CLS')
                logging.info('清除仪器寄存器信息')

                # 验证连接
                idn = self.instrument.query("*IDN?")
                logging.info(f'仪器标识:{idn}, 成功连接{self.model}')
                return idn
            except(pyvisa.VisaIOError, pyvisa.VisaTypeError, TimeoutError):
                retry_count += 1
                if retry_count < max_retries:
                    logging.info(f"等待1秒后重试...")
                    time.sleep(1)
                    # 确保之前的连接被关闭
                    if hasattr(self, 'instrument'):
                        self.instrument.close()
                    if hasattr(self, 'rm'):
                        self.rm.close()
                else:
                    logging.error(f"连接失败次数超过最大重试次数({max_retries})")
                    raise

        return None


    @handle_instrument_error
    def write(self, command: str,
              check_complete: bool = False) -> None:
        """写入命令

        Args:
            command: SCPI命令
            check_complete: 是否等待命令完成

        example:
            self.write(f'SENSE1:FREQ:CENT 1GHz')
        """
        self.instrument.timeout = 100000
        self.instrument.write(command)
        if check_complete:
            self.wait_opc()
        logging.debug(f"{self.model} 写入: {command}")

    @handle_instrument_error
    def query(self, command: str,
              check_complete: bool = False) -> str:
        """查询命令

        Args:
            command: SCPI命令
            check_complete: 是否等待命令完成

        Returns:
            查询结果

        example:
            result = self.query("*IDN?")
            print(result)
        """
        self.instrument.timeout = 20000
        try:
            result = self.instrument.query(command)
            if check_complete:
                self.wait_opc()
            logging.info(f"{self.model} 查询: {command}, 结果: {result}")
            return result
        except VisaIOError as e:
            logging.error(f"{self.model} 查询失败: {e}")
            raise
    
    @handle_instrument_error
    def set_opc_timeout(self, timeout: float = 100, poll_interval: float = None):
        """临时设置OPC超时时间
        
        Args:
            timeout: 新的超时时间(秒)
            poll_interval: 新的轮询间隔(秒)，可选
        """
        self.opc_timeout = timeout
        if poll_interval is not None:
            self.opc_poll_interval = poll_interval
        logging.info(f"{self.model} 设置超时时间: {timeout}秒, 轮询间隔: {poll_interval or self.opc_poll_interval}秒")

    @handle_instrument_error
    def wait_opc(self, timeout=None, opc_poll_interval=None):
        """等待OPC完成
        Args:
            timeout: 超时时间(秒)，默认使用 self.opc_timeout
            opc_poll_interval: 轮询间隔(秒)，默认使用 self.opc_poll_interval
        """
        effective_timeout = self.opc_timeout if timeout is None else timeout
        effective_poll = self.opc_poll_interval if opc_poll_interval is None else opc_poll_interval
        try:
            start_time = time.time()
            logging.info(f"开始等待opc?")

            while True:
                try:
                    opc = self.instrument.query("*OPC?")
                    if opc.strip() == '1':
                        logging.info("opc运行完成")
                        break
                except VisaIOError as e:
                    logging.warning(f"OPC查询失败: {str(e)}")
                    # break  # 通信异常时终止

                elapsed = time.time() - start_time
                if elapsed >= effective_timeout:
                    logging.warning(f"运行超时（已耗时：{elapsed:.1f}秒）")
                    break
                time.sleep(effective_poll)
            end_time = time.time()
            total_time = end_time - start_time
            logging.info(f"总运行时间: {total_time:.2f}秒")
            return total_time  # 返回时间供外部使用
        except Exception as e:
            logging.error(f"发生错误: {str(e)}")
            return str(e)

    @handle_instrument_error
    def close(self) -> None:
        """关闭仪器连接"""
        if hasattr(self, "instrument") and self.instrument:
            self.instrument.close()
            self.instrument = None
        if hasattr(self, "rm") and self.rm:
            self.rm.close()
            self.rm = None
        logging.info(f"{self.model} 连接已关闭")

