import tkinter as tk
from Logic import park_car, remove_car, get_parking_status

root = tk.Tk()
root.title("Parking Lot Simulator")
root.geometry("600x550")

canvas = tk.Canvas(root, width=580, height=300, bg="#2d2d2d")
canvas.pack(pady=10)

# Constants to avoid magic numbers
SLOTS = 5
SLOT_WIDTH = 105
SLOT_START_X = 30
SLOT_START_Y = 40
SLOT_HEIGHT = 160
SLOT_CENTER_OFFSET = 45
ROAD_Y = 235
ANIMATION_SPEED = 15

# Park car section
park_frame = tk.Frame(root)
park_frame.pack(pady=5)

tk.Label(park_frame, text="Enter Car Number:", font=("Arial", 10)).grid(row=0, column=0, padx=5)
entry_park = tk.Entry(park_frame, font=("Arial", 12))
entry_park.grid(row=0, column=1, padx=5)
btn_park = tk.Button(park_frame, text="Park Car", width=12, font=("Arial", 10))
btn_park.grid(row=0, column=2, padx=5)

# Remove car section
remove_frame = tk.Frame(root)
remove_frame.pack(pady=5)

tk.Label(remove_frame, text="Car Number to Remove:", font=("Arial", 10)).grid(row=0, column=0, padx=5)
entry_remove = tk.Entry(remove_frame, font=("Arial", 12))
entry_remove.grid(row=0, column=1, padx=5)
btn_remove_specific = tk.Button(remove_frame, text="Remove Specific", width=12, font=("Arial", 10))
btn_remove_specific.grid(row=0, column=2, padx=5)

# Remove first car button
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
btn_remove_first = tk.Button(btn_frame, text="Remove First Car (FIFO)", width=20, font=("Arial", 10))
btn_remove_first.pack()

status_label = tk.Label(root, text="", font=("Arial", 11), fg="blue")
status_label.pack(pady=10)

# Animation state
animating = False

def disable_all_buttons():
    """Disable all buttons during animation"""
    btn_park.config(state=tk.DISABLED)
    btn_remove_specific.config(state=tk.DISABLED)
    btn_remove_first.config(state=tk.DISABLED)

def enable_all_buttons():
    """Enable all buttons after animation"""
    btn_park.config(state=tk.NORMAL)
    btn_remove_specific.config(state=tk.NORMAL)
    btn_remove_first.config(state=tk.NORMAL)

def draw_background():
    """Draw road and parking area background"""
    # Main road
    canvas.create_rectangle(0, 200, 580, 300, fill="#4a4a4a", outline="")
    
    # Road markings
    for i in range(0, 580, 30):
        canvas.create_rectangle(i, 248, i+15, 252, fill="yellow", outline="")
    
    # Parking area
    canvas.create_rectangle(20, 20, 560, 180, fill="#6b6b6b", outline="")

