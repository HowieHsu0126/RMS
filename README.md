# Paper Fetcher Project

> Haowei Xu
>
> Email: haoweixu0126@163.com



> ⚠️ 提示：在中国大陆运行该项目时，某些学术资源（如 Google Scholar）可能需要通过 VPN 才能正常访问。请确保您已配置 VPN 以避免网络访问限制。


## 项目简介

**Paper Fetcher Project** 是一个 Python 项目，旨在从多个学术资源（例如 ArXiv、Google Scholar 和 PubMed）抓取学术论文，并提供灵活的定制选项。该项目支持定时抓取、去重机制，并可扩展至更多学术数据库。它可以作为科研工作者自动化收集学术资源的工具。

## 功能特点

* **多源数据抓取** ：
  * 支持从  **ArXiv** 、**Google Scholar** 和 **PubMed** 三个常见学术资源抓取论文数据。
  * 每个资源的抓取器模块化设计，支持通过继承 `AbstractPaperFetcher` 类，轻松添加新的学术数据库。
* **组合条件抓取** ：
  * 项目支持根据 **组合条件** 来进行精准的论文抓取，用户可以提供  **关键词** 、 **作者** 、 **年份** 、**期刊** 等多个条件进行组合查询。例如，您可以同时指定论文的关键词为 "cancer"，期刊为 "Nature"，年份为 "2020"，这样抓取器会根据这些条件抓取符合要求的论文。
  * 组合查询的条件可以灵活定制，未提供的条件将被忽略。例如，如果您只指定关键词而不指定作者，系统会根据关键词抓取所有相关的论文。
* **去重机制** ：
  * 自动检查抓取到的论文是否已经下载，基于唯一标识符（如 DOI 或 URL）实现去重，避免重复抓取同一论文。
  * 已抓取的论文 ID 会保存在 JSON 文件中，作为后续去重参考。
* **随机延迟防爬虫机制** ：
  * 抓取过程中引入了  **随机延迟** ，防止过于频繁的请求触发目标网站的反爬机制。每次抓取的延迟时间在用户定义的最小和最大延迟之间随机分配。
* **JSON 格式数据保存** ：
  * 抓取到的论文信息将以 JSON 格式保存，便于后续使用或分析。
  * 每次抓取后，新的数据会自动追加到现有的 JSON 文件中。
* **定时任务支持** ：
  * 内置定时调度功能，支持每隔固定时间间隔（如每 30 分钟）自动抓取最新的论文。
  * 还可以指定每日固定时间（如每天早上 6:00）抓取最新的论文。
* **易扩展性** ：
  * 使用面向对象的设计模式，允许用户通过继承并实现必要的方法来自定义新的数据源。
  * 各抓取模块如 `ArXivFetcher`, `GoogleScholarFetcher`, `PubMedFetcher` 都遵循统一的接口，便于扩展与维护。
* **日志记录** ：
  * 使用 Python 的 `logging` 模块进行日志记录，默认输出到控制台，帮助用户追踪抓取过程中的状态和错误。
  * 可以自定义日志级别，如 `INFO`、`DEBUG`、`ERROR` 等，以满足不同场景下的需求。

## 目录结构

```plaintext
paper_fetcher_project/
│
├── paper_fetcher/               # 核心功能模块
│   ├── __init__.py              # 初始化模块
│   ├── abstract_fetcher.py      # 抽象类及其基础方法
│   ├── arxiv_fetcher.py         # ArXiv 抓取器
│   ├── google_scholar_fetcher.py# Google Scholar 抓取器
│   ├── pubmed_fetcher.py        # PubMed 抓取器
│   └── utils.py                 # 通用工具函数 (如日志配置、去重等)
│
├── tests/                       # 单元测试
│   ├── test_arxiv_fetcher.py    # ArXiv 抓取器测试
│   ├── test_google_scholar_fetcher.py # Google Scholar 抓取器测试
│   ├── test_pubmed_fetcher.py   # PubMed 抓取器测试
│
├── requirements.txt             # 项目依赖
└── main.py                      # 运行脚本
```

## 安装指南

### 先决条件

确保您已安装以下内容：

- Python 3.7 或更高版本
- `pip`：Python 包管理工具

### 克隆仓库

首先，克隆此项目到本地：

```bash
git clone https://github.com/HowieHsu0126/RMS.git
cd paper_fetcher_project
```

### 安装依赖项

运行以下命令安装所需的 Python 包：

```bash
pip install -r requirements.txt
```

## 使用说明

### 运行示例

项目提供了多种抓取方式。以下是抓取 PubMed 论文的示例：

```bash
python main.py
```

`main.py` 文件中包含了具体的抓取配置，例如抓取的关键词、作者和年份。

### 定制抓取参数

可以通过修改 `main.py` 中的 `search_params` 来定制抓取参数。例如，抓取指定期刊和年份的论文：

```python
search_params_pm = {
    "keyword": "cancer",
    "author": "",
    "journal": "Nature",
    "year": "2020"
}
```

### 添加新的数据源

要添加新的数据源，只需继承 `AbstractPaperFetcher` 类并实现 `fetch_papers` 方法即可。

### 定时抓取任务

项目支持定时任务调度。您可以使用以下代码设置每隔 30 分钟抓取一次论文：

```python
pm_fetcher.schedule_task(search_params_pm, interval_minutes=30, max_results=5)
```

## 测试

该项目包含单元测试文件，使用 `pytest` 进行测试。

### 运行测试

安装 `pytest` 依赖：

```bash
pip install pytest
```

运行所有测试：

```bash
pytest tests/
```

## 日志和调试

项目使用 Python 内置的 `logging` 模块进行日志记录。默认日志输出到控制台。可以通过修改 `paper_fetcher/utils.py` 文件来配置日志级别。

## 项目贡献

欢迎任何形式的贡献！请确保在贡献代码前遵循以下指南：

1. **Fork 本仓库**，创建您的 feature 分支。
2. **编写清晰、可读的代码**，确保符合 PEP8 代码风格。
3. **编写测试**：所有新功能或改动都应包含适当的测试。
4. 提交 Pull Request。

## 许可证

[MIT License](https://opensource.org/licenses/MIT)
