"""
环境变量安全加载器
提供安全的配置加载机制,优先使用环境变量
"""
import os
from typing import Optional
from loguru import logger


class SecureConfigLoader:
    """安全的配置加载器,优先使用环境变量"""
    
    @staticmethod
    def get_api_key(key_name: str, config_value: Optional[str] = None) -> Optional[str]:
        """
        按优先级获取API密钥:
        1. 环境变量 (最高优先级)
        2. 配置文件
        
        Args:
            key_name: 密钥名称(会自动转换为大写作为环境变量名)
            config_value: 配置文件中的值
            
        Returns:
            API密钥值,如果都不存在则返回None
        """
        env_key = key_name.upper()
        env_value = os.environ.get(env_key)
        
        if env_value:
            logger.debug(f"Using {key_name} from environment variable")
            return env_value
        
        if config_value:
            logger.debug(f"Using {key_name} from config file")
            return config_value
        
        logger.warning(f"{key_name} not found in environment or config")
        return None
    
    @staticmethod
    def validate_required_keys(keys: dict) -> bool:
        """
        验证必需的API密钥是否存在
        
        Args:
            keys: 字典,键为密钥名称,值为密钥值
            
        Returns:
            如果所有必需密钥都存在返回True
            
        Raises:
            ValueError: 如果有缺失的必需密钥
        """
        missing_keys = [k for k, v in keys.items() if not v or str(v).strip() == ""]
        
        if missing_keys:
            error_msg = f"Missing required API keys: {', '.join(missing_keys)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("All required API keys validated successfully")
        return True
    
    @staticmethod
    def get_config_value(
        key_name: str,
        config_value: Optional[str] = None,
        default: Optional[str] = None,
        required: bool = False
    ) -> Optional[str]:
        """
        获取配置值的通用方法
        
        Args:
            key_name: 配置键名
            config_value: 配置文件中的值
            default: 默认值
            required: 是否为必需配置
            
        Returns:
            配置值
            
        Raises:
            ValueError: 如果required=True且值不存在
        """
        value = SecureConfigLoader.get_api_key(key_name, config_value) or default
        
        if required and not value:
            error_msg = f"Required configuration '{key_name}' is missing"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        return value


class ConfigValidator:
    """配置验证器"""
    
    @staticmethod
    def validate_url(url: Optional[str], name: str = "URL") -> bool:
        """
        验证URL格式
        
        Args:
            url: URL字符串
            name: URL名称(用于错误消息)
            
        Returns:
            验证是否通过
        """
        if not url:
            return False
        
        if not (url.startswith('http://') or url.startswith('https://')):
            logger.warning(f"{name} should start with http:// or https://: {url}")
            return False
        
        return True
    
    @staticmethod
    def validate_model_config(config: dict, provider: str) -> bool:
        """
        验证模型配置的完整性
        
        Args:
            config: 模型配置字典
            provider: 提供商类型(openai, gemini, ollama)
            
        Returns:
            验证是否通过
            
        Raises:
            ValueError: 如果配置不完整或无效
        """
        required_fields = ['model_name']
        
        # OpenAI和Gemini需要API密钥
        if provider in ['openai', 'gemini']:
            required_fields.extend(['api_key', 'base_url'])
        
        missing_fields = [field for field in required_fields if not config.get(field)]
        
        if missing_fields:
            error_msg = f"Missing required fields for {provider}: {', '.join(missing_fields)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # 验证URL格式
        if 'base_url' in config and config['base_url']:
            if not ConfigValidator.validate_url(config['base_url'], f"{provider} base_url"):
                logger.warning(f"Invalid base_url format for {provider}")
        
        logger.info(f"Model configuration for {provider} validated successfully")
        return True
