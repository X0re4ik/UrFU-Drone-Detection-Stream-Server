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
    name: str

    @property
    def URI(self) -> str:
        return (
            f"mongodb://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/"
            f"{self.name}"
        )


class RTSPStreamConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="RTSP_STREAM_")

    input_url: str
    output_url: str

    output_logger_file: str = Field(default_factory=lambda: "ffmpeg-rtsp")

    output_fps: int = Field(default=25)

    hls_fragment_sec: int = Field(default=2)


class Settings(BaseConfig):
    app: APPConfig = Field(default_factory=APPConfig)
    rtsp_stream: RTSPStreamConfig = Field(default_factory=RTSPStreamConfig)
    mongo_db: MongoDBConfig = Field(default_factory=MongoDBConfig)
