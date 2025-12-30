"""
自定义异常类
定义项目特定的异常类型,便于精确的错误处理
"""


class ContestTradeException(Exception):
    """ContestTrade基础异常类"""
    pass


class ConfigurationError(ContestTradeException):
    """配置错误"""
    pass


class ValidationError(ContestTradeException):
    """验证错误"""
    pass


class DataSourceError(ContestTradeException):
    """数据源错误"""
    pass


class DataFetchError(DataSourceError):
    """数据获取错误"""
    pass


class DataParseError(DataSourceError):
    """数据解析错误"""
    pass


class APIError(ContestTradeException):
    """API调用错误"""
    pass


class APITimeoutError(APIError):
    """API超时错误"""
    pass


class APIRateLimitError(APIError):
    """API速率限制错误"""
    pass


class LLMError(ContestTradeException):
    """LLM相关错误"""
    pass


class LLMResponseError(LLMError):
    """LLM响应错误"""
    pass


class LLMParseError(LLMError):
    """LLM输出解析错误"""
    pass


class AgentError(ContestTradeException):
    """Agent执行错误"""
    pass


class AgentTimeoutError(AgentError):
    """Agent执行超时"""
    pass


class ToolError(ContestTradeException):
    """工具执行错误"""
    pass


class ToolNotFoundError(ToolError):
    """工具未找到"""
    pass


class MarketError(ContestTradeException):
    """市场相关错误"""
    pass


class InvalidMarketError(MarketError):
    """无效的市场类型"""
    pass


class InvalidSymbolError(MarketError):
    """无效的股票代码"""
    pass


class SignalParseError(ContestTradeException):
    """信号解析错误"""
    pass


class FactorParseError(ContestTradeException):
    """因子解析错误"""
    pass


# 导出所有异常类
__all__ = [
    'ContestTradeException',
    'ConfigurationError',
    'ValidationError',
    'DataSourceError',
    'DataFetchError',
    'DataParseError',
    'APIError',
    'APITimeoutError',
    'APIRateLimitError',
    'LLMError',
    'LLMResponseError',
    'LLMParseError',
    'AgentError',
    'AgentTimeoutError',
    'ToolError',
    'ToolNotFoundError',
    'MarketError',
    'InvalidMarketError',
    'InvalidSymbolError',
    'SignalParseError',
    'FactorParseError'
]
