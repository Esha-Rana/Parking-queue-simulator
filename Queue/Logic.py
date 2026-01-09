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

def get_parking_status():
    return parking.copy()
