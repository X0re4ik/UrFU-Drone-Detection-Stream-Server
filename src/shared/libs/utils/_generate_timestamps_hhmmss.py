import numpy as np


def generate_timestamps_hhmmss(num_frames: int, fps: float) -> np.ndarray:
    seconds_total = np.arange(num_frames) / fps
    hours = (seconds_total // 3600).astype(int)
    minutes = ((seconds_total % 3600) // 60).astype(int)
    seconds = (seconds_total % 60).astype(int)

    hh = np.char.zfill(hours.astype(str), 2)
    mm = np.char.zfill(minutes.astype(str), 2)
    ss = np.char.zfill(seconds.astype(str), 2)

    return np.char.add(np.char.add(hh, ":"), np.char.add(mm, ":") + ss)
