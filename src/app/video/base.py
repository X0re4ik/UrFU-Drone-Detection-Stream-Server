import cv2
import abc
from src.entities.dto.drone_detection_result import DroneDetectionResultDTO
from src.feature.detection_object.service import DetectionObjects
from src.shared.api.logger import Logger
from src.shared.libs.utils._draw import draw_rectangle, draw_set_text, draw_track
from src.feature.rtsp_stream import RTSPStream

from src.feature.classification_object import (
    ClassificationObject,
)


from src.shared.libs.cv2 import destroyAllWindows, cv_end

from src.app.init import CLASS_MAPPER

from src.shared.configs import PROJECT_SETTINGS


from src.app.init import (
    CLASS_MAPPER,
    MODEL_MAPPER,
)


from src.feature.rtsp_stream import RTSPStream

from src.shared.typing import CVFrameType

logger = Logger


class StreamDroneDetectionBaseApp:

    def __init__(
        self,
        detection_object_service: DetectionObjects,
        classification_object_service: ClassificationObject,
    ):
        self._detection_object_service = detection_object_service
        self._classification_object_service = classification_object_service

    def detect_from_stream(self, stream: RTSPStream):

        while stream.is_open():

            if not stream.update():
                logger.error("Не могу обновить поток")
                break

            frame = stream.get_frame()

            if frame is None:
                logger.debug("Не могу получить Frame")
                continue

            frame_id: int = stream.get_frame_id()

            objs: list[DroneDetectionResultDTO] = self._detection_drone(frame)

            if PROJECT_SETTINGS.app.use_show:
                cv2.imshow(f"Test Frame", frame)
                pass

            self.detection_callback(frame_id, frame, objs, len(objs) != 0)

            if cv_end():
                break

        stream.stop()
        destroyAllWindows()

        return self.after_processing_result_callback()

    def _detection_drone(self, frame: CVFrameType) -> list[DroneDetectionResultDTO]:
        detections_bbox = self._detection_object_service.detect(frame)

        results = []
        for detection_bbox in detections_bbox:
            xmin, ymin, xmax, ymax = detection_bbox.bbox
            class_id: int = detection_bbox.class_id
            track_id: int = detection_bbox.track_id

            points = self._detection_object_service.get_tracker_points(track_id)
            class_name = CLASS_MAPPER[class_id]

            if class_id == 0:
                cropped = frame[ymin:ymax, xmin:xmax]
                if cropped.size == 0:
                    continue

                classification = self._classification_object_service.get_class(cropped)
                model_name = MODEL_MAPPER[classification.model_id]
                draw_set_text(
                    frame,
                    xmin,
                    ymax + 10,
                    f"Model: {model_name} | {classification.confidence:.2f}",
                )
                results.append(
                    DroneDetectionResultDTO(
                        drone_type=model_name,
                        drone_confidence=detection_bbox.confidence,
                        type_confidence=classification.confidence,
                        bbox=[xmin, ymin, xmax, ymax],
                    )
                )
            draw_set_text(
                frame,
                xmin,
                ymin - 10,
                f"Track: {track_id} | Class ID: {class_name} | Conf: {detection_bbox.confidence:.2f}",
            )
            draw_rectangle(frame, xmin, ymin, xmax, ymax)
            draw_track(frame, points)
        return results

    @abc.abstractmethod
    def after_processing_result_callback(self):
        """_summary_

        Returns:
            _type_: _description_
        """

    @abc.abstractmethod
    def detection_callback(
        self,
        frame_id: int,
        frame: CVFrameType,
        detection_results: list[DroneDetectionResultDTO],
        find: bool,
    ) -> None:
        """_summary_

        Args:
            frame_id (int): _description_
            frame (CVFrameType): _description_
            detection_result (list[DroneDetectionResultDTO] | None): _description_
            find (bool): _description_
        """
