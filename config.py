import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

DATA_FILE = os.path.join(DATA_DIR, 'inequalities.json')

CRAWL_DELAY = 2
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

REQUEST_TIMEOUT = 30

INEQUALITY_NAMES = [
    "基本不等式",
    "重要不等式",
    "糖水不等式",
    "常用不等式",
    "二元均值不等式",
    "二元均值不等式（衍生）",
    "三元均值不等式",
    "n元均值不等式",
    "绝对值三角不等式",
    "指数不等式",
    "指数不等式链",
    "对数不等式",
    "对数不等式链1",
    "对数不等式链2",
    "对数不等式链3",
    "三角函数不等式",
    "柯西不等式",
    "Aczel不等式",
    "权方和不等式",
    "权方差不等式",
    "幂平均不等式",
    "排序不等式",
    "琴生不等式",
    "卡尔森不等式",
    "闵可夫斯基不等式",
    "舒尔不等式",
    "穆尔海德不等式",
    "切比雪夫不等式",
    "伯努利不等式",
    "赫尔德不等式",
    "杨氏不等式",
    "嵌入不等式",
    "波波维奇亚不等式",
    "卡拉马特不等式",
    "米尔黑德不等式",
    "麦克劳林不等式",
    "范数不等式",
    "Fan Ky不等式"
]

SEARCH_SOURCES = {
    'wikipedia_zh': 'https://zh.wikipedia.org/wiki/',
    'wikipedia_en': 'https://en.wikipedia.org/wiki/',
    'baidu_baike': 'https://baike.baidu.com/item/',
}
