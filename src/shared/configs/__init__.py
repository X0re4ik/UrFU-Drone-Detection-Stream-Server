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
EXAMPLE_DATA = ROOT_PATH / "examples" / "rows"


logger.info(f"[APP] Develop: {mode(PROJECT_SETTINGS.app.develop)}")
logger.info(f"[APP] Use cv2.imcshow: {mode(PROJECT_SETTINGS.app.use_show)}")
logger.info(f"[APP] Root Path: {ROOT_PATH}")
logger.info(f"[APP] Device: {PROJECT_SETTINGS.app.device}")

logger.info(f"[RTSP] Stream Input: {PROJECT_SETTINGS.rtsp_stream.input_url}")
logger.info(f"[RTSP] Stream Output: {PROJECT_SETTINGS.rtsp_stream.output_url}")
logger.info(f"[RTSP] Stream FPS: {PROJECT_SETTINGS.rtsp_stream.output_fps}")


logger.info(f"[S3] Host: {PROJECT_SETTINGS.s3.host}")
logger.info(f"[S3] Port: {PROJECT_SETTINGS.s3.port}")
logger.info(
    f"[S3] Secret: {PROJECT_SETTINGS.s3.aws_access_key}-{PROJECT_SETTINGS.s3.aws_secret_key}"
)

logger.info(f"[YANDEX] [SUGGEST] Api Key: {PROJECT_SETTINGS.yandex_map.suggest_api_key}")
logger.info(f"[YANDEX] [GEOCODE] Api Key: {PROJECT_SETTINGS.yandex_map.geocode_api_key}")


TRACKER_PATH = ROOT_DATA / "tracker" / "byte_tracker.yaml"
YOLO_DETECTION_PATH = ROOT_DATA / "yolo" / "10-05_22_16_best.pt"
MOBILE_NET_CLASSIFICATION_PATH = ROOT_DATA / "mobile_net" / "17-05-25-resnet18_bpla_1.pth"

for path_ in [TRACKER_PATH, YOLO_DETECTION_PATH, MOBILE_NET_CLASSIFICATION_PATH]:
    if not os.path.exists(path_):
        raise FileNotFoundError(path_)
    logger.info(f"Model Path Exists ({path_})")

for path_ in ["rows", "reports", "processed"]:
    full_path_ = f"/tmp/drones/{path_}/"
    os.makedirs(full_path_, exist_ok=True)
    logger.info(f"Path created ({full_path_})")


logger.info("====" * 25 + "\n")
