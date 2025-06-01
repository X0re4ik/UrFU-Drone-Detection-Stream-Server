from datetime import datetime
import logging
import cv2
from src.shared.libs.utils._get_current_time import get_current_time
from src.feature.save_detection_info import DetectionSaverFactory, DroneDetectionInfoDTO
from src.shared.api.logger import Logger
from src.shared.libs.utils._draw import draw_rectangle, draw_set_text, draw_track
from src.feature.send_to_rtsp.service import SenderToRTSPStream
from src.feature.rtsp_stream import RTSPStream


from src.shared.libs.cv2 import destroyAllWindows, cv_end

from src.app.init import CLASS_MAPPER

from src.shared.configs import PROJECT_SETTINGS, ROOT_PATH
from src.feature.detection_object import DetectionInfoDTO, DetectionObjectsFactory
from src.shared.libs.utils import get_skip_interval
from src.app.video.base import StreamDroneDetectionBaseApp


from src.app.init import (
    detection_service,
    CLASS_MAPPER,
    classification_service,
    MODEL_MAPPER,
)


logger = Logger


INPUT_VIDEO_URL = (
    PROJECT_SETTINGS.rtsp_stream.input_url
)  # ROOT_PATH / "examples" / "rows" / "4.mp4"

stream = RTSPStream(INPUT_VIDEO_URL)


input_stream_fps = stream.fps()
input_stream_size = stream.size()

output_stream_fps = (
    PROJECT_SETTINGS.rtsp_stream.output_fps
    if PROJECT_SETTINGS.rtsp_stream.output_fps
    else input_stream_fps
)


logger.info(f"Input Frame FPS: {input_stream_fps}")
logger.info(f"Input Frame Size: {input_stream_size[0]}x{input_stream_size[1]}")

skip_frame = get_skip_interval(
    input_stream_fps,
    output_stream_fps,
)


logger.info(f"Output Frame FPS: {output_stream_fps}")
logger.info(f"Output Frame Size: {input_stream_size[0]}x{input_stream_size[1]}")
logger.info(f"Output Frame Skip: {skip_frame}")


rtsp_sender_service = SenderToRTSPStream(
    PROJECT_SETTINGS.rtsp_stream.output_url,
    input_stream_size,
    output_stream_fps,
)

detection_saver = DetectionSaverFactory.create()


class StreamDroneDetectionApp(StreamDroneDetectionBaseApp):

    def __init__(
        self,
        detection_object_service,
        classification_object_service,
        rtsp_sender_service: SenderToRTSPStream,
    ):
        super().__init__(detection_object_service, classification_object_service)

        self._rtsp_sender_service = rtsp_sender_service

    def detection_callback(self, frame_id, frame, detection_results, find):
        self._rtsp_sender_service.send_to_rtsp(frame)

        if find:
            logger.debug(f"Found in {frame_id}")

        for detection_result in detection_results:
            detection_saver.save(
                DroneDetectionInfoDTO(
                    model_type=detection_result.drone_type,
                    model_conf=detection_result.type_confidence,
                    bbox=detection_result.bbox,
                    timestamp=datetime.now(),
                )
            )


StreamDroneDetectionApp(
    detection_service, classification_service, rtsp_sender_service
).detect_from_stream(stream)
