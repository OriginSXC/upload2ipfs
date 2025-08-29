# Upload2IPFS

Upload files to the IPFS network easily with [this tool](https://upload2ipfs.ipfs.qzz.io/).

The **Download Gateways** would refresh everyday in *gateways.txt*, and I would be happy if you can provide available gateways.

# Upload2IPFS

一个简单的工具，用于将文件轻松上传到IPFS网络。  

您可以访问[此链接](https://upload2ipfs.ipfs.qzz.io/)使用该工具。  

我们每天都会在`gateways.txt`中刷新**下载网关**，如果您能提供可用的网关，我将非常感激。

## 项目结构

- **index.html**: 主页面文件，包含上传和下载功能的前端界面。
- **gateways.js**: 包含`downloadGateways`变量，用于存储可用的IPFS网关。
- **gateways.txt**: 存储可用的IPFS网关地址。
- **LICENSE**: 项目的许可协议。
- **README.md**: 项目的介绍和使用说明。
- **reports/**: 存放网关探测结果的CSV文件。
- **.github/workflows/**: 包含GitHub Actions工作流文件。

## 功能特点

- **上传文件**: 用户可以上传文件到IPFS网络。
- **下载文件**: 通过已知的IPFS哈希值，从IPFS网络下载文件。
- **网关管理**: 每天自动更新可用的IPFS网关，并支持用户提交新的网关。

## 使用方法

1. 访问[Upload2IPFS](https://upload2ipfs.ipfs.qzz.io/)。
2. 上传文件，获取IPFS哈希。
3. 使用IPFS哈希下载文件。

## 提供网关

如果您有可用的IPFS网关，请提供给我们，以便我们更新`gateways.txt`文件。

## 贡献

欢迎贡献代码或提供可用的IPFS网关。请提交PR或在Issue中提供您的建议。
