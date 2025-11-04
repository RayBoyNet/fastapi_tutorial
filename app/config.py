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
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    
settings = Settings()