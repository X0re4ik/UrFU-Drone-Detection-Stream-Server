def get_current_time(
    processed_frame_id: int,
    input_fps: float,
    skip_ratio: int,
) -> float:
    """
    Вычисляет текущее время видео по номеру обработанного кадра.

    :param processed_frame_id: Номер кадра, который ты реально обработал.
    :param input_fps: Частота кадров исходного видео.
    :param skip_ratio: Количество кадров, которые ты пропускаешь между обработанными.
                       Например, если обрабатываешь каждый 3-й кадр, skip_ratio = 2.
    :return: Текущее время в секундах.
    """
    real_frame_id = processed_frame_id * (skip_ratio + 1)
    return real_frame_id / input_fps
