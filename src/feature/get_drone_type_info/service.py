import os

import json

from src.shared.configs import ROOT_PATH

from .dto import DroneTypeInfoDTO

LOCAL_DB = {}

path_to_local_db = ROOT_PATH / "feature" / "get_drone_type_info" / "db" / "info.json"
image_to_local_db = ROOT_PATH / "feature" / "get_drone_type_info" / "db" / "images"

if not os.path.exists(path_to_local_db):
    raise FileNotFoundError(path_to_local_db)

if not os.path.isdir(image_to_local_db):
    raise FileNotFoundError(image_to_local_db)


with open(path_to_local_db, "r") as json_file:
    dict_data = json.loads(json_file.read())

for data in dict_data:

    path_to_image = os.path.join(image_to_local_db, data["photo"])

    with open(path_to_image, "rb") as photo:
        LOCAL_DB[data["modelName"]] = DroneTypeInfoDTO(
            model_name=data["modelName"],
            maximum_payload=data["maximumPayload"],
            maximum_speed=data["maximumSpeed"],
            cruising_speed=data["cruisingSpeed"],
            communication_range=data["communicationRange"],
            photo=photo.read(),
        )


class GetDroneTypeInfoService:

    def get_drone_type_info(self, drone_type_name: str) -> DroneTypeInfoDTO:
        return LOCAL_DB.get(drone_type_name, None)
