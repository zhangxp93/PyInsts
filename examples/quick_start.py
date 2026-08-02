"""
PyInsts 快速入门示例 (Quick Start Example)

展示如何使用 PyInsts 库连接频谱分析仪、设置参数并读取测量结果。
本示例支持连接真实物理仪器，也支持通过仿真地址（包含 ;@sim）进行无硬件测试。
"""

import logging
from pyinsts.data import setup_logging
from pyinsts.instrument_drivers import FSV3030Sp

# 1. 初始化日志（支持控制台彩色日志显示与 Loguru 记录）
setup_logging(log_level=logging.INFO)


def main():
    # 示例: 连接 R&S FSV3030 频谱分析仪
    # 使用包含 ";@sim" 的仿真地址可在无实体硬件环境下直接运行测试
    sim_address = "USB::0x0AAD::0x0119::100001::INSTR;@sim"

    print("=== 开始 R&S FSV3030 频谱仪控制示例 ===")
    try:
        # 使用 context manager 自动建立连接并在退出时自动关闭释放资源
        with FSV3030Sp(address=sim_address, model="FSV3030") as spec:
            print(f"成功连接仪器，IDN: {spec.idn}")

            # 1. 设置中心频率为 1.0 GHz
            spec.set_freq_center(1.0, "GHz")

            # 2. 设置频跨 (Span) 为 10 MHz
            spec.set_freq_span(10.0, "MHz")

            # 3. 设置 RBW 为自动模式
            spec.set_rbw_auto()

            # 4. 触发 Peak Search 峰值查找
            spec.set_peak_search()

            # 5. 清除状态并等待命令执行完成
            spec.write("*CLS")
            spec.wait_opc()

            print("仪器控制流程成功执行完毕！")

    except Exception as e:
        print(f"仪器控制过程中发生错误: {e}")


if __name__ == "__main__":
    main()
