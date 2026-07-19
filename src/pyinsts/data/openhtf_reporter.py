"""OpenHTF SQLite 报告模块。

提供一个可重用的回调类，用于将 OpenHTF 测试结果报告到 SQLite 数据库和 Excel 文件，
符合 RFChipTest 项目结构要求。
"""

import os
import logging
import json
import sqlite3
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

import openhtf as htf
from openhtf.util import data as htf_data

# 尝试导入项目内部的 SQL 模块，如果失败则提供 mock 以便测试
try:
    from src.pyinsts.data.sql import save_data_to_spl
except ImportError:
    logging.warning("无法导入 src.pyinsts.data.sql。save_data_to_spl 将被模拟(mock)。")
    save_data_to_spl = None

class OpenHTFSQLiteReporter:
    """处理将 OpenHTF 测试结果报告到 SQLite 数据库和 Excel。

    Attributes:
        db_path: SQLite 数据库文件的绝对路径。
        table_name: 插入数据的表名。
        model_name: 被测芯片的型号名称。
        test_type: 测试类型 (例如: '验证', '量产').
    """

    def __init__(
        self,
        db_path: str,
        table_name: str,
        model_name: str,
        test_type: str = '验证',
        result_at_end: bool = True,
        json_export_path: Optional[str] = None,
        enable_excel: bool = True
    ):
        """初始化 OpenHTFSQLiteReporter。

        Args:
            db_path: 数据库文件的绝对路径。
            table_name: 数据库表名。
            model_name: 芯片型号。
            test_type: 测试类型，默认为 '验证'。
            result_at_end: 是否将测试结果列放在最后，默认为 True。
            json_export_path: 用于导出汇总 JSON 的路径。如果为 None，则不执行汇总导出。
            enable_excel: 是否启用 Excel 实时导出。
        """
        self.db_path = db_path
        self.table_name = table_name
        self.model_name = model_name
        self.test_type = test_type
        self.result_at_end = result_at_end
        self.json_export_path = json_export_path
        self.enable_excel = enable_excel
        
        # 自动推导日志目录：在 db_path 同级目录下创建 logs 文件夹
        self.logs_dir = os.path.join(os.path.dirname(db_path), 'logs')
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir, exist_ok=True)

    def __call__(self, record: htf.TestRecord):
        """测试结束时由 OpenHTF 调用的回调函数。"""
        print(f"[{record.dut_id}] 正在处理测试结果并保存到 SQL...")
        try:
            # 1. 准备 JSON 数据并保存到文件
            record_dict = htf_data.convert_to_base_types(record)
            json_str = json.dumps(record_dict, ensure_ascii=False, indent=4)
            
            # 生成唯一文件名: {时间戳}_{DUT}.json
            start_time_str = datetime.fromtimestamp(record.start_time_millis / 1000.0).strftime('%Y%m%d_%H%M%S')
            safe_dut_id = str(record.dut_id).replace(':', '_').replace('/', '_')
            filename = f"{start_time_str}_{safe_dut_id}.json"
            file_path = os.path.join(self.logs_dir, filename)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_str)

            # 2. 提取常规测试数据 (PN 表) 并合并 JSON 路径
            data = self._extract_data(record)
            data['JSON_Log_Path'] = file_path # 将路径作为一列添加到主表
            
            # 保存主表 (PN 表)
            # 使用 inst.enable_excel 控制常规数据是否导出 Excel
            self._save_to_db(data, self.table_name, export_excel=self.enable_excel)

            # 3. 如果配置了导出路径，从数据库导出完整的 JSON 文件 (聚合)
            if self.json_export_path:
                self._export_json_from_db(self.table_name)
            
        except Exception as e:
            print(f"保存结果失败: {e}")
            traceback.print_exc()

    def _export_json_from_db(self, table_name: str):
        """从数据库读取所有 JSON 文件路径，读取内容并导出为单一 JSON 文件。"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # 从主表读取 JSON_Log_Path 列
                cursor.execute(f"SELECT JSON_Log_Path FROM {table_name}")
                rows = cursor.fetchall()
                
                all_records = []
                for row in rows:
                    json_path = row[0]
                    if json_path and os.path.exists(json_path):
                        try:
                            with open(json_path, 'r', encoding='utf-8') as f:
                                record = json.load(f)
                                all_records.append(record)
                        except Exception as e:
                            logging.warning(f"无法读取 JSON 日志文件 {json_path}: {e}")
                
                # 写入聚合文件
                with open(self.json_export_path, 'w', encoding='utf-8') as f:
                    json.dump(all_records, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            # 可能是旧数据没有 JSON_Log_Path 列，或者其他错误
            print(f"导出 JSON 文件失败: {e}")

    def _extract_data(self, record: htf.TestRecord) -> Dict[str, Any]:
        """从 TestRecord 中提取并格式化数据。

        Returns:
            符合 SQL 处理程序要求的字典。
        """
        start_time_ms = record.start_time_millis
        start_time_str = datetime.fromtimestamp(start_time_ms / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
        test_result = str(record.outcome).split('.')[-1] # PASS/FAIL

        # 1. 收集所有阶段的测量值
        all_measurements = {}
        for phase in record.phases:
            all_measurements.update(phase.measurements)

        # 辅助函数：安全提取数值
        def get_val(name, scale=1.0):
            meas = all_measurements.get(name)
            if meas and meas.measured_value is not None:
                if hasattr(meas.measured_value, 'value'):
                    return meas.measured_value.value / scale
                return meas.measured_value / scale
            return None

        # 2. 初始化基本信息
        data = {
            '测试时间': start_time_str,
            '型号': self.model_name,
            '芯片编号': record.dut_id,
            '测试类型': self.test_type,
        }
        
        # 如果不放在最后，则按照原来习惯放在元数据之后
        if not self.result_at_end:
            data['测试结果'] = test_result

        # 3. 自动转换所有测量项
        for name, measurement in all_measurements.items():
            if measurement.measured_value is None:
                continue
            
            # 使用辅助函数获取原始值（未缩放）
            val = get_val(name, scale=1.0)
            
            if 'frequency' in name.lower() and 'hz' in name.lower():
                 data[f'{name}(MHz)'] = val / 1e6
            else:
                 data[name] = val
        
        # 4. 如果配置了放在最后 (默认)
        if self.result_at_end:
            data['测试结果'] = test_result

        return data

    def _save_to_db(self, data: Dict[str, Any], table_name: str, export_excel: bool = True):
        """将格式化的数据保存到数据库。"""
        if save_data_to_spl:
            save_data_to_spl(
                db_path=self.db_path,
                table_name=table_name,
                data=data,
                export_excel=export_excel
            )
            # 只有导出 Excel 时才提示 Export，否则只提示 Save To DB
            if export_excel:
                 print(f"数据成功保存到数据库表 {table_name}: {self.db_path} (已导出Excel)")
            else:
                 print(f"数据成功保存到数据库表 {table_name}: {self.db_path}")

        else:
            print(f"[Mock] 数据保存到 {table_name} (因为找不到 sql 模块):", data)


def configure_reporters(
    test: htf.Test,
    data_dir: str,
    file_name_prefix: str,
    table_name: str,
    model_name: str,
    test_type: str = '验证',
    enable_sql: bool = True,
    enable_excel: bool = True,
    enable_json: bool = False,
    result_at_end: bool = True
):
    """一键配置和添加 OpenHTF 报告器 (SQL 和 JSON)。

    Args:
        test: OpenHTF Test 对象。
        data_dir: 数据保存的目录路径。
        file_name_prefix: 文件名前缀 (不含扩展名)，例如 'demo_result'。
                          将生成 'demo_result.db', 'demo_result.xlsx', 'demo_result.json'。
        table_name: 数据库表名。
        model_name: 芯片型号名称。
        test_type: 测试类型。
        enable_sql: 是否启用 SQL 报告 (数据库)。
        enable_excel: 是否在每次测试后刷新 Excel 文件。建议大数据量时关闭。
        enable_json: 是否启用 JSON 报告 (汇总导出到单一文件)。
        result_at_end: 是否将测试结果(PASS/FAIL)放在最后。默认为 True。
    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)

    # 1. 自动生成路径
    db_path = os.path.join(data_dir, f"{file_name_prefix}.db")
    json_path = os.path.join(data_dir, f"{file_name_prefix}.json") if enable_json else None

    # 2. 配置 SQL/JSON 混合报告器
    if enable_sql:
        sql_reporter = OpenHTFSQLiteReporter(
            db_path=db_path,
            table_name=table_name,
            model_name=model_name,
            test_type=test_type,
            result_at_end=result_at_end,
            json_export_path=json_path, # 传递 JSON 导出路径 (如果 None 则不导出)
            enable_excel=enable_excel   # 传递 Excel 开关
        )
        test.add_output_callbacks(sql_reporter)




