"""
输入验证工具模块
提供各种输入数据的验证功能
"""
from datetime import datetime
from typing import Optional, List
import re
from loguru import logger


class InputValidator:
    """输入验证工具类"""
    
    @staticmethod
    def validate_date_format(date_str: str, format: str = "%Y-%m-%d") -> bool:
        """
        验证日期格式
        
        Args:
            date_str: 日期字符串
            format: 期望的日期格式
            
        Returns:
            是否符合格式
        """
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError as e:
            logger.warning(f"Invalid date format: {date_str}, expected format: {format}, error: {e}")
            return False
    
    @staticmethod
    def validate_date_range(date_str: str, min_date: Optional[str] = None, max_date: Optional[str] = None) -> bool:
        """
        验证日期是否在指定范围内
        
        Args:
            date_str: 日期字符串
            min_date: 最小日期
            max_date: 最大日期
            
        Returns:
            是否在范围内
        """
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            if min_date:
                min_date_obj = datetime.strptime(min_date, "%Y-%m-%d")
                if date_obj < min_date_obj:
                    logger.warning(f"Date {date_str} is before minimum date {min_date}")
                    return False
            
            if max_date:
                max_date_obj = datetime.strptime(max_date, "%Y-%m-%d")
                if date_obj > max_date_obj:
                    logger.warning(f"Date {date_str} is after maximum date {max_date}")
                    return False
            
            return True
        except ValueError as e:
            logger.error(f"Error validating date range: {e}")
            return False
    
    @staticmethod
    def validate_stock_symbol(symbol: str, market: str = "CN") -> bool:
        """
        验证股票代码格式
        
        Args:
            symbol: 股票代码
            market: 市场类型 (CN=中国A股, US=美股, HK=港股)
            
        Returns:
            是否符合格式
        """
        if not symbol:
            logger.warning("Stock symbol is empty")
            return False
        
        symbol = symbol.strip().upper()
        
        if market == "CN":
            # A股代码格式: 6位数字
            if not re.match(r'^\d{6}$', symbol):
                logger.warning(f"Invalid CN stock symbol format: {symbol}, expected 6 digits")
                return False
        elif market == "US":
            # 美股代码格式: 1-5个大写字母
            if not re.match(r'^[A-Z]{1,5}$', symbol):
                logger.warning(f"Invalid US stock symbol format: {symbol}, expected 1-5 uppercase letters")
                return False
        elif market == "HK":
            # 港股代码格式: 5位数字
            if not re.match(r'^\d{5}$', symbol):
                logger.warning(f"Invalid HK stock symbol format: {symbol}, expected 5 digits")
                return False
        else:
            logger.warning(f"Unsupported market type: {market}")
            return False
        
        return True
    
    @staticmethod
    def validate_stock_symbols(symbols: List[str], market: str = "CN") -> tuple[bool, List[str]]:
        """
        批量验证股票代码
        
        Args:
            symbols: 股票代码列表
            market: 市场类型
            
        Returns:
            (是否全部有效, 无效代码列表)
        """
        invalid_symbols = []
        
        for symbol in symbols:
            if not InputValidator.validate_stock_symbol(symbol, market):
                invalid_symbols.append(symbol)
        
        is_valid = len(invalid_symbols) == 0
        
        if not is_valid:
            logger.warning(f"Found {len(invalid_symbols)} invalid symbols: {invalid_symbols}")
        
        return is_valid, invalid_symbols
    
    @staticmethod
    def validate_api_key(api_key: Optional[str], key_name: str) -> str:
        """
        验证API密钥非空
        
        Args:
            api_key: API密钥
            key_name: 密钥名称
            
        Returns:
            清理后的API密钥
            
        Raises:
            ValueError: 如果密钥为空
        """
        if not api_key or api_key.strip() == "":
            error_msg = f"{key_name} is required but not provided"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        return api_key.strip()
    
    @staticmethod
    def validate_positive_number(value: any, name: str, allow_zero: bool = False) -> bool:
        """
        验证正数
        
        Args:
            value: 要验证的值
            name: 参数名称
            allow_zero: 是否允许为0
            
        Returns:
            是否为有效的正数
        """
        try:
            num_value = float(value)
            
            if allow_zero:
                if num_value < 0:
                    logger.warning(f"{name} must be non-negative, got: {value}")
                    return False
            else:
                if num_value <= 0:
                    logger.warning(f"{name} must be positive, got: {value}")
                    return False
            
            return True
        except (ValueError, TypeError) as e:
            logger.warning(f"{name} must be a number, got: {value}, error: {e}")
            return False
    
    @staticmethod
    def validate_integer_range(value: any, name: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> bool:
        """
        验证整数范围
        
        Args:
            value: 要验证的值
            name: 参数名称
            min_val: 最小值(包含)
            max_val: 最大值(包含)
            
        Returns:
            是否在有效范围内
        """
        try:
            int_value = int(value)
            
            if min_val is not None and int_value < min_val:
                logger.warning(f"{name} must be >= {min_val}, got: {value}")
                return False
            
            if max_val is not None and int_value > max_val:
                logger.warning(f"{name} must be <= {max_val}, got: {value}")
                return False
            
            return True
        except (ValueError, TypeError) as e:
            logger.warning(f"{name} must be an integer, got: {value}, error: {e}")
            return False
    
    @staticmethod
    def validate_string_not_empty(value: Optional[str], name: str) -> bool:
        """
        验证字符串非空
        
        Args:
            value: 字符串值
            name: 参数名称
            
        Returns:
            是否非空
        """
        if not value or not value.strip():
            logger.warning(f"{name} cannot be empty")
            return False
        return True
    
    @staticmethod
    def validate_list_not_empty(value: Optional[List], name: str) -> bool:
        """
        验证列表非空
        
        Args:
            value: 列表值
            name: 参数名称
            
        Returns:
            是否非空
        """
        if not value or len(value) == 0:
            logger.warning(f"{name} cannot be empty")
            return False
        return True
    
    @staticmethod
    def validate_market_type(market: str) -> bool:
        """
        验证市场类型
        
        Args:
            market: 市场类型字符串
            
        Returns:
            是否为支持的市场类型
        """
        supported_markets = ["CN", "US", "HK"]
        
        if market.upper() not in supported_markets:
            logger.warning(f"Unsupported market type: {market}, supported: {supported_markets}")
            return False
        
        return True


class DataValidator:
    """数据验证工具类"""
    
    @staticmethod
    def validate_price_data(price: float, symbol: str) -> bool:
        """
        验证价格数据的合理性
        
        Args:
            price: 价格
            symbol: 股票代码
            
        Returns:
            价格是否合理
        """
        if price <= 0:
            logger.warning(f"Invalid price for {symbol}: {price} (must be positive)")
            return False
        
        # 检查是否为异常值(例如价格过高)
        if price > 1000000:
            logger.warning(f"Suspicious high price for {symbol}: {price}")
            return False
        
        return True
    
    @staticmethod
    def validate_volume_data(volume: int, symbol: str) -> bool:
        """
        验证成交量数据的合理性
        
        Args:
            volume: 成交量
            symbol: 股票代码
            
        Returns:
            成交量是否合理
        """
        if volume < 0:
            logger.warning(f"Invalid volume for {symbol}: {volume} (cannot be negative)")
            return False
        
        return True
    
    @staticmethod
    def validate_percentage(value: float, name: str, min_val: float = -100.0, max_val: float = 100.0) -> bool:
        """
        验证百分比值
        
        Args:
            value: 百分比值
            name: 参数名称
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            是否在合理范围内
        """
        if value < min_val or value > max_val:
            logger.warning(f"{name} out of range: {value}, expected [{min_val}, {max_val}]")
            return False
        
        return True
