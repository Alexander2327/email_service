from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8003


class MailConfig(BaseModel):
    email_from: str
    port: int
    host: str
    user: str
    password: str


class BrokerConfig(BaseModel):
    url: str
    mail_queue: str
    callback_mail_queue: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env",),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig
    mail: MailConfig
    broker: BrokerConfig


settings = Settings()
