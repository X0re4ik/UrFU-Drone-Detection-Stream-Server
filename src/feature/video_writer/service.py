import io
import cv2

from src.shared.typing import CVFrameType


class VideoWriterService:

    def __init__(self, task_id: str, fps: int, width: int, height: int, template_path = "/tmp/drones/processed"):
        self._fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        self._file_path: str = f"{template_path}/{task_id}.mp4"

        self._out = cv2.VideoWriter(
            self._file_path,
            self._fourcc,
            fps,
            (
                width,
                height,
            ),
        )

        self._is_close = False

    def write(self, frame: CVFrameType) -> None:
        self._out.write(frame)

    def close(self):
        self._is_close = True
        self._out.release()

    def get_file(self) -> io.BytesIO:

        if not self._is_close:
            raise Exception()

        with open(self._file_path, "rb") as f:
            file_bytes = f.read()

        return io.BytesIO(file_bytes)
