from src.feature.video_writer.service import VideoWriterService
from src.shared.api.logger import Logger

from src.feature.video_analyzer import VideoAnalyzerService
from src.app.video.base import StreamDroneDetectionBaseApp
from src.shared.api.save_video_info import save_video_info_api
from .dto import DroneDetectionVideoInfoDTO


logger = Logger


class TelegramBotDroneDetectionApp(StreamDroneDetectionBaseApp):

    def __init__(
        self,
        detection_object_service,
        classification_object_service,
        video_analyzer_service: VideoAnalyzerService,
        video_writer: VideoWriterService,
        task_id: str,
    ):
        super().__init__(detection_object_service, classification_object_service)

        self._video_analyzer_service = video_analyzer_service
        self._video_writer_service = video_writer

        self._task_id = task_id

    def detection_callback(self, frame_id, frame, detection_results, find):
        if not find:
            detection_results = None
        self._video_analyzer_service.update(frame_id, detection_results)
        self._video_writer_service.write(frame)

    def after_processing_result_callback(self):

        self._video_writer_service.close()

        count_drones: int = self._video_analyzer_service.get_count_drones()
        drone_types: list[str] = self._video_analyzer_service.get_frequent_drone_types()

        report_file = self._video_analyzer_service.report()
        video_file = self._video_writer_service.get_file()

        save_video_info_api.save_report(self._task_id + ".png", report_file)
        save_video_info_api.save_processed_video(self._task_id + ".md4", video_file)

        return DroneDetectionVideoInfoDTO(
            count_drones=count_drones, model_types=drone_types
        )
