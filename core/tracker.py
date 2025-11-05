import os
import requests
from ultralytics import YOLO
from config import MODEL_NAME

# --- MODIFIED: This is the new, working download URL ---
MODEL_URL = f"https://github.com/YapaLab/yolo-face/raw/main/{MODEL_NAME}"

# --- Build a reliable path to where the model should be ---
current_file_path = os.path.abspath(__file__)
core_dir = os.path.dirname(current_file_path)
visionix_dir = os.path.dirname(core_dir)
MODEL_PATH = os.path.join(visionix_dir, MODEL_NAME) # e.g., C:\...\visionix\yolov8n-face.pt


def download_model():
    """Downloads the model file from the URL to the MODEL_PATH."""
    print(f"--- INFO: Model file not found at '{MODEL_PATH}' ---")
    print(f"Downloading '{MODEL_NAME}' from {MODEL_URL}...")
    
    try:
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status() 

        with open(MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"--- SUCCESS: Model downloaded to {MODEL_PATH} ---")
        
    except Exception as e:
        print(f"--- FATAL ERROR: AUTOMATIC DOWNLOAD FAILED ---")
        print(f"Error: {e}")
        print("\nPLEASE CHECK YOUR INTERNET CONNECTION.")
        print(f"-------------------------------------------------")
        exit()
# --- End of added code ---


class PersonTracker:
    def __init__(self):
        """Initializes the YOLOv8 model."""
        
        # Check if file exists, if not, download it
        if not os.path.exists(MODEL_PATH):
            download_model() # Call our new download function
        
        # Now we know the file exists (or the program exited)
        print(f"--- INFO: Loading model from '{MODEL_PATH}' ---")
        self.model = YOLO(MODEL_PATH)
        print("--- INFO: Model loaded successfully. ---")
            
    def process_frame(self, frame):
        """
        Runs the YOLOv8 tracking on a single frame.
        Returns extracted boxes and track IDs.
        """
        results = self.model.track(frame, persist=True, verbose=False)

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            return boxes, track_ids
        
        return None, None