# 📐 数学不等式自动汇总系统

一个完整的Python项目，用于自动爬取36种常见数学不等式的定义、证明方法和典型例题，并生成结构化的可打印文档。

## ✨ 功能特点

- 🕷️ **智能爬虫**: 从Wikipedia、百度百科等权威数学资源爬取数据
- 📊 **结构化存储**: 使用JSON格式存储所有不等式数据
- 📝 **多格式输出**: 生成HTML、Markdown和PDF文档
- 🎨 **美观排版**: 支持MathJax数学公式渲染，适合打印和在线浏览
- 🔄 **增量更新**: 支持数据的增量更新和去重
- 📈 **完整度评分**: 自动评估每个不等式的数据完整程度

## 📋 不等式列表

项目收录以下36种常见数学不等式：

### 基本均值不等式
1. 基本不等式
2. 重要不等式
3. 糖水不等式
4. 常用不等式
5. 二元均值不等式
6. 二元均值不等式（衍生）
7. 三元均值不等式
8. n元均值不等式

### 函数不等式
9. 绝对值三角不等式
10. 指数不等式
11. 指数不等式链
12. 对数不等式
13. 对数不等式链1-3
14. 三角函数不等式

### 经典不等式
15. 柯西不等式
16. 琴生不等式
17. 伯努利不等式
18. 切比雪夫不等式

### 高级不等式
19. Aczel不等式
20. 权方和不等式
21. 权方差不等式
22. 幂平均不等式
23. 排序不等式
24. 卡尔森不等式
25. 闵可夫斯基不等式
26. 舒尔不等式
27. 穆尔海德不等式
28. 赫尔德不等式
29. 杨氏不等式
30. 嵌入不等式
31. 波波维奇亚不等式
32. 卡拉马特不等式
33. 米尔黑德不等式
34. 麦克劳林不等式
35. 范数不等式
36. Fan Ky不等式

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

程序将自动完成以下步骤：
1. 爬取36种不等式的数据
2. 解析并结构化存储数据
3. 生成HTML和Markdown文档
4. （可选）生成PDF文档

## 📁 项目结构

```
inequality-summarizer/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖
├── config.py                    # 配置文件
├── main.py                      # 主程序入口
├── src/                         # 源代码目录
│   ├── __init__.py
│   ├── crawler.py              # 爬虫模块
│   ├── parser.py               # 数据解析模块
│   ├── models.py               # 数据模型定义
│   ├── database.py             # 数据存储模块
│   └── generator.py            # 文档生成模块
├── data/                        # 数据目录
│   ├── inequalities.json       # 不等式数据（自动生成）
│   └── output/                 # 输出文档目录
│       ├── inequality_summary.html
│       ├── inequality_summary.md
│       └── inequality_summary.pdf
└── templates/                   # 文档模板
    ├── summary_template.html
    └── summary_template.md
```

## 📊 数据模型

每个不等式包含以下信息：

```python
{
  "name": "不等式名称",
  "aliases": ["别名1", "别名2"],
  "math_form": "数学形式",
  "conditions": "应用条件",
  "description": "简要描述",
  "proof_methods": ["证法1", "证法2", "证法3"],
  "examples": [
    {
      "description": "例题描述",
      "solution": "解答过程"
    }
  ],
  "related": ["相关不等式"],
  "applications": ["应用场景"]
}
```

## 🎯 输出文档

### HTML文档
- 响应式设计，支持移动端浏览
- 集成MathJax，完美渲染数学公式
- 包含分类目录，便于导航
- 支持打印和导出

### Markdown文档
- 标准Markdown格式
- 便于编辑和二次加工
- 支持Git版本控制

### PDF文档（可选）
- 高质量排版
- 适合打印和分发
- 需要安装weasyprint

## ⚙️ 配置说明

在 `config.py` 中可以配置：

- `CRAWL_DELAY`: 爬取延迟（秒）
- `REQUEST_TIMEOUT`: 请求超时时间
- `INEQUALITY_NAMES`: 要爬取的不等式列表
- `SEARCH_SOURCES`: 数据来源网站

## 🔍 特性说明

### 智能爬虫
- 使用User-Agent轮换避免被封
- 支持多数据源（Wikipedia中英文、百度百科）
- 自动处理网络异常和重试
- 可配置爬取延迟

### 数据解析
- 正则表达式提取数学公式
- 智能识别证明方法和例题
- 支持LaTeX公式解析
- 自动分类和标签化

### 文档生成
- Jinja2模板引擎
- 响应式HTML设计
- MathJax数学渲染
- 自动生成目录和索引

## 📈 数据完整度

程序会自动评估每个不等式的完整度：

- ✅ **完整**: 包含名称、数学形式、至少1个证法和1个例题
- ⚠️ **部分完整**: 缺少部分内容
- ❌ **不完整**: 仅有基本信息

完整度评分标准：
- 名称: 10%
- 数学形式: 20%
- 描述: 10%
- 条件: 10%
- 证法: 最多30% (每个15%)
- 例题: 最多20% (每个10%)

## 🛠️ 技术栈

- **爬虫**: requests, BeautifulSoup4, Selenium
- **数据处理**: json, re, pandas
- **模板引擎**: Jinja2
- **文档生成**: markdown, weasyprint
- **其他**: fake-useragent, logging

## 📝 日志

程序运行日志保存在 `inequality_summarizer.log` 文件中，包含：
- 爬取进度
- 数据处理状态
- 错误和警告信息
- 统计数据

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

数学不等式自动汇总系统

## 🙏 致谢

感谢以下数学资源网站：
- Wikipedia (中文/英文)
- 百度百科
- MathWorld
- ProofWiki

---

**注意**: 本项目仅用于教育和学习目的，爬取数据时请遵守网站的robots.txt和服务条款。
