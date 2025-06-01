from src.feature.rtsp_stream.service import RTSPStream
from src.shared.configs import ROOT_PATH
from src.feature.video_writer.service import VideoWriterService
from src.shared.api.logger import Logger

from src.feature.video_analyzer import VideoAnalyzerService
from src.app.video.base import StreamDroneDetectionBaseApp
from src.shared.api.save_video_info import save_video_info_api
from src.app.init import (
    detection_service,
    classification_service,
)

logger = Logger


class TestDroneDetectionApp(StreamDroneDetectionBaseApp):

    def __init__(
        self,
        detection_object_service,
        classification_object_service,
        video_writer: VideoWriterService,
    ):
        super().__init__(detection_object_service, classification_object_service)

        self._video_writer_service = video_writer

    def detection_callback(self, frame_id, frame, detection_results, find):
        self._video_writer_service.write(frame)

    def after_processing_result_callback(self):
        self._video_writer_service.close()


if __name__ == "__main__":
    VIDEO_NAME = "12"
    INPUT_VIDEO_URL = ROOT_PATH / "examples" / "rows-shorts" / f"{VIDEO_NAME}.mp4"
    logger.info(f"Начинаю демонстрацию видео {INPUT_VIDEO_URL}")
    OUTPUT_PATH = ROOT_PATH / "examples" / "outputs"

    stream = RTSPStream(INPUT_VIDEO_URL)

    TestDroneDetectionApp(
        detection_service,
        classification_service,
        VideoWriterService(
            VIDEO_NAME,
            stream.fps(),
            stream.size()[0],
            stream.size()[1],
            str(OUTPUT_PATH),
        ),
    ).detect_from_stream(stream)
