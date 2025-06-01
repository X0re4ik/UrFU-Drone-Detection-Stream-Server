from .client import YandexGeocodeClientAPI

from src.shared.configs import PROJECT_SETTINGS


yandex_geocode_map_client_api = YandexGeocodeClientAPI(
    api_key=PROJECT_SETTINGS.yandex_map.geocode_api_key
)
