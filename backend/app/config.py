from pydantic_settings import BaseSettings
from typing import List
import os
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 获取当前文件所在目录的父目录（backend目录）
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./interview_questions.db"
    OPENAI_API_KEY_OVERRIDE: str = ""
    OPENAI_BASE_URL_OVERRIDE: str = "https://api.openai.com/v1"
    OPENAI_MODEL_OVERRIDE: str = "gpt-3.5-turbo"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Interview Question Bank API"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # 兼容性属性：提供原始名称的访问方式
    @property
    def OPENAI_API_KEY(self) -> str:
        """兼容旧代码"""
        return self.OPENAI_API_KEY_OVERRIDE
    
    @property
    def OPENAI_BASE_URL(self) -> str:
        """兼容旧代码"""
        return self.OPENAI_BASE_URL_OVERRIDE
    
    @property
    def OPENAI_MODEL(self) -> str:
        """兼容旧代码"""
        return self.OPENAI_MODEL_OVERRIDE
    
    class Config:
        # 使用绝对路径指向 .env 文件
        env_file = str(ENV_FILE_PATH)
        env_file_encoding = 'utf-8'
    
    def log_config(self):
        """打印配置信息（隐藏敏感信息）"""
        logger.info("=" * 60)
        logger.info("⚙️  Application Configuration")
        logger.info("=" * 60)
        logger.info(f"📁 BASE_DIR: {BASE_DIR}")
        logger.info(f"📄 .env file: {ENV_FILE_PATH}")
        logger.info(f"📄 .env exists: {ENV_FILE_PATH.exists()}")
        logger.info("-" * 60)
        
        # 检查各配置项是否被环境变量覆盖
        def get_override_suffix(key: str) -> str:
            """检查配置项是否被环境变量覆盖"""
            return " [env override]" if os.environ.get(key) else ""
        
        logger.info(f"🗄️  DATABASE_URL{get_override_suffix('DATABASE_URL')}: {self.DATABASE_URL}")
        logger.info(f"🤖 OPENAI_BASE_URL{get_override_suffix('OPENAI_BASE_URL_OVERRIDE')}: {self.OPENAI_BASE_URL_OVERRIDE}")
        logger.info(f"🤖 OPENAI_MODEL{get_override_suffix('OPENAI_MODEL_OVERRIDE')}: {self.OPENAI_MODEL_OVERRIDE}")
        
        # 隐藏 API Key 的大部分内容，只显示前后几位
        if self.OPENAI_API_KEY_OVERRIDE:
            masked_key = f"{self.OPENAI_API_KEY_OVERRIDE[:8]}...{self.OPENAI_API_KEY_OVERRIDE[-4:]}"
            override_suffix = get_override_suffix('OPENAI_API_KEY_OVERRIDE')
            logger.info(f"🔑 OPENAI_API_KEY{override_suffix}: {masked_key}")
        else:
            logger.warning("⚠️  OPENAI_API_KEY: 未配置（AI 功能将不可用）")
        
        logger.info(f"🌐 API_V1_STR{get_override_suffix('API_V1_STR')}: {self.API_V1_STR}")
        logger.info(f"📦 PROJECT_NAME{get_override_suffix('PROJECT_NAME')}: {self.PROJECT_NAME}")
        logger.info(f"🔗 CORS_ORIGINS{get_override_suffix('CORS_ORIGINS')}: {self.CORS_ORIGINS}")
        logger.info("=" * 60)
        
        # 检查是否存在旧的环境变量名
        old_env_vars = {
            'OPENAI_API_KEY': 'OPENAI_API_KEY_OVERRIDE',
            'OPENAI_BASE_URL': 'OPENAI_BASE_URL_OVERRIDE',
            'OPENAI_MODEL': 'OPENAI_MODEL_OVERRIDE'
        }
        
        for old_name, new_name in old_env_vars.items():
            if os.environ.get(old_name):
                logger.warning("")
                logger.warning(f"⚠️  警告：检测到旧的环境变量 {old_name}")
                logger.warning(f"   建议：请使用新的变量名 {new_name} 以避免系统环境变量冲突")
                logger.warning(f"   当前应用使用的是 {new_name} 配置（不受 {old_name} 影响）")
                logger.warning("")

settings = Settings()

# 在模块加载时自动打印配置信息
settings.log_config()