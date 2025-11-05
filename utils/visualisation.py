import cv2
from config import (
    GRID_LINE_COLOR, BOX_COLOR, TEXT_COLOR, STATE_COLORS, 
    FONT, GRID_ROWS, GRID_COLS
)

def draw_grid_lines(frame, cell_width, cell_height):
    """Draws the grid lines on the frame."""
    frame_height, frame_width, _ = frame.shape
    for i in range(1, GRID_COLS):
        x = i * cell_width
        cv2.line(frame, (x, 0), (x, frame_height), GRID_LINE_COLOR, 1)
    for i in range(1, GRID_ROWS):
        y = i * cell_height
        cv2.line(frame, (0, y), (frame_width, y), GRID_LINE_COLOR, 1)

def draw_grid_states(frame, grid_manager):
    """Draws the coordinates and appliance state on each grid cell."""
    for r in range(grid_manager.grid_rows):
        for c in range(grid_manager.grid_cols):
            cell_state = grid_manager.grid_states[(r, c)]
            appliance_status = cell_state["appliance"]
            color = STATE_COLORS.get(appliance_status, TEXT_COLOR)
            
            text1 = f"Grid: ({r},{c})"
            text2 = f"State: {appliance_status}"
            
            pos1_x = c * grid_manager.cell_width + 10
            pos1_y = r * grid_manager.cell_height + 20
            pos2_y = pos1_y + 20
            
            cv2.putText(frame, text1, (pos1_x, pos1_y), FONT, 0.5, color, 2)
            cv2.putText(frame, text2, (pos1_x, pos2_y), FONT, 0.5, color, 2)

def draw_person(frame, box, track_id, grid_coord):
    """Draws a single person's box, ID, and grid location."""
    x1, y1, x2, y2 = box
    cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, 2)
    
    text = f"ID: {track_id} -> G:({grid_coord[0]},{grid_coord[1]})"
    cv2.putText(frame, text, (x1, y1 - 10), FONT, 0.6, TEXT_COLOR, 2)