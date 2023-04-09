import requests
from pathlib import Path
from collections import namedtuple

HERE = Path(__file__).parent
# 数据缓存文件存储目录
DATA_DIR = HERE / '../data'
# 创建数据缓存文件目录
DATA_DIR.mkdir(parents=True, exist_ok=True)
# 搜索词缓存位置
SEARCH_RESULT_CACHE_PATH = str(DATA_DIR / 'search-cache.json')
session = requests.Session()

# 存储证券代码的实体
Quote = namedtuple(
    'Quote',
    [
        'code',
        'name',
        'pinyin',
        'id',
        'jys',
        'classify',
        'market_type',
        'security_typeName',
        'security_type',
        'mkt_num',
        'type_us',
        'quote_id',
        'unified_code',
        'inner_code',
    ],
)