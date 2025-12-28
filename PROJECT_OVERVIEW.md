# 项目概览

## 📊 项目统计

- **总文件数**: 19个Python/配置/文档文件
- **核心模块**: 6个Python模块
- **模板文件**: 2个（HTML + Markdown）
- **文档文件**: 3个（README + USAGE + 本文件）
- **代码行数**: ~2000+ 行

## 🏗️ 项目架构

```
inequality-summarizer/
│
├── 📝 文档和配置
│   ├── README.md              - 项目介绍和功能说明
│   ├── USAGE.md               - 详细使用说明
│   ├── PROJECT_OVERVIEW.md    - 项目架构概览（本文件）
│   ├── requirements.txt       - Python依赖列表
│   ├── config.py              - 全局配置文件
│   └── .gitignore             - Git忽略规则
│
├── 🎯 主程序
│   ├── main.py                - 主程序入口（完整版，含爬虫）
│   ├── run_quick_demo.py      - 快速演示（仅用预定义数据）
│   └── test_basic.py          - 单元测试
│
├── 📦 核心模块 (src/)
│   ├── __init__.py            - 包初始化
│   ├── models.py              - 数据模型定义
│   │   ├── Example类         - 例题模型
│   │   └── Inequality类      - 不等式模型
│   │
│   ├── crawler.py             - 网络爬虫模块
│   │   └── InequalityCrawler - 爬取百度百科、维基百科
│   │
│   ├── parser.py              - 数据解析模块
│   │   ├── InequalityParser  - 解析爬取的数据
│   │   └── 预定义数据        - 8个完整不等式数据
│   │
│   ├── database.py            - 数据存储模块
│   │   └── InequalityDatabase - JSON数据库操作
│   │
│   └── generator.py           - 文档生成模块
│       └── DocumentGenerator  - 生成HTML/MD/PDF
│
├── 🎨 模板文件 (templates/)
│   ├── summary_template.html  - HTML文档模板（含CSS样式）
│   └── summary_template.md    - Markdown文档模板
│
└── 💾 数据输出 (data/)
    ├── inequalities.json      - 不等式数据存储（自动生成）
    └── output/                - 输出文档目录
        ├── inequality_summary.html
        ├── inequality_summary.md
        └── inequality_summary.pdf (可选)
```

## 🔄 数据流程

```
1. 输入阶段
   ├─ config.py 中定义36个不等式名称
   └─ 可选：提供英文名称以爬取英文维基百科

2. 爬取阶段 (crawler.py)
   ├─ 百度百科爬取
   ├─ 中文维基百科爬取
   └─ 英文维基百科爬取（如有英文名）

3. 解析阶段 (parser.py)
   ├─ 提取数学公式
   ├─ 识别证明方法
   ├─ 提取例题
   └─ 补充预定义数据

4. 存储阶段 (database.py)
   ├─ 合并新旧数据
   ├─ 去重和更新
   └─ 保存到JSON文件

5. 生成阶段 (generator.py)
   ├─ 分类整理
   ├─ 应用Jinja2模板
   ├─ 生成HTML文档
   ├─ 生成Markdown文档
   └─ 生成PDF文档（可选）

6. 输出阶段
   └─ data/output/ 目录中的最终文档
```

## 🎯 核心功能详解

### 1. 数据模型 (models.py)

#### Inequality 类
- **属性**：
  - name: 不等式名称
  - aliases: 别名列表
  - math_form: 数学形式
  - conditions: 应用条件
  - description: 描述
  - proof_methods: 证明方法列表
  - examples: 例题列表
  - related: 相关不等式
  - applications: 应用场景

- **方法**：
  - to_dict(): 转为字典
  - from_dict(): 从字典创建
  - is_complete(): 判断是否完整
  - completeness_score(): 计算完整度（0-1）

#### Example 类
- description: 例题描述
- solution: 解答过程

### 2. 爬虫模块 (crawler.py)

#### InequalityCrawler 类
- **功能**：
  - 自动轮换User-Agent
  - 请求延迟控制
  - 多数据源支持
  - 异常处理和重试

- **方法**：
  - crawl_baidu_baike(): 爬取百度百科
  - crawl_wikipedia_zh(): 爬取中文维基
  - crawl_wikipedia_en(): 爬取英文维基
  - crawl_inequality(): 统一爬取接口

### 3. 解析模块 (parser.py)

#### InequalityParser 类
- **功能**：
  - 正则表达式提取数学公式
  - 智能识别证明章节
  - 自动提取例题
  - 预定义数据补充

- **预定义数据**：
  包含8个完整不等式：
  1. 基本不等式
  2. 柯西不等式
  3. 三角不等式
  4. 琴生不等式
  5. 伯努利不等式
  6. 切比雪夫不等式
  7. 赫尔德不等式
  8. 闵可夫斯基不等式

### 4. 数据库模块 (database.py)

#### InequalityDatabase 类
- **功能**：
  - JSON格式存储
  - 增量更新
  - 智能合并
  - 数据去重
  - 统计分析

