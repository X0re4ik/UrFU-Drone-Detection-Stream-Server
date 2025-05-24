import cv2


def cv_end() -> bool:
    return cv2.waitKey(1) & 0xFF == ord("q")
