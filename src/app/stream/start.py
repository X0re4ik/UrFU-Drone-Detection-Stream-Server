import logging
import cv2
from src.shared.api.logger import Logger
from src.shared.libs.utils._draw import draw_rectangle, draw_set_text, draw_track
from src.feature.send_to_rtsp.service import SenderToRTSPStream
from src.feature.rtsp_stream import RTSPStream


from src.shared.libs.cv2 import destroyAllWindows, cv_end

from src.app.init import CLASS_MAPPER

from src.shared.configs import PROJECT_SETTINGS, ROOT_PATH
from src.feature.detection_object import DetectionInfoDTO, DetectionObjectsFactory
from src.shared.libs.utils import get_skip_interval


from src.app.init import (
    detection_service,
    CLASS_MAPPER,
    classification_service,
    MODEL_MAPPER,
)


logger = Logger

# test_path = ROOT_PATH / "examples" / "rows" / "4.mp4"

stream = RTSPStream(PROJECT_SETTINGS.rtsp_stream.input_url)


input_stream_fps = stream.fps()
input_stream_size = stream.size()

output_stream_fps = PROJECT_SETTINGS.rtsp_stream.output_fps


logger.info(f"Input Frame FPS: {input_stream_fps}")
logger.info(f"Input Frame Size: {input_stream_size[0]}x{input_stream_size[1]}")

skip_frame = get_skip_interval(
    input_stream_fps,
    output_stream_fps,
)


rtsp_sender = SenderToRTSPStream(
    PROJECT_SETTINGS.rtsp_stream.output_url,
    input_stream_size,
    output_stream_fps,
)

logger.info(f"Output Frame FPS: {output_stream_fps}")
logger.info(f"Output Frame Size: {input_stream_size[0]}x{input_stream_size[1]}")
logger.info(f"Output Frame Skip: {skip_frame}")


while stream.is_open():
    if not stream.update():
        logger.error("Не могу обновить поток")
        break

    frame = stream.get_frame_with_skip_every(skip_frame)

    if frame is None:
        logger.debug("Не могу получить Frame")
        continue

    # detections_bbox = detection_service.detect(frame)

    # for detection_bbox in detections_bbox:
    #     xmin, ymin, xmax, ymax = detection_bbox.bbox
    #     confidence: float = detection_bbox.confidence
    #     class_id: int = detection_bbox.class_id
    #     track_id: int = detection_bbox.track_id

    #     points = detection_service.get_tracker_points(track_id)

    #     draw_set_text(
    #         frame,
    #         xmin,
    #         ymin - 10,
    #         f"Track: {track_id} | Class ID: {CLASS_MAPPER[class_id]} | Conf: {confidence:.2f}",
    #     )
    #     draw_rectangle(frame, xmin, ymin, xmax, ymax)
    #     draw_track(frame, points)

    #     if class_id == 0:
    #         cropped = frame[ymin:ymax, xmin:xmax]
    #         if cropped.size == 0:
    #             continue

    #         classification = classification_service.get_class(cropped)

    #         draw_set_text(
    #             frame,
    #             xmin,
    #             ymax + 10,
    #             f"Model: {MODEL_MAPPER[classification.model_id]} | {classification.confidence:.2f}",
    #         )

    logger.info(stream.get_frame_id() / output_stream_fps)
    rtsp_sender.send_to_rtsp(frame)

    if PROJECT_SETTINGS.app.develop:
        # cv2.imshow("Test Frame", frame)
        pass

    if cv_end():
        break

stream.stop()
destroyAllWindows()
