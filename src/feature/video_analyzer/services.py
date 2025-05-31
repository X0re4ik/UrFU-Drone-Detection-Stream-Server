import io
from typing import Literal
import cv2
import time


from dataclasses import dataclass
from typing import Literal, List, Dict
from collections import defaultdict
import torch
import numpy as np
import matplotlib.pyplot as plt


import numpy as np

from src.entities.dto.drone_detection_result import DroneDetectionResultDTO

from collections import defaultdict

from src.shared.libs.utils import generate_timestamps_hhmmss


class VideoAnalyzerService:
    def __init__(self, fps: float, min_valid_duration: int = 30):
        self._fps = fps
        self._min_valid_duration = min_valid_duration

        self._drone_detection_statistics: dict[int, list[DroneDetectionResultDTO]] = (
            defaultdict(list)
        )
        self._empty_frames = set()
        self._count_drones: dict[int, int] = defaultdict(int)
        self._drone_type_frame_counts: dict[str, int] = defaultdict(int)

        self._count_frames = 0

    def update(
        self,
        frame_id: int,
        drone_detection_result: (
            list[DroneDetectionResultDTO] | DroneDetectionResultDTO | None
        ) = None,
    ) -> None:
        self._count_frames = max(frame_id, self._count_frames)
        if drone_detection_result is None:
            self._empty_frames.add(frame_id)
            self._count_drones[0] += 1
            return

        if isinstance(drone_detection_result, list):
            self._drone_detection_statistics[frame_id].extend(drone_detection_result)
            num_detections = len(drone_detection_result)
            types_in_frame = set(d.drone_type for d in drone_detection_result)
        else:
            self._drone_detection_statistics[frame_id].append(drone_detection_result)
            num_detections = 1
            types_in_frame = {drone_detection_result.drone_type}

        self._count_drones[num_detections] += 1

        # Учитываем каждый тип только один раз за кадр (если в кадре 2 одинаковых дрона, всё равно +1)
        for t in types_in_frame:
            self._drone_type_frame_counts[t] += 1

    def get_count_drones(self) -> int:
        filtered = {
            count: duration
            for count, duration in self._count_drones.items()
            if duration >= self._min_valid_duration
        }
        if not filtered:
            return 0
        return max(filtered.items(), key=lambda x: x[1])[0]

    def get_frequent_drone_types(self) -> list[str]:
        """
        Возвращает список типов дронов, которые встречались чаще min_frames раз.
        Это исключает случайные ложные срабатывания.
        """
        return [
            drone_type
            for drone_type, count in self._drone_type_frame_counts.items()
            if count >= self._min_valid_duration
        ]

    def get_most_frequent_drone_type(self) -> str | None:
        """Возвращает тип дрона, который встречался чаще всего (с учётом фильтрации)"""
        if not self._drone_type_frame_counts:
            return None
        return max(self._drone_type_frame_counts.items(), key=lambda x: x[1])[0]

    def report(self) -> plt.Figure:
        time_lines: list[str] = generate_timestamps_hhmmss(
            self._count_frames + 1, self._fps
        )

        # --- Подготовка данных ---
        drone_counts = np.zeros(self._count_frames + 1)
        drone_confidences = np.zeros(self._count_frames + 1)
        type_confidences = np.zeros(self._count_frames + 1)
        type_counter = defaultdict(int)

        for frame_id in range(self._count_frames + 1):
            detections = self._drone_detection_statistics.get(frame_id, [])
            drone_counts[frame_id] = len(detections)
            if detections:
                drone_confidences[frame_id] = np.mean(
                    [d.drone_confidence for d in detections]
                )
                type_confidences[frame_id] = np.mean(
                    [d.type_confidence for d in detections]
                )
                for d in detections:
                    type_counter[d.drone_type] += 1

        # --- Построение графиков ---
        fig, axs = plt.subplots(2, 2, figsize=(20, 10))
        fig.suptitle("Анализ дронов по видеопотоку", fontsize=16)

        # 1. Количество дронов по времени
        axs[0, 0].plot(drone_counts, label="Количество дронов", color="royalblue")
        axs[0, 0].set_title("Количество дронов по времени")
        axs[0, 0].set_xlabel("Время")
        axs[0, 0].set_ylabel("Число дронов")
        axs[0, 0].set_xticks(np.linspace(0, self._count_frames, 10, dtype=int))
        axs[0, 0].set_xticklabels(
            time_lines[np.linspace(0, self._count_frames, 10, dtype=int)], rotation=45
        )
        axs[0, 0].grid(True)
        axs[0, 0].legend()

        # 2. Круговая диаграмма типов дронов
        axs[0, 1].pie(
            type_counter.values(),
            labels=type_counter.keys(),
            autopct="%1.1f%%",
            startangle=140,
        )
        axs[0, 1].set_title("Распределение типов дронов")

        # 3. Уверенность в том, что это дрон
        axs[1, 0].plot(drone_confidences, label="Уверенность (дрон)", color="green")
        axs[1, 0].set_title("Уверенность в том, что это дрон")
        axs[1, 0].set_xlabel("Время")
        axs[1, 0].set_ylabel("Уверенность (0–1)")
        axs[1, 0].set_xticks(np.linspace(0, self._count_frames, 10, dtype=int))
        axs[1, 0].set_xticklabels(
            time_lines[np.linspace(0, self._count_frames, 10, dtype=int)], rotation=45
        )
        axs[1, 0].set_ylim(0, 1)
        axs[1, 0].grid(True)
        axs[1, 0].legend()

        # 4. Уверенность в типе дрона
        axs[1, 1].plot(
            type_confidences, label="Уверенность (тип дрона)", color="orange"
        )
        axs[1, 1].set_title("Уверенность в типе дрона")
        axs[1, 1].set_xlabel("Время")
        axs[1, 1].set_ylabel("Уверенность (0–1)")
        axs[1, 1].set_xticks(np.linspace(0, self._count_frames, 10, dtype=int))
        axs[1, 1].set_xticklabels(
            time_lines[np.linspace(0, self._count_frames, 10, dtype=int)], rotation=45
        )
        axs[1, 1].set_ylim(0, 1)
        axs[1, 1].grid(True)
        axs[1, 1].legend()

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        #plt.show()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        
        return buf
