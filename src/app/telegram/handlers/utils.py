from src.shared.api.yandex.suggest_map import yandex_suggest_map_client_api


async def list_potential_targets_message(
    longitude: float,
    latitude: float,
    cruising_speed: float,
) -> str:

    yandex_map_results = (
        await yandex_suggest_map_client_api.set_ll(
            longitude,
            latitude,
        )
        .set_attrs()
        .send("Производственное предприятие")
    )

    message = "Список потенциальных целей:"

    yandex_map_results = sorted(
        yandex_map_results,
        key=lambda yandex_map_result: yandex_map_result.distance.value,
    )

    for i, yandex_map_result in enumerate(yandex_map_results, start=1):
        distance_str = yandex_map_result.distance.text
        distance_value = yandex_map_result.distance.value
        minute = ((distance_value / 1000) / cruising_speed) * 60
        message += f"\n{i}) <b>{distance_str} ({minute:.2f} мин.)</b>: {yandex_map_result.title}"

    return message
