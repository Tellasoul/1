"""
系统常量定义
将硬编码的魔法数字提取为有意义的常量
"""


class DataAgentConstants:
    """数据分析Agent相关常量"""
    
    # 并发控制
    MAX_CONCURRENT_TASKS = 6  # 最大并发任务数
    
    # 批处理配置
    CREDITS_PER_BATCH = 10  # 每批次的信用额度
    CONTENT_CUTOFF_LENGTH = 2000  # 内容截断长度(字符)
    
    # LLM配置
    MAX_LLM_CONTEXT = 28000  # LLM最大上下文长度(tokens)
    LLM_CALL_NUM = 2  # 每批次LLM调用次数
    FINAL_TARGET_TOKENS = 4000  # 最终输出目标token数
    
    # 数据源配置
    DEFAULT_DATA_SOURCES = [
        "data_source.sina_news_crawl.SinaNewsCrawl",
        "data_source.thx_news_crawl.ThxNewsCrawl",
        "data_source.price_market_akshare.PriceMarketAkshare",
        "data_source.hot_money_akshare.HotMoneyAkshare"
    ]


class ResearchAgentConstants:
    """研究Agent相关常量"""
    
    # ReAct循环配置
    MAX_REACT_STEP = 10  # 最大ReAct步骤数
    MIN_REACT_STEP = 1  # 最小ReAct步骤数
    
    # 信号输出配置
    MAX_SIGNALS_PER_AGENT = 5  # 每个agent最多输出信号数
    MIN_CONFIDENCE_THRESHOLD = 0.6  # 最小置信度阈值
    
    # 工具配置
    DEFAULT_TOOLS = [
        "tools.stock_symbol_search_akshare.stock_symbol_search",
        "tools.stock_selector_akshare.stock_selector",
        "tools.corp_info_akshare.company_financial_info",
        "tools.price_info_akshare.price_info",
        "tools.search_web.search_web",
        "tools.stock_summary_akshare.stock_summary",
        "tools.final_report.final_report"
    ]


class APIConstants:
    """API调用相关常量"""
    
    # 超时配置
    DEFAULT_TIMEOUT = 60.0  # 默认超时时间(秒)
    LONG_TIMEOUT = 120.0  # 长超时时间(秒)
    SHORT_TIMEOUT = 30.0  # 短超时时间(秒)
    
    # 重试配置
    MAX_RETRIES = 3  # 最大重试次数
    RETRY_DELAY = 20.0  # 重试延迟(秒) - 将被新的指数退避策略替代
    INITIAL_RETRY_DELAY = 1.0  # 初始重试延迟(秒)
    MAX_RETRY_DELAY = 60.0  # 最大重试延迟(秒)
    EXPONENTIAL_BASE = 2.0  # 指数退避基数
    
    # 速率限制
    RATE_LIMIT_DELAY = 1.0  # 速率限制延迟(秒)
    RATE_LIMIT_CALLS_PER_MINUTE = 60  # 每分钟最大调用次数
    
    # HTTP状态码
    HTTP_SUCCESS_CODES = [200, 201, 202]
    HTTP_RETRY_CODES = [429, 500, 502, 503, 504]  # 可重试的HTTP错误码


class PathConstants:
    """文件路径相关常量"""
    
    # 目录路径
    WORKSPACE_DIR = "agents_workspace"
    RESULTS_DIR = "agents_workspace/results"
    CACHE_DIR = "utils/cache"
    LOGS_DIR = "logs"
    CONFIG_DIR = "config"
    
    # 配置文件
    BELIEF_LIST_FILE = "config/belief_list.json"
    MARKET_CONFIG_FILE = "config/market_config.yaml"
    MARKET_CONFIG_US_FILE = "config/market_config_us.yaml"
    
    # 日志文件
    DEFAULT_LOG_FILE = "logs/contesttrade.log"
    ERROR_LOG_FILE = "logs/error.log"
    
    # 缓存文件
    PRICE_CACHE_FILE = "utils/cache/price_cache.json"
    NEWS_CACHE_FILE = "utils/cache/news_cache.json"


