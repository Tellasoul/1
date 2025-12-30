"""
重试机制工具模块
提供智能的重试策略,包括指数退避和抖动
"""
import asyncio
import random
from typing import Callable, TypeVar, Optional, Tuple, Type
from functools import wraps
from loguru import logger

T = TypeVar('T')


class RetryConfig:
    """重试配置类"""
    
    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        jitter_range: Tuple[float, float] = (0.5, 1.5)
    ):
        """
        初始化重试配置
        
        Args:
            max_retries: 最大重试次数
            initial_delay: 初始延迟时间(秒)
            max_delay: 最大延迟时间(秒)
            exponential_base: 指数退避的基数
            jitter: 是否添加抖动
            jitter_range: 抖动范围(乘数)
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.jitter_range = jitter_range
    
    def calculate_delay(self, attempt: int) -> float:
        """
        计算延迟时间(指数退避+抖动)
        
        Args:
            attempt: 当前重试次数(从0开始)
            
        Returns:
            延迟时间(秒)
        """
        # 计算指数退避延迟
        delay = min(
            self.initial_delay * (self.exponential_base ** attempt),
            self.max_delay
        )
        
        # 添加抖动
        if self.jitter:
            jitter_min, jitter_max = self.jitter_range
            jitter_factor = random.uniform(jitter_min, jitter_max)
            delay = delay * jitter_factor
        
        return delay


def async_retry(
    config: Optional[RetryConfig] = None,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None
):
    """
    异步重试装饰器
    
    Args:
        config: 重试配置,如果为None则使用默认配置
        exceptions: 需要重试的异常类型元组
        on_retry: 重试时的回调函数,接收(exception, attempt)参数
        
    Returns:
        装饰器函数
    """
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                    
                except exceptions as e:
                    last_exception = e
                    
                    # 如果是最后一次尝试,直接抛出异常
                    if attempt == config.max_retries:
                        logger.error(
                            f"Function {func.__name__} failed after {config.max_retries} retries: {str(e)}",
                            exc_info=True
                        )
                        raise
                    
                    # 计算延迟时间
                    delay = config.calculate_delay(attempt)
                    
                    logger.warning(
                        f"Function {func.__name__} failed (attempt {attempt + 1}/{config.max_retries}), "
                        f"retrying in {delay:.2f}s: {str(e)}"
                    )
                    
                    # 调用回调函数
                    if on_retry:
                        try:
                            on_retry(e, attempt)
                        except Exception as callback_error:
                            logger.error(f"Error in retry callback: {callback_error}")
                    
                    # 等待后重试
                    await asyncio.sleep(delay)
                
                except Exception as e:
                    # 不在重试列表中的异常直接抛出
                    logger.error(
                        f"Function {func.__name__} raised non-retryable exception: {type(e).__name__}: {str(e)}",
                        exc_info=True
                    )
                    raise
            
            # 理论上不会到达这里,但为了类型检查
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def sync_retry(
    config: Optional[RetryConfig] = None,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None
):
    """
    同步重试装饰器
    
    Args:
        config: 重试配置,如果为None则使用默认配置
        exceptions: 需要重试的异常类型元组
        on_retry: 重试时的回调函数,接收(exception, attempt)参数
        
    Returns:
        装饰器函数
    """
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    last_exception = e
                    
                    # 如果是最后一次尝试,直接抛出异常
                    if attempt == config.max_retries:
                        logger.error(
                            f"Function {func.__name__} failed after {config.max_retries} retries: {str(e)}",
                            exc_info=True
                        )
                        raise
                    
                    # 计算延迟时间
                    delay = config.calculate_delay(attempt)
                    
                    logger.warning(
                        f"Function {func.__name__} failed (attempt {attempt + 1}/{config.max_retries}), "
                        f"retrying in {delay:.2f}s: {str(e)}"
                    )
                    
                    # 调用回调函数
                    if on_retry:
                        try:
                            on_retry(e, attempt)
                        except Exception as callback_error:
                            logger.error(f"Error in retry callback: {callback_error}")
                    
                    # 等待后重试
                    import time
                    time.sleep(delay)
                
                except Exception as e:
                    # 不在重试列表中的异常直接抛出
                    logger.error(
                        f"Function {func.__name__} raised non-retryable exception: {type(e).__name__}: {str(e)}",
                        exc_info=True
                    )
                    raise
            
            # 理论上不会到达这里,但为了类型检查
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


class RetryContext:
    """重试上下文管理器"""
    
    def __init__(
        self,
        config: Optional[RetryConfig] = None,
        exceptions: Tuple[Type[Exception], ...] = (Exception,)
    ):
        """
        初始化重试上下文
        
        Args:
            config: 重试配置
            exceptions: 需要重试的异常类型元组
        """
        self.config = config or RetryConfig()
        self.exceptions = exceptions
        self.attempt = 0
        self.last_exception = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return True
        
        if not issubclass(exc_type, self.exceptions):
            # 不在重试列表中的异常,不处理
            return False
        
        self.last_exception = exc_val
        
        if self.attempt >= self.config.max_retries:
            # 已达到最大重试次数
            logger.error(
                f"Retry context failed after {self.config.max_retries} retries: {str(exc_val)}",
                exc_info=True
            )
            return False
        
        # 计算延迟并等待
        delay = self.config.calculate_delay(self.attempt)
        logger.warning(
            f"Retry context failed (attempt {self.attempt + 1}/{self.config.max_retries}), "
            f"retrying in {delay:.2f}s: {str(exc_val)}"
        )
        
        import time
        time.sleep(delay)
        self.attempt += 1
        
        # 返回True表示异常已处理,继续执行
        return True


# 使用示例
if __name__ == "__main__":
    # 示例1: 使用装饰器
    @async_retry(
        config=RetryConfig(max_retries=3, initial_delay=2.0),
        exceptions=(ValueError, ConnectionError)
    )
    async def fetch_data(url: str):
        # 模拟API调用
        import random
        if random.random() < 0.7:
            raise ConnectionError("Network error")
        return {"data": "success"}
    
    # 示例2: 使用上下文管理器
    def process_with_retry():
        retry_ctx = RetryContext(
            config=RetryConfig(max_retries=3),
            exceptions=(IOError,)
        )
        
        while retry_ctx.attempt <= retry_ctx.config.max_retries:
            with retry_ctx:
                # 可能失败的操作
                result = perform_operation()
                return result
        
        raise retry_ctx.last_exception
