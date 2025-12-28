# 使用说明

## 快速开始

### 1. 安装依赖

#### 方式一：使用虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 方式二：全局安装

```bash
pip install -r requirements.txt
```

### 2. 运行程序

#### 快速演示（使用预定义数据）

```bash
python run_quick_demo.py
```

这将使用8个预定义的不等式生成示例文档，不需要网络连接。

#### 完整版本（爬取所有36个不等式）

```bash
python main.py
```

这将：
1. 从多个数据源爬取36种不等式的数据
2. 解析并存储数据到 `data/inequalities.json`
3. 生成HTML和Markdown文档到 `data/output/` 目录

**注意**：完整运行可能需要较长时间（约10-30分钟），取决于网络状况。

### 3. 查看结果

生成的文档位于 `data/output/` 目录：

- `inequality_summary.html` - 网页版，可在浏览器中打开
- `inequality_summary.md` - Markdown版，可用任何文本编辑器查看
- `inequality_summary.pdf` - PDF版（需要安装weasyprint）

数据文件：
- `data/inequalities.json` - 结构化的不等式数据

## 配置选项

编辑 `config.py` 可以修改：

### 爬取设置

```python
CRAWL_DELAY = 2  # 请求间隔（秒），避免过快请求
REQUEST_TIMEOUT = 30  # 请求超时时间
```

### 自定义不等式列表

```python
INEQUALITY_NAMES = [
    "基本不等式",
    "柯西不等式",
    # 添加或删除不等式...
]
```

### 数据源

```python
SEARCH_SOURCES = {
    'wikipedia_zh': 'https://zh.wikipedia.org/wiki/',
    'wikipedia_en': 'https://en.wikipedia.org/wiki/',
    'baidu_baike': 'https://baike.baidu.com/item/',
}
```

## 高级用法

### 1. 增量更新

如果已经运行过一次，再次运行会：
- 保留已有的完整数据
- 只更新不完整或新增的不等式
- 自动合并多次爬取的结果

### 2. 使用多线程

在 `main.py` 中设置：

```python
use_multithreading = True
max_workers = 3  # 并发线程数
```

### 3. 只生成文档（不爬取）

如果已有 `data/inequalities.json`，可以只生成文档：

```python
from src.database import InequalityDatabase
from src.generator import DocumentGenerator
import config

db = InequalityDatabase(config.DATA_FILE)
gen = DocumentGenerator(config.TEMPLATES_DIR, config.OUTPUT_DIR)

inequalities = db.get_all()
gen.generate_html(inequalities)
gen.generate_markdown(inequalities)
```

### 4. 自定义模板

编辑模板文件来自定义输出格式：
- `templates/summary_template.html` - HTML模板
- `templates/summary_template.md` - Markdown模板

模板使用Jinja2语法，可以修改样式、布局和内容。

## 测试

运行单元测试：

```bash
python test_basic.py
```

## 故障排除

### 问题1：模块未找到错误

```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**：安装缺失的依赖

```bash
pip install xxx
# 或重新安装所有依赖
pip install -r requirements.txt
```

### 问题2：爬取失败

```
Failed to fetch https://...
```

**可能原因**：
1. 网络连接问题
2. 网站访问受限
3. 请求频率过高

**解决方案**：
1. 检查网络连接
2. 增加 `CRAWL_DELAY` 的值
3. 使用代理（需修改 `crawler.py`）
4. 使用快速演示模式（不需要网络）

### 问题3：PDF生成失败

```
weasyprint not installed, skipping PDF generation
```

**解决方案**：

```bash
pip install weasyprint
```

注意：weasyprint在某些系统上可能需要额外的系统依赖。

### 问题4：虚拟环境问题

如果遇到虚拟环境相关问题：

```bash
# 删除旧的虚拟环境
rm -rf venv

# 重新创建
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 日志

程序日志保存在 `inequality_summarizer.log` 文件中，包含：
- 详细的运行信息
- 错误和警告
- 爬取进度
- 统计数据

查看日志：

```bash
tail -f inequality_summarizer.log
```

## 性能优化

### 减少爬取时间

1. 减少不等式数量（编辑 `config.py`）
2. 增加并发线程数（在 `main.py` 中）
3. 跳过某些数据源

### 减少文档大小

1. 限制每个不等式的例题数量
2. 修改模板，移除不需要的部分
3. 压缩CSS样式

## 数据格式

### JSON数据结构

```json
{
  "name": "不等式名称",
  "aliases": ["别名1", "别名2"],
  "math_form": "数学形式",
  "conditions": "应用条件",
  "description": "描述",
  "proof_methods": ["证法1", "证法2"],
  "examples": [
    {
      "description": "例题",
      "solution": "解答"
    }
  ],
  "related": ["相关不等式"],
  "applications": ["应用场景"]
}
```

### 完整度评分

- 100%：包含所有字段，至少2个证法和3个例题
- 80-99%：大部分字段完整
- 60-79%：基本信息完整
- <60%：信息不完整

## 贡献数据

如果你有更好的不等式数据：

1. 编辑 `data/inequalities.json`
2. 或在 `src/parser.py` 中添加预定义数据
3. 重新生成文档

## 许可证

MIT License - 可自由使用和修改
