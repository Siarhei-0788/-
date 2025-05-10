from dataclasses import dataclass

@dataclass
class Guest:
    id: int
    name: str
    phone: str
    email: str

@dataclass
class Room:
    id: int
    number: int
    type: str
    price: int
    status: str  # "available" / "occupied"

@dataclass
class Service:
    id: int
    name: str
    price: int

POPULARS = {
    "room_types": ["Одноместный", "Двухместный", "Люкс", "Апартаменты"],
    "hotel_services": ["Завтрак", "SPA-процедуры", "Трансфер", "Wi-Fi", "Парковка", "Рыбалка"],
    "years": [str(y) for y in range(2020, 2035)]  # Годы для бронирования
}

AUTHOR = "Пачко Сергей Александрович | АС-576"
