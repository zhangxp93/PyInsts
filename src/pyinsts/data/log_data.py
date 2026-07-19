import logging
import os
import sys
import time
from loguru import logger
from functools import wraps

# --- 拦截器：将标准 logging 的消息转发给 loguru ---
class InterceptHandler(logging.Handler):
    """
    一个通用的 logging Handler，将接收到的 LogRecord 转发给 loguru 记录器。
    通过 patch 机制，直接使用 LogRecord 中已有的调用位置信息，彻底解决行号错误问题。
    """
    def emit(self, record):
        # 获取对应的 loguru 日志级别名
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 定义一个 patch 函数，修正用于显示的模块名、函数名和行号
        def patcher(loguru_record):
            # 直接修改 record 字典中的基础类型字段，这些字段是可写的
            # record.module 对应 {name}, record.funcName 对应 {function}, record.lineno 对应 {line}
            loguru_record["name"] = record.module
            loguru_record["function"] = record.funcName
            loguru_record["line"] = record.lineno

        # 使用 patch 注入信息，bind 绑定原始记录器名（如 pyvisa）
        # 注意：我们不再尝试修改只读的 loguru_record["file"] 对象
        logger.opt(exception=record.exc_info).patch(patcher).bind(raw_name=record.name).log(level, record.getMessage())

def setup_logging(log_file=None, log_level=logging.INFO, max_bytes=10 * 1024 * 1024, 
                  backup_count=5, use_timed_rotating=False, log_to_file=True,
                  console_level=None, file_level=None):
    """
    使用 loguru 作为后端重新配置异步日志记录。
    """
    # 转换 logging 级别为 loguru 字符串格式
    if isinstance(log_level, int):
        level_name = logging.getLevelName(log_level)
    else:
        level_name = log_level
    
    # 1. 拦截原生 logging 的所有输出
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # 2. 清除 loguru 的默认处理程序
    logger.remove()

    # 3. 配置控制台处理器
    c_level = logging.getLevelName(console_level) if console_level else level_name
    
    # 定义控制台格式：时间 | 级别 | 原始名称 | 模块名:函数名:行号 - 消息
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<magenta>{extra[raw_name]: <10}</magenta> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    
    logger.add(sys.stdout, level=c_level, format=console_format, colorize=True)

    # 4. 配置异步文件处理器
    if log_to_file:
        if log_file is None:
            log_file = os.getenv('LOG_FILE_PATH', 'log/test.log')
            
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        f_level = logging.getLevelName(file_level) if file_level else level_name
        file_format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra[raw_name]: <10} | {name}:{function}:{line} - {message}"

        rotation = "00:00" if use_timed_rotating else f"{max_bytes} B"

        logger.add(
            log_file,
            level=f_level,
            format=file_format,
            rotation=rotation,
            retention=backup_count,
            compression="zip",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            encoding="utf-8"
        )

    # 默认绑定 raw_name 为 ROOT
    logger.configure(extra={"raw_name": "ROOT"})

    logger.info("=" * 60)
    logger.info(f"Loguru 异步后端日志系统已启动".center(60, ' '))
    logger.info("=" * 60)
    
    return logger


def log_data(data, level=logging.INFO, logger_instance=None):
    """记录数据的日志"""
    _logger = logger_instance or logger
    lvl = logging.getLevelName(level) if isinstance(level, int) else level
    _logger.log(lvl, f"数据记录: {data}")


def log_exceptions(logger_instance=None, reraise=True, level=logging.ERROR):
    """异常处理装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _logger = logger_instance or logger
            lvl = logging.getLevelName(level) if isinstance(level, int) else level
            with _logger.catch(level=lvl, reraise=reraise):
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator


class LogContext:
    """耗时统计上下文管理器"""
    def __init__(self, enter_message, exit_message=None, logger_instance=None, level=logging.INFO):
        self.enter_message = enter_message
        self.exit_message = exit_message or f"完成: {enter_message}"
        self.logger = logger_instance or logger
        self.level = logging.getLevelName(level) if isinstance(level, int) else level
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        self.logger.log(self.level, self.enter_message)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        if exc_type:
            self.logger.error(f"在 '{self.enter_message}' 期间发生异常")
        else:
            self.logger.log(self.level, f"{self.exit_message} (耗时: {duration:.3f}秒)")
        return False


if __name__ == "__main__":
    log = setup_logging(log_level=logging.DEBUG)
    log.info("测试异步 Loguru 后端")
    logger.info('调试')
    logger.error('错误')
    log.error('错误')
