"""
日志配置模块
提供统一的日志配置和管理
"""
import sys
from pathlib import Path
from typing import Optional
from loguru import logger
from config.constants import LogConstants, PathConstants


class LoggerConfig:
    """统一的日志配置管理器"""
    
    _initialized = False
    
    @staticmethod
    def setup_logger(
        log_level: str = LogConstants.LEVEL_INFO,
        log_file: Optional[str] = None,
        rotation: str = LogConstants.LOG_ROTATION,
        retention: str = LogConstants.LOG_RETENTION,
        compression: str = LogConstants.LOG_COMPRESSION,
        format_string: Optional[str] = None,
        enable_console: bool = True,
        enable_file: bool = True,
        colorize: bool = True
    ):
        """
        配置全局logger
        
        Args:
            log_level: 日志级别(DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: 日志文件路径,如果为None则使用默认路径
            rotation: 日志轮转策略(如"500 MB", "1 day")
            retention: 日志保留策略(如"10 days", "1 week")
            compression: 日志压缩格式(如"zip", "gz")
            format_string: 自定义日志格式,如果为None则使用默认格式
            enable_console: 是否启用控制台输出
            enable_file: 是否启用文件输出
            colorize: 控制台输出是否使用颜色
            
        Returns:
            配置后的logger实例
        """
        # 避免重复初始化
        if LoggerConfig._initialized:
            logger.warning("Logger already initialized, skipping re-initialization")
            return logger
        
        # 移除默认handler
        logger.remove()
        
        # 使用默认格式或自定义格式
        if format_string is None:
            format_string = LogConstants.DEFAULT_FORMAT
        
        # 添加控制台输出
        if enable_console:
            logger.add(
                sys.stderr,
                format=format_string,
                level=log_level,
                colorize=colorize,
                backtrace=True,
                diagnose=True
            )
        
        # 添加文件输出
        if enable_file:
            if log_file is None:
                log_file = PathConstants.DEFAULT_LOG_FILE
            
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.add(
                log_file,
                format=format_string,
                level=log_level,
                rotation=rotation,
                retention=retention,
                compression=compression,
                encoding="utf-8",
                backtrace=True,
                diagnose=True,
                enqueue=True  # 异步写入,避免阻塞
            )
        
        LoggerConfig._initialized = True
        logger.info(f"Logger initialized with level: {log_level}")
        
        return logger
    
    @staticmethod
    def add_error_log_file(
        error_log_file: Optional[str] = None,
        rotation: str = LogConstants.LOG_ROTATION,
        retention: str = LogConstants.LOG_RETENTION
    ):
        """
        添加单独的错误日志文件
        
        Args:
            error_log_file: 错误日志文件路径
            rotation: 日志轮转策略
            retention: 日志保留策略
        """
        if error_log_file is None:
            error_log_file = PathConstants.ERROR_LOG_FILE
        
        error_log_path = Path(error_log_file)
        error_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            error_log_file,
            format=LogConstants.DEFAULT_FORMAT,
            level=LogConstants.LEVEL_ERROR,
            rotation=rotation,
            retention=retention,
            compression=LogConstants.LOG_COMPRESSION,
            encoding="utf-8",
            backtrace=True,
            diagnose=True,
            enqueue=True,
            filter=lambda record: record["level"].name in ["ERROR", "CRITICAL"]
        )
        
        logger.info(f"Error log file added: {error_log_file}")
    
    @staticmethod
    def setup_simple_logger(log_level: str = LogConstants.LEVEL_INFO):
        """
        配置简单的logger(仅控制台输出,简单格式)
        
        Args:
            log_level: 日志级别
            
        Returns:
            配置后的logger实例
        """
        logger.remove()
        
        logger.add(
            sys.stderr,
            format=LogConstants.SIMPLE_FORMAT,
            level=log_level,
            colorize=True
        )
        
        LoggerConfig._initialized = True
        
        return logger
    
    @staticmethod
    def get_logger():
        """
        获取logger实例
        
        Returns:
            logger实例
        """
        if not LoggerConfig._initialized:
            LoggerConfig.setup_logger()
        
        return logger
    
    @staticmethod
    def set_level(level: str):
        """
        动态设置日志级别
        
        Args:
            level: 日志级别
        """
        # 注意: loguru不支持动态修改已添加handler的级别
        # 需要重新配置logger
        logger.warning(f"Changing log level to {level} requires logger reconfiguration")
        LoggerConfig._initialized = False
        LoggerConfig.setup_logger(log_level=level)


class ContextLogger:
    """带上下文信息的logger包装器"""
    
    def __init__(self, context: dict):
        """
        初始化上下文logger
        
        Args:
            context: 上下文信息字典
        """
        self.context = context
        self.logger = logger.bind(**context)
    
    def debug(self, message: str, **kwargs):
        """Debug级别日志"""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Info级别日志"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Warning级别日志"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Error级别日志"""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Critical级别日志"""
        self.logger.critical(message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """记录异常信息"""
        self.logger.exception(message, **kwargs)


def get_agent_logger(agent_name: str, agent_id: Optional[int] = None) -> ContextLogger:
    """
    获取带agent上下文的logger
    
    Args:
        agent_name: agent名称
        agent_id: agent ID
        
    Returns:
        带上下文的logger
    """
    context = {"agent_name": agent_name}
    if agent_id is not None:
        context["agent_id"] = agent_id
    
    return ContextLogger(context)


def get_tool_logger(tool_name: str) -> ContextLogger:
    """
    获取带tool上下文的logger
    
    Args:
        tool_name: 工具名称
        
    Returns:
        带上下文的logger
    """
    return ContextLogger({"tool_name": tool_name})


# 使用示例
if __name__ == "__main__":
    # 示例1: 基本配置
    LoggerConfig.setup_logger(log_level="DEBUG")
    logger.info("This is an info message")
    logger.error("This is an error message")
    
    # 示例2: 添加错误日志文件
    LoggerConfig.add_error_log_file()
    
    # 示例3: 使用上下文logger
    agent_logger = get_agent_logger("data_agent", 1)
    agent_logger.info("Agent started processing")
    
    # 示例4: 简单logger
    LoggerConfig.setup_simple_logger()
    logger.info("Simple log message")
