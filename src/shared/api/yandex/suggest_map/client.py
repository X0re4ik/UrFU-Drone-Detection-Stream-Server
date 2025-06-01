import aiohttp
import asyncio


from .dto import YandexMapResultDTO, YandexMapDistanceDTO


class YandexSuggestMapsClientAPI:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://suggest-maps.yandex.ru/v1/suggest",
    ):
        self._api_key = api_key
        self._base_url = base_url
        self._params = {
            "apikey": self._api_key,
        }

    def set_ll(self, lon: float, lat: float):
        self._params["ll"] = f"{lon},{lat}"
        return self

    def set_results(self, count: int):
        self._params["results"] = str(count)
        return self

    def set_attrs(self):
        self._params["attrs"] = "uri"
        return self

    async def send(self, text: str) -> list[YandexMapResultDTO]:
        params = self._params.copy()
        params["text"] = text

        async with aiohttp.ClientSession() as session:
            async with session.get(self._base_url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Request failed with status {response.status}")

                json_data = await response.json()
                results = json_data.get("results", [])

                return [
                    YandexMapResultDTO(
                        title=item["title"]["text"],
                        distance=YandexMapDistanceDTO(
                            value=item["distance"]["value"],
                            text=item["distance"]["text"],
                        ),
                    )
                    for item in results
                    if "distance" in item
                ]