class TestSpecs:
    """管理测试规格和限制。

    Attributes:
        specs: 一个将测量名称映射到其 (min, max) 限制的字典。
               使用 None 表示没有限制。
               例如: {'输出功率(dBm)': (1.0, 2.0), '频率': (None, None)}
    """

    def __init__(self, specs: Dict[str, Tuple[Optional[float], Optional[float]]]):
        """使用给定的规格初始化 TestSpecs。"""
        self.specs = specs

    def get_measurements(self) -> List[htf.Measurement]:
        """根据规格生成 OpenHTF Measurement 对象。

        Returns:
            配置好的 htf.Measurement 对象列表，可以直接传递给 @htf.measures(*list)。
        """
        measurements = []
        for name, limits in self.specs.items():
            meas = htf.Measurement(name)
            
            # 安全检查 limits 格式
            if not isinstance(limits, (list, tuple)) or len(limits) != 2:
                # 如果格式不对，默认不加限制，但建议用户检查
                measurements.append(meas)
                continue

            min_val, max_val = limits
            
            # 如果有具体的范围限制
            if min_val is not None and max_val is not None:
                meas = meas.in_range(min_val, max_val)
            # 只有下限
            elif min_val is not None:
                meas = meas.in_range(min_val, float('inf'))
            # 只有上限
            elif max_val is not None:
                meas = meas.in_range(float('-inf'), max_val)
            
            measurements.append(meas)
        return measurements


