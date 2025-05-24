import cv2
import threading

from src.shared.typing import CVFrameType


class RTSPStream:
    """"""

    def __init__(self, rtsp_url: str):
        self.rtsp_url = rtsp_url
        self.cap = cv2.VideoCapture(self.rtsp_url)
        self.frame = None
        self._frame_id = 0
        self.running = True

    def is_open(self):
        return self.cap.isOpened()

    def fps(self):
        return int(self.cap.get(cv2.CAP_PROP_FPS))

    def size(self) -> tuple[int, int]:
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height

    def update(self) -> bool:
        """ """
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                return False
            self.frame = frame
            self._frame_id += 1
            return True

    def get_frame(self) -> CVFrameType | None:
        """_summary_

        Returns:
            CVFrameType | None: _description_
        """
        return self.frame.copy() if self.frame is not None else None

    def get_frame_id(self) -> int:
        return self._frame_id

    def get_frame_with_skip_every(self, skip_every: int = 5) -> CVFrameType | None:
        if skip_every < 1:
            return self.frame

        if self._frame_id % skip_every == 0:
            return self.frame
        return None

    def stop(self) -> None:
        """_summary_"""
        self.running = False
        self.cap.release()
