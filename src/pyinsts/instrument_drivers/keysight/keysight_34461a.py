# 控制TH1963子程序
import time

from pyinsts.instrument_drivers.th1963.th1963 import Th1963



# 定义TH1963类，连接TH1963数字万用表
class DM34461A(Th1963):
    def __init__(self, address: str = None, config_path="config.yaml", model: str = "DM34461A"):
        super().__init__(address=address, config_path=config_path, model=model)


if __name__ == '__main__':
    star_time = time.time()
    
    dm34461a = DM34461A(config_path="config.yaml")
    # 一次获取多个测量值
    results = dm34461a.get_measurements('uA')
    print(f"电流: {results['current']} uA")
    print(f"电压: {results['voltage']} V")
    
    end_time = time.time()
    print(f"程序运行时间：{end_time - star_time}秒")
