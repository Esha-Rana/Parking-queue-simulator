from datetime import datetime
from typing import Optional, List, Dict, Tuple


class ParkingLot:
    def __init__(self, lot_id: str, max_size: int = 5):
        self.lot_id = lot_id
        self.max_size = max_size
        self.parking: List[Optional[Dict]] = [None] * max_size
        self.parked_cars = set()
    
    def can_park(self, car_number: str) -> Tuple[bool, str]:
        if car_number in self.parked_cars:
            return False, f"Car {car_number} already parked!"
        
        if self._has_empty_slot():
            return True, "Can park"
        
        return False, f"Lot {self.lot_id} is full!"
    
    def park(self, car_number: str) -> Tuple[bool, str]:
        car_number = car_number.strip().upper()
        
        if not car_number:
            return False, "Car number cannot be empty!"
        
        if car_number in self.parked_cars:
            return False, f"Car {car_number} already parked!"
        
        for i in range(self.max_size):
            if self.parking[i] is None:
                self.parking[i] = {
                    "car_number": car_number,
                    "entry_time": datetime.now()
                }
                self.parked_cars.add(car_number)
                return True, f"Car {car_number} parked at Lot {self.lot_id}, Slot {i+1}"
        
        return False, f"Lot {self.lot_id} is full!"
    
    def get_next_empty_slot(self) -> Optional[int]:
        for i in range(self.max_size):
            if self.parking[i] is None:
                return i
        return None
    
    def remove_first(self) -> Tuple[bool, Optional[str], Optional[int]]:
        for i in range(self.max_size):
            if self.parking[i] is not None:
                car_number = self.parking[i]["car_number"]
                self.parking[i] = None
                self.parked_cars.remove(car_number)
                return True, car_number, i
        return False, None, None
    
    def remove_specific(self, car_number: str) -> Tuple[bool, str]:
        if self.is_empty():
            return False, "Parking is empty!"
        
        for i in range(self.max_size):
            if self.parking[i] is not None and self.parking[i]["car_number"] == car_number:
                self.parking[i] = None
                self.parked_cars.remove(car_number)
                return True, f"Car {car_number} removed successfully!"
        
        return False, f"Car {car_number} not found!"
    
    def get_status(self) -> List[Optional[Dict]]:
        return self.parking
    
    def get_parking_status(self) -> List[Optional[str]]:
        return [
            slot["car_number"] if slot is not None else None
            for slot in self.parking
        ]
    
    def get_first_car(self) -> Optional[str]:
        for slot in self.parking:
            if slot is not None:
                return slot["car_number"]
        return None
    
    def get_occupancy(self) -> Tuple[int, int]:
        occupied = sum(1 for slot in self.parking if slot is not None)
        return occupied, self.max_size
    
    def is_full(self) -> bool:
        return all(slot is not None for slot in self.parking)
    
    def is_empty(self) -> bool:
        return all(slot is None for slot in self.parking)
    
    def _has_empty_slot(self) -> bool:
        return any(slot is None for slot in self.parking)