from src.feature.rtsp_stream import RTSPStreamFactory
from src.feature.video_writer import VideoWriterServiceFactory
from src.feature.video_analyzer.services import VideoAnalyzerService
from .start import TelegramBotDroneDetectionApp


from src.app.init import detection_service, classification_service

from .dto import DroneDetectionVideoInfoDTO

def start_video_analyzer(task_id: str) -> DroneDetectionVideoInfoDTO:
    stream = RTSPStreamFactory.create_from_s3(task_id + ".md4")
    return TelegramBotDroneDetectionApp(
        detection_service,
        classification_service,
        VideoAnalyzerService(stream.fps()),
        VideoWriterServiceFactory.create(task_id, stream.fps(), stream.size()),
        task_id,
    ).detect_from_stream(stream)
