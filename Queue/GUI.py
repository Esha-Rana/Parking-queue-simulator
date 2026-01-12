import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random
from Logic import ParkingLot


class ParkingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Queue Sim. (DSA Project)")
        self.root.geometry("950x800")
        self.root.resizable(False, False)
        
        self.bg_color = "#2b2b2b"
        self.canvas_bg = "#1e1e1e"
        self.road_color = "#3a3a3a"
        self.slot_color = "#4a4a4a"
        
        self.root.configure(bg=self.bg_color)
        
        self.lot_a = ParkingLot("A")
        self.lot_b = ParkingLot("B")
        self.animating = False
        self.auto_mode = False
        self.car_counter = 1
        
        self.animating_car = None
        self.animating_car_pos = None
        
        self.setup_ui()
        self.draw_scene()
    
    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=15)
        
        tk.Label(
            title_frame,
            text="Parking Queue Simulator",
            font=("Arial", 18, "bold"),
            fg="white",
            bg=self.bg_color
        ).pack()
        
        self.canvas = tk.Canvas(
            self.root, 
            width=900, 
            height=420, 
            bg=self.canvas_bg,
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=15)
        
        self.auto_btn = tk.Button(
            control_frame,
            text="▶ Start Auto Simulation",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            width=22,
            height=2,
            command=self.toggle_auto_mode,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.auto_btn.pack(pady=(0, 15))
        
        manual_frame = tk.LabelFrame(
            control_frame,
            text=" Manual Controls ",
            font=("Arial", 11, "bold"),
            fg="white",
            bg=self.bg_color,
            padx=20,
            pady=15
        )
        manual_frame.pack()
        
        park_frame = tk.Frame(manual_frame, bg=self.bg_color)
        park_frame.pack(pady=8)
        
        tk.Label(
            park_frame,
            text="Car Number:",
            font=("Arial", 10),
            fg="white",
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.car_entry = tk.Entry(
            park_frame,
            width=12,
            font=("Arial", 10),
            bg="#3a3a3a",
            fg="white",
            insertbackground="white",
            relief=tk.FLAT
        )
        self.car_entry.pack(side=tk.LEFT, padx=5, ipady=4)
        
        tk.Label(
            park_frame,
            text="Lot:",
            font=("Arial", 10),
            fg="white",
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=(15, 5))
        
        self.lot_var = tk.StringVar(value="A")
        
        tk.Radiobutton(
            park_frame,
            text="A",
            variable=self.lot_var,
            value="A",
            font=("Arial", 10),
            fg="white",
            bg=self.bg_color,
            selectcolor="#3a3a3a",
            activebackground=self.bg_color,
            activeforeground="white"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Radiobutton(
            park_frame,
            text="B",
            variable=self.lot_var,
            value="B",
            font=("Arial", 10),
            fg="white",
            bg=self.bg_color,
            selectcolor="#3a3a3a",
            activebackground=self.bg_color,
            activeforeground="white"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            park_frame,
            text="Park",
            command=self.manual_park,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0), ipady=3)
        
        remove_frame = tk.Frame(manual_frame, bg=self.bg_color)
        remove_frame.pack(pady=8)
        
        tk.Button(
            remove_frame,
            text="Remove First from A",
            command=lambda: self.manual_remove("A"),
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=22,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=3)
        
        tk.Button(
            remove_frame,
            text="Remove First from B",
            command=lambda: self.manual_remove("B"),
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=22,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=3)
        
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 11),
            fg="#27ae60",
            bg=self.bg_color
        )
        self.status_label.pack(pady=10)
        
        author_btn = tk.Button(
            self.root,
            text="About Authors",
            command=self.show_authors,
            bg="#34495e",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
            relief=tk.FLAT,
            cursor="hand2"
        )
        author_btn.pack(pady=5)
        
        credits_label = tk.Label(
            self.root,
            text="Created by: Esha Rana & Ananya Tripathi | C.S. 2",
            font=("Arial", 9),
            fg="#95a5a6",
            bg=self.bg_color
        )
        credits_label.pack(pady=5)
    
    def draw_scene(self):
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(0, 320, 900, 420, fill=self.road_color, outline="")
        
        for i in range(0, 900, 35):
            self.canvas.create_rectangle(i, 368, i+20, 372, fill="yellow", outline="")
        
        self.canvas.create_rectangle(435, 0, 465, 420, fill=self.road_color, outline="")
        for i in range(0, 420, 35):
            self.canvas.create_rectangle(448, i, 452, i+20, fill="yellow", outline="")
        
        self.draw_parking_lot(20, 20, self.lot_a, "A")
        
        self.draw_parking_lot(480, 20, self.lot_b, "B")
        
        if self.animating_car and self.animating_car_pos:
            self.draw_car(int(self.animating_car_pos[0]), int(self.animating_car_pos[1]), self.animating_car)
    
    def draw_parking_lot(self, x, y, lot, lot_name):
        self.canvas.create_rectangle(
            x, y, x+400, y+280,
            fill=self.slot_color,
            outline="white",
            width=2
        )
        
        self.canvas.create_text(
            x+200, y+15,
            text=f"LOT {lot_name}",
            font=("Arial", 16, "bold"),
            fill="white"
        )
        
        for i in range(5):
            sx = x + 10 + i * 78
            sy = y + 35
            
            self.canvas.create_rectangle(
                sx, sy, sx+68, sy+220,
                outline="white",
                width=2,
                fill="#3a3a3a"
            )
            
            self.canvas.create_text(
                sx+34, sy+200,
                text=f"P{i+1}",
                font=("Arial", 13, "bold"),
                fill="white"
            )
            
            car = lot.parking[i]
            if car:
                self.draw_car(sx+34, sy+90, car['car_number'])
    
    def draw_car(self, x, y, car_num):
        self.canvas.create_rectangle(
            x-24, y-18, x+24, y+18,
            fill="#3498db",
            outline="#2980b9",
            width=2
        )
        
        self.canvas.create_polygon(
            x-18, y-18,
            x-12, y-28,
            x+12, y-28,
            x+18, y-18,
            fill="#2980b9",
            outline="#1a5490",
            width=2
        )
        
        self.canvas.create_polygon(
            x-11, y-26,
            x-9, y-20,
            x+9, y-20,
            x+11, y-26,
            fill="#85c1e9",
            outline="#2980b9"
        )
        
        self.canvas.create_rectangle(
            x-20, y+5, x+20, y+15,
            fill="yellow",
            outline="black",
            width=2
        )
        self.canvas.create_text(
            x, y+10,
            text=str(car_num),
            font=("Arial", 8, "bold"),
            fill="black"
        )
        
        self.canvas.create_oval(x-18, y+14, x-10, y+22, fill="black")
        self.canvas.create_oval(x+10, y+14, x+18, y+22, fill="black")
    
    def toggle_auto_mode(self):
        self.auto_mode = not self.auto_mode
        
        if self.auto_mode:
            self.auto_btn.config(
                text="⏸ Pause Auto Simulation",
                bg="#e74c3c"
            )
            self.status_label.config(
                text="Auto Mode: Running...",
                fg="#27ae60"
            )
            self.run_auto_simulation()
        else:
            self.auto_btn.config(
                text="▶ Start Auto Simulation",
                bg="#27ae60"
            )
            self.status_label.config(
                text="Auto Mode: Paused",
                fg="#f39c12"
            )
    
    def show_authors(self):
        import tkinter.messagebox as messagebox
        messagebox.showinfo(
            "Project Authors",
            "Parking Queue Simulator\nDSA Project\n\n"
            "Created by:\n\n"
            "Esha Rana\n"
            "Ananya Tripathi\n\n"
            "C.S. 2"
        )
    
    def run_auto_simulation(self):
        if not self.auto_mode:
            return
        
        action = random.choice(["park", "remove"])
        
        if action == "park":
            lot = random.choice([self.lot_a, self.lot_b])
            if not lot.is_full():
                car_num = f"C{self.car_counter:03d}"
                self.car_counter += 1
                self.animate_park(lot, car_num)
        else:
            lot = random.choice([self.lot_a, self.lot_b])
            if not lot.is_empty():
                self.animate_remove(lot)
        
        delay = random.randint(2000, 4000)
        self.root.after(delay, self.run_auto_simulation)
    
    def manual_park(self):
        if self.animating or self.auto_mode:
            return
        
        car = self.car_entry.get().strip().upper()
        if not car:
            self.status_label.config(
                text="Enter car number!",
                fg="#e74c3c"
            )
            return
        
        lot = self.lot_a if self.lot_var.get() == "A" else self.lot_b
        self.car_entry.delete(0, tk.END)
        self.animate_park(lot, car)
    
    def manual_remove(self, lot_name):
        if self.animating or self.auto_mode:
            return
        
        lot = self.lot_a if lot_name == "A" else self.lot_b
        self.animate_remove(lot)
    
    def animate_park(self, lot, car_num):
        if self.animating:
            return
        
        can_park, msg = lot.can_park(car_num)
        if not can_park:
            self.status_label.config(text=msg, fg="#e74c3c")
            return
        
        slot_index = lot.get_next_empty_slot()
        if slot_index is None:
            self.status_label.config(text=f"Lot {lot.lot_id} is full!", fg="#e74c3c")
            return
        
        self.animating = True
        self.animating_car = car_num
        
        self.status_label.config(
            text=f"Parking {car_num}...",
            fg="#3498db"
        )
        
        base_x = 20 if lot == self.lot_a else 480
        final_x = base_x + 44 + slot_index * 78
        final_y = 145
        
        if lot == self.lot_a:
            start_x = -30
            start_y = 370
            turn_x = final_x
            turn_y = 370
            
            self.animate_car_three_phase(
                start_x, start_y, turn_x, turn_y, turn_x, turn_y, final_x, final_y,
                car_num, lot, True
            )
        else:
            start_x = -30
            start_y = 370
            junction_x = 450
            junction_y = 370
            turn_x = final_x
            turn_y = 370
            
            self.animate_car_three_phase(
                start_x, start_y, junction_x, junction_y, turn_x, turn_y, final_x, final_y,
                car_num, lot, True
            )
    
    def animate_remove(self, lot):
        if self.animating:
            return
        
        success, car_num, slot_idx = lot.remove_first()
        if not success:
            self.status_label.config(
                text=f"Lot {lot.lot_id} is empty!",
                fg="#e74c3c"
            )
            return
        
        self.animating = True
        self.animating_car = car_num
        
        self.status_label.config(
            text=f"Removing {car_num}...",
            fg="#e74c3c"
        )
        
        base_x = 20 if lot == self.lot_a else 480
        start_x = base_x + 44 + slot_idx * 78
        start_y = 145
        
        road_y = 370
        exit_x = 950
        
        self.animate_car_movement(
            start_x, start_y, start_x, road_y, exit_x, road_y,
            car_num, lot, False
        )
    
    def animate_car_three_phase(self, x1, y1, x2, y2, x3, y3, x4, y4, car_num, lot, is_parking):
        steps = 25
        
        dx1 = (x2 - x1) / steps
        dy1 = (y2 - y1) / steps
        
        dx2 = (x3 - x2) / steps
        dy2 = (y3 - y2) / steps
        
        dx3 = (x4 - x3) / steps
        dy3 = (y4 - y3) / steps
        
        current = [x1, y1]
        phase = [1]
        step = [0]
        
        def animate_step():
            if phase[0] == 1:
                if step[0] < steps:
                    current[0] += dx1
                    current[1] += dy1
                    step[0] += 1
                else:
                    phase[0] = 2
                    step[0] = 0
            elif phase[0] == 2:
                if step[0] < steps:
                    current[0] += dx2
                    current[1] += dy2
                    step[0] += 1
                else:
                    phase[0] = 3
                    step[0] = 0
            elif phase[0] == 3:
                if step[0] < steps:
                    current[0] += dx3
                    current[1] += dy3
                    step[0] += 1
                else:
                    if is_parking:
                        success, final_msg = lot.park(car_num)
                        final_color = "#27ae60" if success else "#e74c3c"
                    else:
                        final_msg = f"Car {car_num} removed from Lot {lot.lot_id}"
                        final_color = "#e74c3c"
                    
                    self.animating = False
                    self.animating_car = None
                    self.animating_car_pos = None
                    self.status_label.config(text=final_msg, fg=final_color)
                    self.draw_scene()
                    return
            
            self.animating_car_pos = [current[0], current[1]]
            self.draw_scene()
            self.root.after(20, animate_step)
        
        animate_step()
    
    def animate_car_movement(self, x1, y1, x2, y2, x3, y3, car_num, lot, is_parking):
        steps = 25
        
        dx1 = (x2 - x1) / steps
        dy1 = (y2 - y1) / steps
        
        dx2 = (x3 - x2) / steps
        dy2 = (y3 - y2) / steps
        
        current = [x1, y1]
        phase = [1]
        step = [0]
        
        def animate_step():
            if phase[0] == 1:
                if step[0] < steps:
                    current[0] += dx1
                    current[1] += dy1
                    step[0] += 1
                else:
                    phase[0] = 2
                    step[0] = 0
            elif phase[0] == 2:
                if step[0] < steps:
                    current[0] += dx2
                    current[1] += dy2
                    step[0] += 1
                else:
                    if is_parking:
                        success, final_msg = lot.park(car_num)
                        final_color = "#27ae60" if success else "#e74c3c"
                    else:
                        final_msg = f"Car {car_num} removed from Lot {lot.lot_id}"
                        final_color = "#e74c3c"
                    
                    self.animating = False
                    self.animating_car = None
                    self.animating_car_pos = None
                    self.status_label.config(text=final_msg, fg=final_color)
                    self.draw_scene()
                    return
            
            self.animating_car_pos = [current[0], current[1]]
            self.draw_scene()
            self.root.after(20, animate_step)
        
        animate_step()


def main():
    root = tk.Tk()
    app = ParkingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()