def _get_version() -> str:
    # 延迟导入，避免不必要的依赖加载
    from importlib.resources import files
    from pathlib import Path
    import versioningit

    try:
        module_path = files("pyinsts")
        if isinstance(module_path, Path):
            # 开发状态：从 git 仓库动态获取
            return versioningit.get_version(project_dir=Path(module_path).parent.parent)
    except Exception:
        pass

    # 降级方案：若读取失败（例如未打 tag 或不在 git 环境中），直接返回备用版本
    return "0.0.8"

# 构建发布包时，这行 __version__ 会被 versioningit 自动改写为真正的发布版本（如 "0.0.4"）
__version__ = "0.0.8"
