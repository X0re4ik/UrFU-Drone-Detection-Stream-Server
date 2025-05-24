import os
import torch
import logging
import logging.config
from pathlib import Path
from ._settings import Settings
from .logger_config import get_logger
from ._mode import mode

PROJECT_SETTINGS = Settings()
_logger_config = get_logger(PROJECT_SETTINGS.app.logger_level)
logging.config.dictConfig(_logger_config)

logger = logging.getLogger(__name__)


ROOT_PATH = Path(__file__).parent.parent.parent

ROOT_DATA = ROOT_PATH / "app" / "data"


logger.info(f"APP Develop: {mode(PROJECT_SETTINGS.app.develop)}")
logger.info(f"APP Root Path: {ROOT_PATH}")
logger.info(f"APP Device: {PROJECT_SETTINGS.app.device}")

logger.info(f"RTSP Stream Input: {PROJECT_SETTINGS.rtsp_stream.input_url}")
logger.info(f"RTSP Stream Output: {PROJECT_SETTINGS.rtsp_stream.output_url}")
logger.info(f"RTSP Stream FPS: {PROJECT_SETTINGS.rtsp_stream.output_fps}")


TRACKER_PATH = ROOT_DATA / "tracker" / "byte_tracker.yaml"
YOLO_DETECTION_PATH = ROOT_DATA / "yolo" / "10-05_22_16_best.pt"
MOBILE_NET_CLASSIFICATION_PATH = ROOT_DATA / "mobile_net" / "best.pth"

for path_ in [TRACKER_PATH, YOLO_DETECTION_PATH, MOBILE_NET_CLASSIFICATION_PATH]:
    if not os.path.exists(path_):
        raise FileNotFoundError(path_)
    logger.info(f"Model Path Exists ({path_})")
