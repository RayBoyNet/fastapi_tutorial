from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    algorithm: str 
    secret_key: str 
    access_token_exp_minutes: int 
    db_username: str 
    db_password: str 
    db_hostname: str 
    db_port: str 
    db_name: str 
    
    class Config:
        env_file = '.env'
    
settings = Settings()