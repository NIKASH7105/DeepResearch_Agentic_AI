"""
Configuration management for DeepResearch Agent
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # LLM Configuration
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    llm_model: str = Field(default="llama3.2", env="LLM_MODEL")
    llm_temperature: float = Field(default=0.7, env="LLM_TEMPERATURE")
    max_tokens: int = Field(default=4096, env="MAX_TOKENS")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        env="CORS_ORIGINS"
    )
    
    # Research Configuration
    max_research_iterations: int = Field(default=10, env="MAX_RESEARCH_ITERATIONS")
    max_sources_per_query: int = Field(default=15, env="MAX_SOURCES_PER_QUERY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self):
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
