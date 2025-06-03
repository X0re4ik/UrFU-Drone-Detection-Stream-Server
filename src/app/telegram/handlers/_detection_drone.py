from aiogram import Bot
import asyncio
from src.feature.get_drone_type_info import get_drone_type_info_service, to_message
from src.app.video.analyzer.di import start_video_analyzer
from src.shared.libs.utils._generate_task_id import generate_task_id
from src.shared.api.logger import Logger
from src.shared.api.save_video_info import save_video_info_api

from aiogram.enums.parse_mode import ParseMode
from aiogram import Bot, Dispatcher, types

from .utils import list_potential_targets_message


from src.shared.api.yandex.geocode_map import yandex_geocode_map_client_api

logger = Logger


async def detection_drone_handler(
    user_bot: Bot,
    service_bot: Bot,
    target_chat_id: int,
    file_id: int,
    latitude: float,
    longitude: float,
):

    pos = await yandex_geocode_map_client_api.reverse_geocode(latitude, longitude)

    message = await service_bot.send_message(
        chat_id=target_chat_id,
        text=f"❗ВНИМАНИЕ❗\nГраждане сообщают об атаке БПЛА по адресу {pos}",
    )

    video_file = await user_bot.get_file(file_id)
    video_bytes = await user_bot.download_file(video_file.file_path)

    task_id = generate_task_id()
    logger.info(f"Зарегестрирована задача: {task_id}")

    video_name = task_id + ".md4"
    report_name = task_id + ".png"

    save_video_info_api.save_row_video(video_name, video_bytes)

    video_result = start_video_analyzer(task_id)

    logger.info(
        f"Обнаружено {video_result.count_drones} дронов следующих типов {video_result.model_types}"
    )

    processed_video = save_video_info_api.get_processed_video(video_name)
    report_file = save_video_info_api.get_report(report_name)

    await service_bot.send_video(
        chat_id=target_chat_id,
        video=types.BufferedInputFile(
            file=processed_video.getvalue(), filename=video_name
        ),
        caption="Обработанное видео 📹: ",
        reply_to_message_id=message.message_id,
    )

    await service_bot.send_photo(
        chat_id=target_chat_id,
        photo=types.BufferedInputFile(report_file.getvalue(), filename=report_name),
        caption="Статистика 📊: ",
        reply_to_message_id=message.message_id,
    )

    if video_result.count_drones == 0:
        return await service_bot.send_message(
            chat_id=target_chat_id,
            text="Дрон не обнаружен",
            reply_to_message_id=message.message_id,
        )

    await service_bot.send_message(
        chat_id=target_chat_id,
        text=f"Количество дронов: {video_result.count_drones}\nМодели дронов {'; '.join(video_result.model_types)}",
        reply_to_message_id=message.message_id,
    )

    async def _send_drone_types(model_type: str):
        drone_data_info = get_drone_type_info_service.get_drone_type_info(model_type)
        if drone_data_info is None:
            logger.error("")
            return

        await service_bot.send_photo(
            chat_id=target_chat_id,
            photo=types.BufferedInputFile(
                drone_data_info.photo, filename=f"{drone_data_info.model_name}.png"
            ),
            caption=to_message(drone_data_info),
            reply_to_message_id=message.message_id,
            parse_mode=ParseMode.HTML,
        )

    await asyncio.gather(
        *[_send_drone_types(model_type) for model_type in video_result.model_types]
    )

    drone_data_info = get_drone_type_info_service.get_drone_type_info(
        video_result.model_types[0]
    )

    _message = await list_potential_targets_message(
        longitude, latitude, drone_data_info.cruising_speed
    )
    await service_bot.send_message(
        chat_id=target_chat_id,
        text=_message,
        reply_to_message_id=message.message_id,
        parse_mode=ParseMode.HTML,
    )
