import cv2
import sys
from config import VIDEO_SOURCE
from core.tracker import PersonTracker
from core.grid_manager import GridManager
from utils import visualisation as viz

def run_pipeline():
    # --- 1. INITIALIZATION ---
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print(f"Error: Could not open video source {VIDEO_SOURCE}")
        sys.exit()

    # Read one frame to get dimensions
    success, frame = cap.read()
    if not success:
        print("Error: Could not read first frame.")
        sys.exit()
    
    frame_height, frame_width, _ = frame.shape
    
    # Initialize our core components
    tracker = PersonTracker()
    grid_manager = GridManager(frame_width, frame_height)

    # --- 2. MAIN PROCESSING LOOP ---
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Video ended or frame read error.")
            break
        
        # This set will hold all grids occupied in *this* frame
        occupied_grids_this_frame = set()

        # --- 3. TRACKING ---
        boxes, track_ids = tracker.process_frame(frame)
        
        # --- 4. PROCESS DETECTIONS ---
        if track_ids is not None:
            for box, track_id in zip(boxes, track_ids):
                # Get person's location (bottom-center)
                x1, y1, x2, y2 = box
                person_location_x = (x1 + x2) // 2
                person_location_y = y2
                
                # Find which grid cell they are in
                grid_coord = grid_manager.get_grid_cell(person_location_x, person_location_y)
                
                # Mark this grid as occupied
                occupied_grids_this_frame.add(grid_coord)
                
                # Draw the person's box and info
                viz.draw_person(frame, box, track_id, grid_coord)

        # --- 5. UPDATE AUTOMATION STATE ---
        grid_manager.update_states(occupied_grids_this_frame)
        
        # --- 6. DRAW VISUALIZATIONS ---
        viz.draw_grid_lines(frame, grid_manager.cell_width, grid_manager.cell_height)
        viz.draw_grid_states(frame, grid_manager)
        
        # --- 7. DISPLAY FRAME ---
        cv2.imshow("Visionix Smart Grid", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Exiting...")
            break

    # --- 8. CLEANUP ---
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_pipeline()