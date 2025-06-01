from .client import YandexSuggestMapsClientAPI
from .dto import YandexMapResultDTO, YandexMapDistanceDTO

from src.shared.configs import PROJECT_SETTINGS


yandex_suggest_map_client_api = YandexSuggestMapsClientAPI(api_key=PROJECT_SETTINGS.yandex_map.suggest_api_key)
