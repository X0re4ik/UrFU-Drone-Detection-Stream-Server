from typing import Any
from src.shared.typing import CVFrameType
from PIL import Image

import cv2
import torch
from torchvision import transforms
from PIL import Image
import numpy as np
import torch.nn.functional as F


from .dto import ClassificationInfoDTO


class ClassificationObject:

    def __init__(self, transform: transforms.Compose, model: Any):
        self._transform = transform
        self._model = model

    def get_class(self, frame: CVFrameType) -> ClassificationInfoDTO:

        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        input_tensor = self._transform(pil_image).unsqueeze(0)

        with torch.no_grad():
            logits = self._model(input_tensor)
            probs = F.softmax(logits, dim=1)
            confidence, predicted_class = torch.max(probs, dim=1)
        confidence = float(confidence.item())
        predicted_class = int(predicted_class.item())
        return ClassificationInfoDTO(confidence, predicted_class)
