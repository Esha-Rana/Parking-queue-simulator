MAX_SIZE = 5
parking = [None] * MAX_SIZE
front = -1
rear = -1

def park_car(car):
    global front, rear

    if front == (rear + 1) % MAX_SIZE:
        print("Parking is full!")
        return

    if front == -1:
        front = 0
        rear = 0
    else:
        rear = (rear + 1) % MAX_SIZE

    parking[rear] = car
    print(f"Car {car} parked successfully!")

def remove_car():
    global front, rear

    if front == -1:
        print("Parking is empty!")
        return

    car = parking[front]
    parking[front] = None

    if front == rear:
        front = -1
        rear = -1
    else:
        front = (front + 1) % MAX_SIZE

    print(f"Car {car} left the parking!")

def display_parking():
    if front == -1:
        print("Parking is empty!")
        return

    print("\nParking Slots:")
    for i in range(MAX_SIZE):
        print(f"Slot {i}: {parking[i]}")

while True:
    print("\n--- Parking Menu ---")
    print("1. Park a car")
    print("2. Remove a car")
    print("3. Show parking")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        while True:
            car = input("Enter car number (or 'q' to stop): ")
            if car.lower() == 'q':
                break
            park_car(car)
            
    elif choice == '2':
        remove_car()

    elif choice == '3':
        display_parking()

    elif choice == '4':
        print("Exiting program...")
        break

    else:
        print("Invalid choice! Please enter 1-4.")
