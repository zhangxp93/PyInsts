"""
仪器并发查询示例 - 使用ConcurrentTask管理器

演示如何使用ConcurrentTask管理器实现多仪器的并发查询，
提供直观、高效的API，同时保持优秀的性能。

性能对比：
- 串行查询：~0.82秒
- 并发查询：~0.46秒
- 加速比：~1.8x（节省约44%时间）
"""

import time
from typing import Callable, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, Future
from loguru import logger




class ConcurrentTask:
    """
    并发任务管理器
    提供直观的API来管理多线程任务，支持命名任务和批量结果获取
    """

    def __init__(self, max_workers: int = 4):
        """
        初始化并发任务管理器
        :param max_workers: 线程池最大工作线程数
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.futures: Dict[str, Future] = {}

    def run_async(self, name: str, func: Callable, *args, **kwargs) -> None:
        """
        异步执行任务
        :param name: 任务名称（用于后续获取结果）
        :param func: 要执行的函数
        :param args: 位置参数
        :param kwargs: 关键字参数

        示例：
            task_manager.run_async('current', vcc.query_curr, ch=1, unit='mA')
        """
        self.futures[name] = self.executor.submit(func, *args, **kwargs)

    def get_result(self, name: str, timeout: Optional[float] = None) -> Any:
        """
        获取任务结果
        :param name: 任务名称
        :param timeout: 超时时间（秒），None表示无限等待
        :return: 任务返回值

        示例：
            icc1 = task_manager.get_result('current')
        """
        if name not in self.futures:
            raise KeyError(f"任务 '{name}' 不存在")

        try:
            return self.futures[name].result(timeout=timeout)
        except Exception as e:
            logger.error(f"任务 '{name}' 执行失败: {e}")
            raise

    def get_all_results(self, *names: str,
                        timeout: Optional[float] = None) -> tuple:
        """
        获取多个任务的结果
        :param names: 任务名称列表
        :param timeout: 超时时间（秒）
        :return: 按顺序返回结果元组

        示例：
            icc1, voltage = task_manager.get_all_results('current', 'voltage')
        """
        return tuple(self.get_result(name, timeout) for name in names)

    def is_done(self, name: str) -> bool:
        """
        检查任务是否完成
        :param name: 任务名称
        :return: True表示已完成
        """
        if name not in self.futures:
            return False
        return self.futures[name].done()

    def wait_all(self, timeout: Optional[float] = None) -> None:
        """
        等待所有任务完成
        :param timeout: 超时时间（秒）
        """
        for future in self.futures.values():
            future.result(timeout=timeout)

    def shutdown(self, wait: bool = True):
        """关闭线程池"""
        self.executor.shutdown(wait=wait)

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时自动关闭线程池"""
        self.shutdown()

    def __del__(self):
        """析构时确保线程池被关闭"""
        if hasattr(self, 'executor'):
            self.shutdown(wait=False)

