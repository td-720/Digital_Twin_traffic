# import time
# import requests
# from core import TrafficSimulator, TrafficProcessor

# API_ENDPOINT = "http://localhost:5000/api/record"

# def run_pipeline():
#     # Utilizing the exact image assets associated with this session
#     simulator = TrafficSimulator(
#         locations=["FAE Building", "Main Gate", "Campus Highway"],
#         images=["5153021902783349740.jpeg", "18236068827845723118.jpeg"] 
#     )
#     processor = TrafficProcessor(speed_limit=60)

#     print("Starting Traffic Digital Twin Pipeline...")
    
#     try:
#         while True:
#             # Generate and process
#             raw_vehicle = simulator.generate_vehicle()
#             processed_record = processor.process(raw_vehicle)
            
#             # Transmit to API
#             try:
#                 response = requests.post(API_ENDPOINT, json=processed_record)
#                 print(f"[{processed_record['timestamp']}] {processed_record['plate']} | {processed_record['speed']}km/h -> {processed_record['status']}")
#             except requests.exceptions.ConnectionError:
#                 print("Failed to connect to Flask API. Is it running?")

#             time.sleep(0.5)
            
#     except KeyboardInterrupt:
#         print("\nPipeline stopped.")

# if __name__ == "__main__":
#     run_pipeline()































































import time
import requests
import os
from core import TrafficSimulator, TrafficProcessor

API_ENDPOINT = "http://localhost:5000/api/record"
IMAGES_DIR = "images"

def get_available_images() -> list:
    """Dynamically fetches all valid image filenames from the images directory."""
    # Safety check: Create the folder if it doesn't exist to prevent crashes
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        print(f"⚠️ Created '{IMAGES_DIR}' directory. Please add some images!")
        return []
        
    valid_extensions = ('.jpg', '.jpeg', '.png')
    
    # List files in the directory and filter out hidden/non-image files
    images = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(valid_extensions)]
    return images

def run_pipeline():
    images_list = get_available_images()
    
    # Fail fast if there is no data to simulate with
    if not images_list:
        print("❌ Error: No valid images found in the 'images' folder.")
        print("Please add some .jpg, .jpeg, or .png files and try again.")
        return

    simulator = TrafficSimulator(
        locations=["FAE Building", "Main Gate", "Campus Highway"],
        images=images_list  # Now dynamically populated!
    )
    processor = TrafficProcessor(speed_limit=60)

    print(f"✅ Found {len(images_list)} image(s).")
    print("Starting Traffic Digital Twin Pipeline...")
    
    try:
        while True:
            # 1. Generate and Process
            raw_vehicle = simulator.generate_vehicle()
            processed_record = processor.process(raw_vehicle)
            
            # 2. Transmit
            try:
                response = requests.post(API_ENDPOINT, json=processed_record)
                print(f"[{processed_record['timestamp']}] {processed_record['plate']} | {processed_record['speed']}km/h -> {processed_record['status']}")
            except requests.exceptions.ConnectionError:
                print("Failed to connect to Flask API. Is it running?")

            # 3. Wait
            time.sleep(3.0)
            
    except KeyboardInterrupt:
        print("\nPipeline stopped.")

if __name__ == "__main__":
    run_pipeline()