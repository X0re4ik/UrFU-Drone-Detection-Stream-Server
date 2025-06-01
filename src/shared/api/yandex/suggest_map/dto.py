from pydantic import BaseModel


class YandexMapDistanceDTO(BaseModel):
    text: str
    value: float


class YandexMapResultDTO(BaseModel):
    title: str
    distance: YandexMapDistanceDTO
