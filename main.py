"""
@date: 2024-11-24
@author: zhangxp93
@contact: 937097345@qq.com

您可以免费地使用、修改和分发PyInsts ，但必须包含原始作者的版权声明和下列许可声明。

You may use, modify, and distribute pyinsts free of charge, but you must include
the original author's copyright notice and the following license notice.
"""
from pyinsts.data import setup_logging
from pyinsts.instrument_drivers import FswpPN

# 这是一个示例 Python 脚本。



fswp_addr = 'TCPIP::192.168.1.1::INSTR'
n9020b_addr = 'TCPIP::192.168.1.2::INSTR'

setup_logging()


if __name__ == '__main__':
    fswp = FswpPN(fswp_addr)
    fswp.close()

