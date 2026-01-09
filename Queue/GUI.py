import tkinter as tk
from Logic import park_car, remove_car, get_parking_status

root = tk.Tk()
root.title("Parking Queue Simulator")
root.geometry("520x400")

canvas = tk.Canvas(root, width=500, height=200, bg="lightgray")
canvas.pack(pady=10)

label = tk.Label(root, text="Enter Car Number:")
label.pack(side=tk.LEFT, padx=5, pady=5)

entry = tk.Entry(root, font=("Arial",12))
entry.pack(side=tk.LEFT, padx=5, pady=5)

status_label = tk.Label(root, text="", font=("Arial", 11))
status_label.pack(pady=5)

def draw_parking():
    canvas.delete("all")
    parking = get_parking_status()

    for i in range(len(parking)):
        x1 = 20 + i * 90
        y1 = 60
        x2 = x1 + 70
        y2 = 120

        canvas.create_rectangle(x1, y1, x2, y2, fill="white")
        canvas.create_text((x1 + x2)//2, y1 - 10, text=f"Slot {i}", font=("Arial", 10, "bold"))

        if parking[i] is not None:
            canvas.create_text(
                (x1 + x2) // 2,
                (y1 + y2) // 2,
                text=parking[i],
                font=("Arial", 10)

            )

def park():
    car = entry.get()
    if car:
        msg = park_car(car)
        status_label.config(text=msg)
        entry.delete(0, tk.END)
        draw_parking()

def remove():
    msg = remove_car()
    status_label.config(text=msg)
    draw_parking()


btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Park Car", width=12, command=park).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Remove Car", width=12, command=remove).grid(row=0, column=1, padx=5)

draw_parking()

root.mainloop()