- **方法**：
  - load(): 加载数据
  - save(): 保存数据
  - add_or_update(): 添加/更新
  - get(): 查询单个
  - get_all(): 获取全部
  - get_complete_inequalities(): 获取完整的
  - get_statistics(): 统计信息

### 5. 文档生成器 (generator.py)

#### DocumentGenerator 类
- **功能**：
  - Jinja2模板渲染
  - 自动分类整理
  - MathJax数学渲染
  - 响应式HTML设计
  - PDF导出（可选）

- **分类规则**：
  - 基本均值不等式
  - 经典不等式
  - 函数不等式
  - 高级不等式
  - 其他不等式

## 🎨 文档模板特性

### HTML模板
- **设计特点**：
  - 响应式布局（支持移动端）
  - 美观的配色方案
  - 清晰的层次结构
  - 打印友好
  - MathJax数学公式渲染

- **功能模块**：
  - 页面标题和元信息
  - 可展开的目录
  - 分类导航
  - 完整度百分比显示
  - 标签和关联不等式
  - 响应式CSS

### Markdown模板
- **特点**：
  - 标准Markdown语法
  - GitHub风格
  - 目录结构清晰
  - 便于Git版本控制
  - 易于编辑和转换

## 📊 数据完整度评分系统

### 评分标准（总分100%）

| 项目 | 权重 | 说明 |
|------|------|------|
| 名称 | 10% | 不等式名称 |
| 数学形式 | 20% | 不等式的数学表达式 |
| 描述 | 10% | 简要说明 |
| 条件 | 10% | 应用条件 |
| 证明方法 | 30% | 每个证法15%，最多2个 |
| 例题 | 20% | 每个例题10%，最多2个 |

### 完整度等级

- **100%**: 全部完整，包含所有要素
- **80-99%**: 基本完整，缺少少量信息
- **60-79%**: 部分完整，有重要信息缺失
- **<60%**: 不完整，需要补充

## 🚀 性能优化

### 已实现的优化

1. **多线程爬取**
   - 可配置线程数
   - 并发处理多个不等式
   - 显著减少总时间

2. **增量更新**
   - 保留已有完整数据
   - 只更新缺失部分
   - 避免重复爬取

3. **请求延迟控制**
   - 避免被反爬虫系统拦截
   - 可配置延迟时间
   - 尊重网站服务条款

4. **缓存机制**
   - JSON文件作为本地缓存
   - 重复运行时快速读取
   - 支持离线文档生成

### 可能的改进

1. 使用异步IO (aiohttp)
2. 添加Redis缓存
3. 实现更智能的爬取策略
4. 添加OCR识别图片中的公式

## 🧪 测试覆盖

### test_basic.py

测试内容：
- ✅ 数据模型的创建和序列化
- ✅ 解析器的功能
- ✅ 数据库的增删改查
- ✅ 文档生成器的分类功能

### 运行测试

```bash
python test_basic.py
```

## 📈 使用场景

1. **学生学习**
   - 快速查阅不等式定义
   - 学习证明方法
   - 练习例题

2. **教师教学**
   - 备课参考资料
   - 习题库
   - 讲义制作

3. **研究参考**
   - 不等式快速检索
   - 应用场景查找
   - 相关不等式关联

4. **考试复习**
   - 系统性复习
   - 打印复习资料
   - 离线查阅

## 🔧 技术栈详解

### 核心依赖

| 库 | 版本 | 用途 |
|---|------|------|
| requests | 2.31+ | HTTP请求 |
| beautifulsoup4 | 4.12+ | HTML解析 |
| lxml | 4.9+ | XML/HTML解析器 |
| jinja2 | 3.1+ | 模板引擎 |
| markdown | 3.5+ | Markdown处理 |
| fake-useragent | 1.4+ | User-Agent生成 |

### 可选依赖

| 库 | 用途 |
|---|------|
| weasyprint | PDF生成 |
| selenium | 动态页面爬取 |
| pandas | 数据分析 |

## 📝 日志系统

### 日志级别

- INFO: 正常流程信息
- WARNING: 警告信息（如爬取失败）
- ERROR: 错误信息（如解析失败）

### 日志输出

- 控制台：实时显示
- 文件：inequality_summarizer.log

### 日志内容

- 时间戳
- 日志级别
- 模块名称
- 详细信息

## 🔒 安全和合规

### 爬虫道德

1. 遵守robots.txt
2. 合理的请求延迟
3. 不过度请求
4. 尊重版权

### 数据使用

- 仅用于教育目的
- 不用于商业用途
- 引用来源网站

## 🛣️ 未来规划

### 短期目标

- [ ] 添加更多预定义数据
- [ ] 改进数学公式识别
- [ ] 优化文档样式
- [ ] 添加搜索功能

### 长期目标

- [ ] Web界面
- [ ] 在线编辑功能
- [ ] 用户贡献系统
- [ ] 多语言支持
- [ ] 移动应用

## 📞 联系和贡献

- 问题反馈：提交Issue
- 代码贡献：提交Pull Request
- 数据贡献：编辑预定义数据

## 📄 许可证

MIT License - 详见项目根目录

---

**最后更新**: 2025-12-28  
**版本**: 1.0.0