class MarketConstants:
    """市场相关常量"""
    
    # 支持的市场类型
    MARKET_CN = "CN"  # 中国A股
    MARKET_US = "US"  # 美股
    MARKET_HK = "HK"  # 港股
    
    SUPPORTED_MARKETS = [MARKET_CN, MARKET_US, MARKET_HK]
    
    # 交易时间(仅用于参考)
    CN_TRADING_HOURS = {
        "morning_start": "09:30",
        "morning_end": "11:30",
        "afternoon_start": "13:00",
        "afternoon_end": "15:00"
    }
    
    US_TRADING_HOURS = {
        "regular_start": "09:30",  # EST
        "regular_end": "16:00"  # EST
    }
    
    # 股票代码格式
    CN_STOCK_CODE_LENGTH = 6
    US_STOCK_CODE_MIN_LENGTH = 1
    US_STOCK_CODE_MAX_LENGTH = 5
    HK_STOCK_CODE_LENGTH = 5


class LLMConstants:
    """LLM模型相关常量"""
    
    # 支持的提供商
    PROVIDER_OPENAI = "openai"
    PROVIDER_GEMINI = "gemini"
    PROVIDER_OLLAMA = "ollama"
    
    SUPPORTED_PROVIDERS = [PROVIDER_OPENAI, PROVIDER_GEMINI, PROVIDER_OLLAMA]
    
    # 模型参数默认值
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 4096
    DEFAULT_TOP_P = 0.9
    
    # Token限制
    MAX_INPUT_TOKENS = 128000  # 最大输入token数
    MAX_OUTPUT_TOKENS = 8192  # 最大输出token数
    
    # 流式输出
    STREAM_CHUNK_SIZE = 1024  # 流式输出块大小


class ContestConstants:
    """竞赛机制相关常量"""
    
    # 评估配置
    NUM_JUDGERS = 3  # 评委数量
    WINDOW_M = 3  # 时间窗口M
    WINDOW_N = 3  # 时间窗口N
    
    # 评分配置
    MIN_SCORE = 0.0  # 最小评分
    MAX_SCORE = 10.0  # 最大评分
    PASS_SCORE = 6.0  # 及格分数
    
    # 权重配置
    DEFAULT_WEIGHT = 1.0  # 默认权重
    MIN_WEIGHT = 0.0  # 最小权重
    MAX_WEIGHT = 1.0  # 最大权重


class ValidationConstants:
    """验证相关常量"""
    
    # 日期格式
    DATE_FORMAT = "%Y-%m-%d"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # 数值范围
    MIN_PRICE = 0.01  # 最小股价
    MAX_PRICE = 1000000.0  # 最大股价(用于异常检测)
    MIN_VOLUME = 0  # 最小成交量
    
    # 百分比范围
    MIN_PERCENTAGE = -100.0
    MAX_PERCENTAGE = 100.0
    
    # 字符串长度限制
    MAX_SYMBOL_LENGTH = 10
    MAX_NAME_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 5000


class LogConstants:
    """日志相关常量"""
    
    # 日志级别
    LEVEL_DEBUG = "DEBUG"
    LEVEL_INFO = "INFO"
    LEVEL_WARNING = "WARNING"
    LEVEL_ERROR = "ERROR"
    LEVEL_CRITICAL = "CRITICAL"
    
    # 日志轮转
    LOG_ROTATION = "500 MB"  # 日志文件大小限制
    LOG_RETENTION = "10 days"  # 日志保留时间
    LOG_COMPRESSION = "zip"  # 日志压缩格式
    
    # 日志格式
    DEFAULT_FORMAT = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    SIMPLE_FORMAT = "{time:HH:mm:ss} | {level} | {message}"


class CacheConstants:
    """缓存相关常量"""
    
    # 缓存过期时间(秒)
    CACHE_EXPIRE_SHORT = 300  # 5分钟
    CACHE_EXPIRE_MEDIUM = 3600  # 1小时
    CACHE_EXPIRE_LONG = 86400  # 24小时
    
    # 缓存大小限制
    MAX_CACHE_SIZE_MB = 100  # 最大缓存大小(MB)
    MAX_CACHE_ENTRIES = 1000  # 最大缓存条目数


# 导出所有常量类
__all__ = [
    'DataAgentConstants',
    'ResearchAgentConstants',
    'APIConstants',
    'PathConstants',
    'MarketConstants',
    'LLMConstants',
    'ContestConstants',
    'ValidationConstants',
    'LogConstants',
    'CacheConstants'
]
