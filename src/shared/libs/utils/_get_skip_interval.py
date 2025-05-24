def get_skip_interval(input_fps: int, output_fps: int) -> int:
    """_summary_

    Args:
        input_fps (float): _description_
        output_fps (float): _description_

    Returns:
        int: _description_
    """
    if output_fps >= input_fps:
        return 0  # Пропускать не нужно

    keep_ratio = output_fps / input_fps
    skip_every = round(1 / (1 - keep_ratio))

    return skip_every
