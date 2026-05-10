import random
from datetime import datetime

class TrafficSimulator:
    def __init__(self, locations: list, images: list):
        self.locations = locations
        self.images = images

    def generate_vehicle(self) -> dict:
        return {
            "plate": f"ABC{random.randint(100, 999)}",
            "speed": random.randint(20, 120),
            "location": random.choice(self.locations),
            "image": random.choice(self.images),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

class TrafficProcessor:
    def __init__(self, speed_limit: int = 60):
        self.speed_limit = speed_limit

    def process(self, vehicle_data: dict) -> dict:
        record = vehicle_data.copy()
        record["speed_limit"] = self.speed_limit
        
        if record["speed"] > self.speed_limit:
            record["status"] = "VIOLATION"
        else:
            record["status"] = "OK"
            
        return record