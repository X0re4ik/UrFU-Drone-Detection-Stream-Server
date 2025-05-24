import cv2
import numpy as np


DEFAULT_COLOR = (0, 0, 255)


def draw_set_text(frame, x, y, label: str, color=DEFAULT_COLOR):
    cv2.putText(
        frame,
        f"{label}",
        (x, y - 10),
        cv2.FONT_HERSHEY_COMPLEX,
        0.3,
        color,
        1,
    )


def draw_rectangle(frame, xmin, ymin, xmax, ymax, color=DEFAULT_COLOR):
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)


def draw_track(frame, points, color=DEFAULT_COLOR):
    cv2.polylines(
        frame,
        np.array([points]),
        isClosed=False,
        color=color,
        thickness=1,
        lineType=cv2.LINE_8,
        shift=0,
    )
