from collections import defaultdict


from typing import Any


import cv2
import torch
import numpy as np


import cv2
import numpy as np


from abc import ABC
import os
from collections import defaultdict


from ultralytics import YOLO

from src.shared.typing import CVFrameType

from .dto import DetectionInfoDTO


class DetectionObjects:

    def __init__(
        self,
        model: YOLO,
        tracker_yaml: str,
        conf: float = 0.4,
        verbose: bool = False,
    ):
        """_summary_

        Args:
            model (YOLO): _description_
            tracker_yaml (str): _description_
            conf (float, optional): _description_. Defaults to 0.4.
            verbose (bool, optional): _description_. Defaults to False.

        Raises:
            FileNotFoundError: _description_
        """

        self._model = model
        self._conf = conf
        self._tracker_yaml = tracker_yaml

        self._verbose = verbose

        if not os.path.exists(self._tracker_yaml):
            raise FileNotFoundError(self._tracker_yaml)

        self._tracker_history = defaultdict(list)

        self._max_tracker_detection = 1000
        
    
    def get_tracker_points(self, tracker_id: int):
        track = self._tracker_history[tracker_id]
        return np.hstack(track).astype(np.int32).reshape((-1, 1, 2))

    def detect(self, frame: CVFrameType) -> list[DetectionInfoDTO]:
        result = self._model.track(
            frame,
            persist=True,
            tracker=self._tracker_yaml,
            verbose=self._verbose,
        )[0]

        if not result.boxes or result.boxes.id is None:
            return []

        detections_results: list[DetectionInfoDTO] = []

        boxes = result.boxes.xywh.cpu()
        conf_s = result.boxes.conf.cpu()
        cls_s = result.boxes.cls.cpu()
        track_ids = result.boxes.id.int().cpu().tolist()

        for box, track_id, conf, cls in zip(boxes, track_ids, conf_s, cls_s):

            class_id = int(cls.item())
            conf = float(conf.item())

            if conf < self._conf:
                continue

            x, y, w, h = box
            track = self._tracker_history[track_id]
            track.append((float(x), float(y)))
            if len(track) > self._max_tracker_detection:
                track.pop(0)

            xmin, ymin, xmax, ymax = (
                int(x - w / 2),
                int(y - h / 2),
                int(x + w / 2),
                int(y + h / 2),
            )

            detections_results.append(
                DetectionInfoDTO([xmin, ymin, xmax, ymax], conf, class_id, track_id)
            )

        return detections_results
