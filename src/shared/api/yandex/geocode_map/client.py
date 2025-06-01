import aiohttp
import asyncio
from typing import Optional


class YandexGeocodeClientAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://geocode-maps.yandex.ru/v1/"

    async def reverse_geocode(self, lat: float, lon: float) -> Optional[str]:
        """
        Получает человекочитаемый адрес по координатам (широта, долгота).
        """
        params = {"apikey": self.api_key, "geocode": f"{lon},{lat}", "format": "json"}

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Ошибка запроса: {response.status}")
                data = await response.json()

                try:
                    feature_member = data["response"]["GeoObjectCollection"][
                        "featureMember"
                    ]
                    if not feature_member:
                        return None
                    return feature_member[0]["GeoObject"]["metaDataProperty"][
                        "GeocoderMetaData"
                    ]["Address"]["formatted"]
                except KeyError:
                    return None
