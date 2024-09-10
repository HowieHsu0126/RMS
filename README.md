# Paper Fetcher Project


>  Haowei Xu
>
> Email: haoweixu0126@163.com


## 项目简介

**Paper Fetcher Project** 是一个用于从多个学术资源（例如 ArXiv、Google Scholar 和 PubMed）抓取论文的 Python 项目。该项目提供了模块化的设计，方便扩展和定制不同的学术数据源，并支持定时抓取和去重功能。

## 功能特点

- **支持多源抓取**：从 ArXiv、Google Scholar 和 PubMed 抓取论文。
- **去重机制**：自动跳过已下载的论文，避免重复抓取。
- **定时任务**：支持定时自动抓取最新的论文。
- **可扩展性**：使用面向对象设计，便于扩展其他学术数据源。

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
git clone https://gitee.com/Howie0126/paper-crawler.git
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

## 项目贡献

欢迎任何形式的贡献！请确保在贡献代码前遵循以下指南：

1. **Fork 本仓库**，创建您的 feature 分支。
2. **编写清晰、可读的代码**，确保符合 PEP8 代码风格。
3. **编写测试**：所有新功能或改动都应包含适当的测试。
4. 提交 Pull Request。

### 开发环境设置

1. 克隆仓库：

   ```bash
   git clone https://gitee.com/Howie0126/paper-crawler.git
   cd paper_fetcher_project
   ```
2. 安装开发依赖：

   ```bash
   pip install -r requirements.txt
   ```

## 日志和调试

项目使用 Python 内置的 `logging` 模块进行日志记录。默认日志输出到控制台。可以通过修改 `paper_fetcher/utils.py` 文件来配置日志级别。

## 许可证

[MIT License](https://opensource.org/licenses/MIT)
