from .dto import DroneTypeInfoDTO


def to_message(drone_type_info: DroneTypeInfoDTO) -> str:
    return f"""
Атака ведется моделью: <b>{drone_type_info.model_name}</b>
1) Полезная нагрузка: {drone_type_info.maximum_payload} кг.
2) Максимальная скорость: {drone_type_info.maximum_speed} км/ч
3) Средняя скорость: {drone_type_info.cruising_speed} км/ч
4) Дальность связи: {drone_type_info.communication_range} км.
"""
