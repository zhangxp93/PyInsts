# 分支使用说明

点击后续列表的版本号链接，可前往对应备份分支页面。

部分备份分支含有体积较大的二进制库，会让你花费长时间下载。因此，建议只下载你需要用的分支。

方法1：将所需的分支，fork到你自己的账号下，然后clone你自己仓库。

方法2：使用以下命令手动clone指定分支：

```
git clone --single-branch --branch [分支名] https://github.com/zhangxp93/PyInst.git
```

方法3：在本仓库手动下载指定分支的zip源码包。

`[分支名]` 可以是 `main` 、`release/1.0.0` 等，详见下方列表。

`main`、`dev` 等分支，可能含有开发中的不稳定的新功能。如果用于研究学习或二次开发，建议选择 `release` 开头的分支。

# 更新日志 CHANGE LOG

### [release/v0.1.0](https://github.com/zhangxp93/PyInst.git) `2026.08.02`
- `BaseInstrument` 新增 Context Manager（`with` 语句自动关闭连接）
- 完善 `pyproject.toml` 构建配置，移除无效 workspace 成员与未使用的 `colorlog` 依赖
- 统一 `write(..., check_complete=True)` 调用风格，修复 `KeysightN9030B.close()` 递归调用 bug
- 导出 `Rsa6000`、`Rsa6000Sp`、`Sna6034a`、`Zna43`、`Ts760Set` 驱动
- `pyinsts` 包根命名空间导出 `__version__`
- 新增基于 `@sim` 仿真后端的 pytest 单元测试
- 修正 `set_opc_timeout` 默认值与 `wait_opc` 临时超时逻辑

### [release/v0.0.9](https://github.com/zhangxp93/PyInst.git) `2026.08.02`
- 修复所有驱动及数据模块中遗留的 `src.` 包导入路径错误（包含 `serial_interface.py`, `keysight_e36312a.py`, `sna6034a.py`, `zna.py` 等）
- 移除冗余文件 `openhtf_reporter.py`

### [release/v0.0.8](https://github.com/zhangxp93/PyInst.git) `2026.08.02`
- 修改readme config.yaml地址格式错误

### [release/v0.0.7](https://github.com/zhangxp93/PyInst.git) `2026.08.01`
- 修改引用错误

### [release/v0.0.4](https://github.com/zhangxp93/PyInst.git) `2026.03.08`
- **核心架构重构与解耦**：
  - 拆分底层设计为 `instrument`（单数，存放通信 Adapter 与生命周期基类）和 `instrument_drivers`（复数，存放具体的仪器驱动）。
  - 仪器厂家分类目录以及文件名统一规范为全小写，避免跨系统大小写敏感导致的导入失败问题。
  - 类名命名规范化为“厂家统一缩写前缀 + 型号驼峰”（如 `KeysightN9020b`、`RsFswp`），解决命名不统一的问题。
- **百分之百向下兼容**：
  - 在各个驱动文件底部以及包入口定义并保留了极简的无厂家前缀别名（如 `N9020b = KeysightN9020b`），保证已有使用旧版类的老代码可以直接运行。
- **打包与版本管理重构**：
  - 项目集成 `versioningit` 动态版本管理器，支持在发布包时根据 Git Tag 自动决定发布版本。
  - 修正 `_version.py` 的文件布局，将其移入 `pyinsts` 内部包中，添加了读取失败时的安全降级机制（Fallback），避免了在开发环境下直接运行 Demo 时因缺少 Git Tag 而崩溃的问题。
- **包依赖管理补充**：
  - 在项目根目录添加了 `requirements.txt` 依赖配置文件，方便常规 `pip` 用户安装开发与运行环境。

### [release/v0.0.3.3](https://github.com/zhangxp93/PyInst.git) `2026.03.08`
- 更新 Keysight N9020B 仪器驱动，修复了直接导入路径依赖的问题（移除了冗余的 `src.` 前缀）

### [release/v0.0.3.2](https://github.com/zhangxp93/PyInst.git) `2026.03.08`
- 重构模块内部导入路径，移除了冗余的 `src.` 前缀，改为从顶层模块 `pyinsts` 直接导入（如 `main.py` 与 `baseinstrument.py`）
- 更新项目包管理器配置锁文件 `uv.lock` 从而使得版本及包名依赖彻底保持一致

### [release/v0.0.3.1](https://github.com/zhangxp93/PyInst.git) `2026.03.08`
- 修复 PyPI 上 README 中无效的文档相对跳转链接，将其替换为 GitHub 上的绝对链接
- 在 pyproject.toml 文件中增加了 `[project.urls]` 以便在 PyPI 侧边栏展示项目主页和更新日志

### [release/v0.0.3](https://github.com/zhangxp93/PyInst.git) `2026.03.08`
- 新增 `PyInst Instrument Control` Agent Skill 以支持 AI 模型通过自然语言或者流程自动化控制仪器
- 修复 `libs/keysight/N9020B.py` 文件中由于绝对导入导致的循环导入报错问题
- 在 `libs/keysight/N9020B.py` 中动态追加系统路径 `sys.path` 以解决直接运行脚本时的依赖包找不到的问题
- 更新项目依赖管理，使用 `uv` 替换 `Poetry`
- 引入 uv workspaces 配置以支持多个项目成员（如 `test_app`）
- 清理冗余的 `poetry.lock` 和 `poetry.toml` 配置文件

### [release/v0.0.2](https://github.com/zhangxp93/PyInst.git) `2025.12.13`
- 重构项目架构，引入基类仪器控制模块
- 优化Keysight N9020B频谱仪控制类
- 完善Rohde & Schwarz频谱仪控制类
- 添加配置文件加载功能
- 改进日志系统，支持彩色日志输出
- 修复多个仪器控制相关bug
- 更新项目依赖管理，使用Poetry管理依赖

### [release/v0.0.1](https://github.com/zhangxp93/PyInst.git) `2025.09.14`
- 项目第一个版本发布
- 支持基于 PyVISA 的仪器控制
- 实现对 Keysight 和 Rohde & Schwarz 仪器的 SCPI 命令控制
- 支持多种连接方式（USB、GPIB、TCP/IP）

### [main](https://github.com/zhangxp93/PyInst.git) `2024.11.24`
- "梦开始的地方"