from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ConfigDict, Field
from dotenv import load_dotenv
import torch

load_dotenv()


class BaseConfig(BaseSettings):
    """ """

    model_config = SettingsConfigDict(
        extra="allow", env_file=".env", env_file_encoding="utf-8"
    )


class APPConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="APP_")

    develop: bool = Field(default=False)
    logger_level: str = Field(default="INFO")

    device: str = Field(
        default_factory=lambda: "cuda" if torch.cuda.is_available() else "cpu"
    )


class MongoDBConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="MONGO_DB_")

    user: str
    password: str
    host: str
    port: int

    @property
    def URI(self) -> str:
        return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/"


class RTSPStreamConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="RTSP_STREAM_")

    input_url: str
    output_url: str

    output_logger_file: str = Field(default_factory=lambda: "ffmpeg-rtsp.log")

    output_fps: int | None = Field(default=None)

    hls_fragment_sec: int = Field(default=2)


class S3Config(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="S3_")

    host: str
    port: int
    aws_access_key: str
    aws_secret_key: str

    bucket: str

    use_ssl: bool = Field(default=False)


class TelegramBotConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="TELEGRAM_BOT_")

    user_token: str
    service_token: str
    service_chat_id: str


class YandexMapConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="YANDEX_MAP_")

    suggest_api_key: str
    geocode_api_key: str


class Settings(BaseConfig):
    app: APPConfig = Field(default_factory=APPConfig)
    rtsp_stream: RTSPStreamConfig = Field(default_factory=RTSPStreamConfig)
    mongo_db: MongoDBConfig = Field(default_factory=MongoDBConfig)
    s3: S3Config = Field(default_factory=S3Config)
    telegram_bot: TelegramBotConfig = Field(default_factory=TelegramBotConfig)
    yandex_map: YandexMapConfig = Field(default_factory=YandexMapConfig)
