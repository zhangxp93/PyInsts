import os
import json
import yaml
import logging


def load_config(config_path="config.yaml"):
    """加载配置文件，支持YAML和JSON格式
    
    Args:
        config_path: 配置文件路径(.yaml或.json)
        
    Returns:
        配置字典
    """
    if not os.path.exists(config_path):
        logging.error(f"配置文件未找到: {config_path}")
        raise FileNotFoundError(f"配置文件未找到: {config_path}")
        
    file_ext = os.path.splitext(config_path)[1].lower()
    
    with open(config_path, "r", encoding="utf-8") as file:
        try:
            if file_ext in ['.yaml', '.yml']:
                return yaml.safe_load(file)
            elif file_ext == '.json':
                return json.load(file)
            else:
                error_msg = f"不支持的配置文件格式: {file_ext}"
                logging.error(error_msg)
                raise ValueError(error_msg)
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            error_msg = f"配置文件格式错误: {e}"
            logging.error(error_msg)
            raise ValueError(error_msg)

def get_config_path(config_path):
    """获取当前工作目录"""
    # 获取当前工作目录
    current_dir = os.getcwd()
    # 拼接配置文件的路径
    config_path = os.path.join(current_dir, config_path)
    return config_path


if __name__ == '__main__':
    config = get_config_path("config.yaml")