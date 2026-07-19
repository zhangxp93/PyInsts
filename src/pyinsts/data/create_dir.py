import os


def check_and_create_dir(directory_path):
    """
    检测路径下是否有指定文件夹，如果没有就创建

    Args:
        directory_path (str): 要检测和创建的目录路径

    Returns:
        bool: 创建成功返回True，否则返回False
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"目录已创建: {directory_path}")
            return True
        else:
            print(f"目录已存在: {directory_path}")
            return True
    except Exception as e:
        print(f"创建目录时出错: {e}")
        return False
