# Upload2IPFS

<details open>
<summary><strong>English Version</strong></summary>

A simple tool to easily upload files to the IPFS network.

You can use the tool by visiting [this link](https://ipfs.qzz.io/).

The **Download Gateways** are re-checked weekly; the working ones are written to `online_gateways.txt` and the page. I would be grateful if you could provide any available gateways.

## Project Structure

* **index.html**: The main page file, containing the front-end interface for upload and download functions.
* **gateways.js**: Contains the `downloadGateways` variable for storing available IPFS gateways.
* **gateways.txt**: Stores the addresses of available IPFS gateways.
* **LICENSE**: The project's license agreement.
* **README.md**: The project's introduction and usage instructions.
* **reports/**: Directory for storing gateway detection result CSV files.
* **.github/workflows/**: Contains GitHub Actions workflow files.

## Features

* **Upload Files**: Users can upload files to the IPFS network.
* **Download Files**: Download files from the IPFS network using a known IPFS hash.
* **Gateway Management**: Weekly discovers gateways from the public gateway list, verifies each one actually serves a known test file, and supports user submissions of new gateways.
* **Switch Download Gateway**: Each upload result can switch to another download gateway, or find one that already serves the file automatically.

## How to Use

### Upload

1. Open [Upload2IPFS](https://ipfs.qzz.io/). On the first visit, read the terms and click **Accept**.
2. *(Optional)* Click **Check & filter upload gateways**. Gateways that fail are removed from the upload list and the rest are sorted by speed. The result is remembered in your browser.
3. Pick a gateway under **Select a gateway to upload your files**.
4. Click **Choose Files** (hold <kbd>Ctrl</kbd> to select several), then **Upload**. Use **Cancel Upload** to stop.

### Results

Each uploaded file gets one row with its CID, file name and size:

* Click the link to open or download the file.
* **Copy URL** copies that file's link; **Copy All URLs** copies every link, one per line.
* The dropdown in the row shows which download gateway the link uses.

### If a link does not open

A freshly uploaded file is not on every gateway right away. Switching gateway usually fixes it:

1. Click **Find working** in that row. All download gateways are tried at once; each option is marked `✓ time` or `✗`, and the row switches to the fastest gateway that returns your file. The link and Copy URL update with it.
2. Or pick another gateway in the row's dropdown yourself.
3. Changing **Select a gateway to view your uploaded files** at the top switches all rows at once.
4. If it shows **None yet, retry later**, the file has not spread yet. Wait a minute and try again.

**Check & filter download gateways** tests every download gateway with a known file, keeps only the working ones and sorts them by speed.

### Notes

* **Everything you upload is public.** Anyone with the CID can download it, and it cannot be deleted. Do not upload sensitive files.
* Free public gateways do not promise to keep files forever. For important files, pin them on your own IPFS node or a pinning service.
* The official gateways `ipfs.io` and `dweb.link` were retired in September 2026, so they are not in the list.

## Providing Gateways

If you have an available IPFS gateway, please provide it to us so we can update the `gateways.txt` file.

## Contributing

Contributions are welcome, whether it's code or providing available IPFS gateways. Please submit a PR or provide your suggestions in an Issue.

</details>

<details>
<summary><strong>中文版本 (Chinese Version)</strong></summary>

一个简单的工具，用于将文件轻松上传到IPFS网络。

您可以访问[此链接](https://ipfs.qzz.io/)使用该工具。

**下载网关**每周自动重新检测，可用的会写入 `online_gateways.txt` 和页面。如果您能提供可用的网关，我将非常感激。

## 项目结构

* **index.html**: 主页面文件，包含上传和下载功能的前端界面。
* **gateways.js**: 包含`downloadGateways`变量，用于存储可用的IPFS网关。
* **gateways.txt**: 存储可用的IPFS网关地址。
* **LICENSE**: 项目的许可协议。
* **README.md**: 项目的介绍和使用说明。
* **reports/**: 存放网关探测结果的CSV文件。
* **.github/workflows/**: 包含GitHub Actions工作流文件。

## 功能特点

* **上传文件**: 用户可以上传文件到IPFS网络。
* **下载文件**: 通过已知的IPFS哈希值，从IPFS网络下载文件。
* **网关管理**: 每周从公共网关列表发现新网关，并用已知测试文件逐个确认真的能下载，也支持用户提交新的网关。
* **切换下载网关**: 每条上传结果都可以换一个下载网关，或自动找一个已经能下载该文件的网关。

## 使用方法

### 上传

1. 打开 [Upload2IPFS](https://ipfs.qzz.io/)。第一次访问时会弹出使用条款，阅读后点 **Accept**。
2. （可选）点 **Check & filter upload gateways**，测不通的上传网关会从列表中去掉，剩下的按速度排序。结果会保存在浏览器里。
3. 在 **Select a gateway to upload your files** 里选一个上传网关。
4. 点 **Choose Files** 选择文件（按住 <kbd>Ctrl</kbd> 可多选），再点 **Upload**。上传途中可以点 **Cancel Upload** 取消。

### 上传结果

每个文件一行，显示 CID、文件名和大小：

* 点链接即可打开或下载。
* **Copy URL** 复制这个文件的链接；**Copy All URLs** 复制全部链接，一行一个。
* 这一行的下拉框显示链接当前用的是哪个下载网关。

### 链接打不开怎么办

刚上传的文件不会立刻出现在所有网关上，换一个网关通常就能下载：

1. 点这一行的 **Find working**。页面会同时尝试所有下载网关，每个选项标上 `✓ 耗时` 或 `✗`，并自动切到最快能拿到你这个文件的网关，链接和 Copy URL 随之更新。
2. 也可以在这一行的下拉框里自己换一个网关。
3. 改页面上方的 **Select a gateway to view your uploaded files**，所有结果会一起切换。
4. 如果显示 **None yet, retry later**，说明文件还没传开，等一两分钟再试。

**Check & filter download gateways** 会用一个已知文件测试所有下载网关，只保留能用的，并按速度排序。

### 注意事项

* **上传的内容是公开的**：任何拿到 CID 的人都能下载，而且无法删除。请不要上传敏感文件。
* 免费的公共网关不保证永久保存文件。重要文件请在自己的 IPFS 节点或 pinning 服务上固定（pin）。
* 官方网关 `ipfs.io`、`dweb.link` 已于 2026 年 9 月退役，所以不在列表里。

## 提供网关

如果您有可用的IPFS网关，请提供给我们，以便我们更新`gateways.txt`文件。

## 贡献

欢迎贡献代码或提供可用的IPFS网关。请提交PR或在Issue中提供您的建议。

</details>
