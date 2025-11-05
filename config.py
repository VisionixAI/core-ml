import cv2

# --- Model & Video Config ---
MODEL_NAME = 'yolov8n-face.pt'  # Nano model - fast
VIDEO_SOURCE = 0          # 0 for webcam, or "path/to/video.mp4"
PERSON_CLASS_ID = 0       # 'person' class ID

# --- Grid & Automation Config ---
GRID_ROWS = 4             # MODIFIED: Was 3
GRID_COLS = 4             # MODIFIED: Was 3
DELAY_SECONDS = 15        # 15-second delay for all actions

# --- VISUALIZATION COLORS (BGR) ---
GRID_LINE_COLOR = (0, 255, 0)   # Green
BOX_COLOR = (255, 0, 0)    # Blue
TEXT_COLOR = (255, 255, 255) # White

# Grid cell state colors
STATE_COLORS = {
    "OFF": (70, 70, 70),       # Dark Gray
    "ON": (0, 255, 0),         # Bright Green
    "PENDING_ON": (0, 255, 255), # Yellow
    "PENDING_OFF": (0, 165, 255) # Orange
}

# --- FONT ---
FONT = cv2.FONT_HERSHEY_SIMPLEX