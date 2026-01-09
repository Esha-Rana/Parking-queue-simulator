MAX_SIZE = 5
parking = [None] * MAX_SIZE
front = -1
rear = -1

def park_car(car):
    global front, rear

    if front == (rear + 1) % MAX_SIZE:
        return "Parking is full!"

    if front == -1:
        front = 0
        rear = 0
    else:
        rear = (rear + 1) % MAX_SIZE

    parking[rear] = car
    return f"Car {car} parked successfully!"

def remove_car():
    global front, rear

    if front == -1:
        return "Parking is empty!"

    car = parking[front]
    parking[front] = None

    if front == rear:
        front = -1
        rear = -1
    else:
        front = (front + 1) % MAX_SIZE

    return f"Car {car} left the parking!"

def remove_specific(car_number):
    global front, rear, parking

    if front == -1:
        return "Parking is empty!"

    i = front
    found = False

    while True:
        if parking[i] == car_number:
            found = True
            break
        if i == rear:
            break
        i = (i + 1) % MAX_SIZE

    if not found:
        return f"Car {car_number} not found!"

    # Shift elements
    j = i
    while j != rear:
        next_index = (j + 1) % MAX_SIZE
        parking[j] = parking[next_index]
        j = next_index

    parking[rear] = None

    if front == rear:
        front = rear = -1
    else:
        rear = (rear - 1 + MAX_SIZE) % MAX_SIZE

    return f"Car {car_number} removed successfully!"

def get_parking_status():
        return parking.copy()
