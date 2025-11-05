import time
from config import GRID_ROWS, GRID_COLS, DELAY_SECONDS

class GridManager:
    def __init__(self, frame_width, frame_height):
        """Initializes the grid states and dimensions."""
        self.grid_rows = GRID_ROWS
        self.grid_cols = GRID_COLS
        self.cell_width = frame_width // self.grid_cols
        self.cell_height = frame_height // self.grid_rows
        
        self.grid_states = {}
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                self.grid_states[(r, c)] = {
                    "state": "EMPTY",
                    "appliance": "OFF",
                    "state_change_time": time.time()
                }

    def _get_appliance_number(self, r, c):
        """
        NEW: Calculates a unique appliance number (1-16 for a 4x4 grid).
        Grid (0,0) -> 1, Grid (0,1) -> 2, ... Grid (1,0) -> 5
        """
        return (r * self.grid_cols) + c + 1

    def get_grid_cell(self, person_location_x, person_location_y):
        """Calculates the grid cell (row, col) for a given (x, y) coordinate."""
        grid_col = min(person_location_x // self.cell_width, self.grid_cols - 1)
        grid_row = min(person_location_y // self.cell_height, self.grid_rows - 1)
        return (grid_row, grid_col)

    def update_states(self, occupied_grids_this_frame):
        """
        Updates the state of all grid cells based on timers and occupancy.
        Contains the new terminal output logic.
        """
        current_time = time.time()

        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                grid_coord = (r, c)
                cell = self.grid_states[grid_coord]
                is_occupied = grid_coord in occupied_grids_this_frame
                time_elapsed = current_time - cell["state_change_time"]
                
                # Get the unique appliance number for this grid cell
                app_num = self._get_appliance_number(r, c)

                # --- CHECK FOR PERSON ENTRY ---
                if is_occupied and cell["state"] == "EMPTY":
                    cell["state"] = "OCCUPIED"
                    cell["state_change_time"] = current_time
                    if cell["appliance"] == "OFF":
                        cell["appliance"] = "PENDING_ON"
                        # MODIFIED: New output
                        print(f"RUNTIME: Person detected in Grid ({r},{c}). Starting {DELAY_SECONDS}s 'ON' timer for appliances {app_num}.")
                    elif cell["appliance"] == "PENDING_OFF":
                        cell["appliance"] = "ON"
                        # MODIFIED: New output
                        print(f"RUNTIME: Grid ({r},{c}) re-occupied. Cancelling 'OFF' timer. Appliances {app_num} stay ON.")

                # --- CHECK FOR PERSON EXIT ---
                elif not is_occupied and cell["state"] == "OCCUPIED":
                    cell["state"] = "EMPTY"
                    cell["state_change_time"] = current_time
                    if cell["appliance"] == "ON":
                        cell["appliance"] = "PENDING_OFF"
                        # MODIFIED: New output
                        print(f"RUNTIME: Grid ({r},{c}) is now empty. Starting {DELAY_SECONDS}s 'OFF' timer for appliances {app_num}.")
                    elif cell["appliance"] == "PENDING_ON":
                        cell["appliance"] = "OFF"
                        # MODIFIED: New output
                        print(f"RUNTIME: Grid ({r},{c}) vacated. Cancelling 'ON' timer. Appliances {app_num} stay OFF.")

                # --- PROCESS PENDING STATES (TIMER CHECK) ---
                if cell["appliance"] == "PENDING_ON" and time_elapsed > DELAY_SECONDS:
                    cell["appliance"] = "ON"
                    # MODIFIED: New output as requested
                    print(f"*** ACTION: Fan {app_num} and Light {app_num} corresponding to Grid ({r},{c}) are switching ON. ***")
                
                elif cell["appliance"] == "PENDING_OFF" and time_elapsed > DELAY_SECONDS:
                    cell["appliance"] = "OFF"
                    # MODIFIED: New output as requested
                    print(f"*** ACTION: Fan {app_num} and Light {app_num} corresponding to Grid ({r},{c}) are switching OFF. ***")