def draw_parking_spaces(parking_snapshot):
    """Draw parking spaces and cars from a snapshot"""
    for i in range(SLOTS):
        x1 = SLOT_START_X + i * SLOT_WIDTH
        y1 = SLOT_START_Y
        x2 = x1 + 90
        y2 = SLOT_HEIGHT
        
        # Parking space lines
        canvas.create_line(x1, y1, x1, y2, fill="white", width=3)
        canvas.create_line(x2, y1, x2, y2, fill="white", width=3)
        canvas.create_line(x1, y2, x2, y2, fill="white", width=3)
        
        # Slot number
        canvas.create_text((x1 + x2)//2, y2 - 15, text=f"P{i+1}", font=("Arial", 14, "bold"), fill="white")
        
        # Draw parked car if exists in snapshot
        if i < len(parking_snapshot) and parking_snapshot[i] is not None:
            draw_car((x1 + x2) // 2, (y1 + y2) // 2 - 10, parking_snapshot[i], "car")

def draw_parking_lot():
    """Draw complete parking lot with current state"""
    canvas.delete("all")
    draw_background()
    parking = get_parking_status()
    draw_parking_spaces(parking)

def draw_car(x, y, car_number, tag="car"):
    """Draw a detailed car"""
    # Car shadow
    canvas.create_oval(x-28, y+20, x+28, y+28, fill="#1a1a1a", outline="", tags=tag)
    
    # Car body
    canvas.create_rectangle(x-30, y-20, x+30, y+20, fill="#3498db", outline="#2980b9", width=2, tags=tag)
    
    # Car roof
    canvas.create_polygon(x-20, y-20, x-15, y-30, x+15, y-30, x+20, y-20, 
                         fill="#2980b9", outline="#1a5490", width=2, tags=tag)
    
    # Windshield
    canvas.create_polygon(x-15, y-28, x-12, y-22, x+12, y-22, x+15, y-28,
                         fill="#85c1e9", outline="#2980b9", tags=tag)
    
    # Side windows
    canvas.create_rectangle(x-25, y-15, x-15, y-5, fill="#85c1e9", outline="#2980b9", tags=tag)
    canvas.create_rectangle(x+15, y-15, x+25, y-5, fill="#85c1e9", outline="#2980b9", tags=tag)
    
    # License plate
    canvas.create_rectangle(x-20, y+5, x+20, y+15, fill="white", outline="black", width=2, tags=tag)
    canvas.create_text(x, y+10, text=car_number, font=("Arial", 9, "bold"), fill="black", tags=tag)
    
    # Wheels
    canvas.create_oval(x-22, y+15, x-14, y+23, fill="black", outline="#333", width=2, tags=tag)
    canvas.create_oval(x+14, y+15, x+22, y+23, fill="black", outline="#333", width=2, tags=tag)
    
    # Wheel rims
    canvas.create_oval(x-20, y+17, x-16, y+21, fill="#555", outline="", tags=tag)
    canvas.create_oval(x+16, y+17, x+20, y+21, fill="#555", outline="", tags=tag)
    
    # Headlights
    canvas.create_oval(x-25, y+8, x-20, y+12, fill="#ffffcc", outline="#ffff99", tags=tag)
    canvas.create_oval(x+20, y+8, x+25, y+12, fill="#ffffcc", outline="#ffff99", tags=tag)

def animate_park(car_number, target_slot):
    """Animate car driving in and parking"""
    global animating
    animating = True
    disable_all_buttons()
    
    # Get snapshot ONCE at start
    parking_snapshot = get_parking_status().copy()
    
    start_x = -50
    start_y = ROAD_Y
    target_x = SLOT_START_X + target_slot * SLOT_WIDTH + SLOT_CENTER_OFFSET
    target_y = 90
    
    steps_road = 35
    steps_park = 20
    
    dx_road = (target_x - start_x) / steps_road
    current_x = start_x
    current_y = start_y
    
    def move_on_road(step=0):
        nonlocal current_x
        
        if step < steps_road:
            canvas.delete("all")
            draw_background()
            draw_parking_spaces(parking_snapshot)
            draw_car(current_x, current_y, car_number, "moving_car")
            current_x += dx_road
            root.after(ANIMATION_SPEED, lambda: move_on_road(step + 1))
        else:
            move_to_space(0)
    
    def move_to_space(step=0):
        global animating
        nonlocal current_y
        
        if step < steps_park:
            canvas.delete("all")
            draw_background()
            draw_parking_spaces(parking_snapshot)
            draw_car(current_x, current_y, car_number, "moving_car")
            current_y -= (start_y - target_y) / steps_park
            root.after(ANIMATION_SPEED, lambda: move_to_space(step + 1))
        else:
            # NOW update data after animation completes
            msg = park_car(car_number)
            status_label.config(text=msg)
            animating = False
            enable_all_buttons()
            draw_parking_lot()
    
    move_on_road()

def animate_remove(car_number, from_slot, on_complete):
    """Animate car leaving parking lot"""
    global animating
    animating = True
    disable_all_buttons()
    
    # Get snapshot ONCE at start (before data removal)
    parking_snapshot = get_parking_status().copy()
    
    start_x = SLOT_START_X + from_slot * SLOT_WIDTH + SLOT_CENTER_OFFSET
    start_y = 90
    road_y = ROAD_Y
    exit_x = 630
    
    steps_exit = 20
    steps_road = 35
    
    dy_exit = (road_y - start_y) / steps_exit
    dx_road = (exit_x - start_x) / steps_road
    
    current_x = start_x
    current_y = start_y
    
    def move_to_road(step=0):
        nonlocal current_y
        
        if step < steps_exit:
            canvas.delete("all")
            draw_background()
            draw_parking_spaces(parking_snapshot)
            draw_car(current_x, current_y, car_number, "moving_car")
            current_y += dy_exit
            root.after(ANIMATION_SPEED, lambda: move_to_road(step + 1))
        else:
            move_on_road(0)
    
    def move_on_road(step=0):
        global animating
        nonlocal current_x
        
        if step < steps_road:
            canvas.delete("all")
            draw_background()
            draw_parking_spaces(parking_snapshot)
            draw_car(current_x, current_y, car_number, "moving_car")
            current_x += dx_road
            root.after(ANIMATION_SPEED, lambda: move_on_road(step + 1))
        else:
            # NOW update data after animation completes
            on_complete()
            animating = False
            enable_all_buttons()
            draw_parking_lot()
    
    move_to_road()

def park():
    """Handle park car button"""
    if animating:
        return
    
    car = entry_park.get().strip()
    if not car:
        status_label.config(text="Please enter a car number!")
        return
    
    parking = get_parking_status()
    target_slot = None
    
    for i in range(SLOTS):
        if i >= len(parking) or parking[i] is None:
            target_slot = i
            break
    
    if target_slot is None:
        status_label.config(text="Parking is full!")
        return
    
    entry_park.delete(0, tk.END)
    animate_park(car, target_slot)

def remove_specific():
    """Handle remove specific car button"""
    if animating:
        return
    
    car = entry_remove.get().strip()
    if not car:
        status_label.config(text="Please enter a car number!")
        return
    
    parking = get_parking_status()
    from_slot = None
    
    for i in range(SLOTS):
        if i < len(parking) and parking[i] == car:
            from_slot = i
            break
    
    if from_slot is None:
        status_label.config(text=f"Car {car} not found!")
        return
    
    entry_remove.delete(0, tk.END)
    
    def complete_removal():
        msg = remove_car(car)
        status_label.config(text=msg)
    
    animate_remove(car, from_slot, complete_removal)

def remove_first():
    """Handle remove first car (FIFO) button"""
    if animating:
        return
    
    # Import actual parking list to get the real first car
    from Logic import parking as actual_parking
    
    if len(actual_parking) == 0:
        status_label.config(text="Parking is empty!")
        return
    
    # Get the ACTUAL first car in the list
    car_number = actual_parking[0]
    
    # Find its visual position
    parking_display = get_parking_status()
    from_slot = None
    
    for i in range(SLOTS):
        if i < len(parking_display) and parking_display[i] == car_number:
            from_slot = i
            break
    
    if from_slot is None:
        status_label.config(text="Error: Car data mismatch!")
        return
    
    def complete_removal():
        msg = remove_car()  # Remove first car (FIFO)
        status_label.config(text=msg)
    
    animate_remove(car_number, from_slot, complete_removal)

# Connect button commands
btn_park.config(command=park)
btn_remove_specific.config(command=remove_specific)
btn_remove_first.config(command=remove_first)

draw_parking_lot()
root.mainloop()