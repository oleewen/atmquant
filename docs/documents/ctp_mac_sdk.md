# Mac CTP SDK 更新说明

## 问题背景

C++ 封装代码（vnctp）针对较新版本的 CTP SDK 编写，包含更多结构体字段、函数参数和新类型；而 Mac 版 SDK（`vnpy_ctp/api/` 下 `.framework` 或 `include/mac/ctp`）可能是较旧或精简版，缺少这些定义，导致在 macOS 上编译报错（如 `CThostFtdcInvestorInfoCommRecField`、`CThostFtdcCombLegField` 等未知类型）。

## 方案一：更新 Mac CTP SDK 头文件（推荐先做）

将 Mac 使用的头文件更新为与 [vnpy/vnpy_ctp](https://github.com/vnpy/vnpy_ctp) 官方一致的 `include/mac/ctp` 版本，并保持与现有 `.framework` 内 Headers 一致。

### 操作步骤

在项目根目录执行：

```bash
./scripts/update_mac_ctp_sdk.sh
```

脚本会：

1. 从 `vnpy/vnpy_ctp` 的 `main` 分支拉取以下 4 个头文件到 `vnpy_ctp/api/include/mac/ctp/`：
   - `ThostFtdcMdApi.h`
   - `ThostFtdcTraderApi.h`
   - `ThostFtdcUserApiDataType.h`
   - `ThostFtdcUserApiStruct.h`
2. 将上述头文件复制到：
   - `vnpy_ctp/api/thosttraderapi_se.framework/Versions/A/Headers/`
   - `vnpy_ctp/api/thostmduserapi_se.framework/Versions/A/Headers/`

依赖：需要可访问 `raw.githubusercontent.com`（若网络不稳定可多试几次或配置代理）。

### 若仍缺类型（如 6.6.9/6.7.x 新增结构体）

官方 Mac 头文件若仍比 Linux/Windows 少类型，可二选一：

- **从 OpenCTP 使用 Linux 头文件补全**：  
  [openctp/openctp](https://github.com/openctp/openctp) 的 `ctpapi-python/CTPAPI/linux/` 下有完整头文件。可将其中 `ThostFtdcUserApiStruct.h`、`ThostFtdcUserApiDataType.h` 等与 Mac 版对比，把缺失的结构体定义合并进 `include/mac/ctp/` 及上述两个 `Headers` 目录（注意仅补类型定义，不替换 Mac 库的二进制）。
- **或采用方案二**：在 vnctp 中对缺失类型/接口做 `#ifdef __APPLE__` 条件编译，在 Mac 上跳过或用占位实现。

## 获取 vnctp 源码（本地编译或打补丁时）

vnctp 源码在 vnpy_ctp 官方仓库的 `vnpy_ctp/api/vnctp/`。若需本地编译或对缺失类型做 `__APPLE__` 条件编译，可克隆后复制到本项目：

```bash
git clone --depth 1 https://github.com/vnpy/vnpy_ctp.git /tmp/vnpy_ctp
cp -R /tmp/vnpy_ctp/vnpy_ctp/api/vnctp /path/to/atmquant/vnpy_ctp/api/
```

本项目已提供 `vnpy_ctp/api/vnctp/vnctp.h`，完整 vnctpmd/vnctptd 需从上述仓库复制。

## 方案二：在 vnctp 中按 Mac 条件编译

若无法通过更新头文件补齐（例如 Mac 官方库 ABI 与新版头文件不兼容），则需修改 vnctp 源码，对仅在 Linux/Windows 新 SDK 中存在的成员或类型做条件编译：

- 在引用到缺失类型或新字段的代码处使用 `#ifndef __APPLE__` / `#ifdef __APPLE__`，在 Mac 上编译时排除或提供替代实现。
- 先按上一节获取完整 `vnpy_ctp/api/vnctp/`，再在 vnctp 中为缺失类型/接口添加 `__APPLE__` 条件编译。

## 方案三：使用与当前 Mac SDK 匹配的旧版 vnpy_ctp

若本机 Mac CTP SDK 版本较旧且无法更新，可选用与该 SDK 版本匹配的 vnpy_ctp 发行版（见 [vnpy_ctp Releases](https://github.com/vnpy/vnpy_ctp/releases)），以降低头文件与库的版本差。

## 参考链接

- [vnpy/vnpy_ctp](https://github.com/vnpy/vnpy_ctp) — 官方 CTP 接口与 include/mac/ctp、vnctp 源码
- [openctp 下载页](http://openctp.cn/download.html) — CTP 各版本接口包（多为 Linux/Windows）
- [VeighNa 社区：Mac 编译 vnpy_ctp](https://www.vnpy.com/forum/topic/34312-mac-bian-yi-an-zhuang-vnpy-ctpshi-bai) — 常见 Mac 编译问题
