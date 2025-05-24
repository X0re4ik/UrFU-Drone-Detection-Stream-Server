import subprocess
from src.shared.typing import CVFrameType


from src.shared.configs import PROJECT_SETTINGS


LOG_FILE = open(PROJECT_SETTINGS.rtsp_stream.output_logger_file, "w")


class SenderToRTSPStream:

    def __init__(self, rtsp_url: str, new_size: tuple[int, int], fps: int):

        ffmpeg_write_rtsp_cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "bgr24",
            "-s",
            f"{new_size[0]}x{new_size[1]}",
            "-r",
            str(fps),
            "-i",
            "-",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-preset",
            "ultrafast",
            "-f",
            "flv",
            rtsp_url,
        ]

        self._process = subprocess.Popen(
            ffmpeg_write_rtsp_cmd,
            stdin=subprocess.PIPE,
            stdout=LOG_FILE,
            stderr=subprocess.STDOUT,
        )

    def send_to_rtsp(self, frame: CVFrameType) -> bool:
        self._process.stdin.write(frame.tobytes())
        return True
