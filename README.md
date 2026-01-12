# Parking Queue Simulator - Mini Project Report

## Course: Data Structure and Algorithms (COMP 202),
## Assignment 1

This project is a parking management simulator that demonstrates the use of Data Structures and Algorithms (DSA) concepts, specifically the circular queue. The simulator allows users to park cars, remove cars, and view the current state of parking slots using a GUI interface with Tkinter. The program ensures efficient utilization of parking space by reusing slots freed by departing cars.

---

# Objective:

- To implement a real-world problem (parking lot management) using DSA concepts.
- To demonstrate the functionality of a circular queue for efficient memory usage.
- To provide an interactive and visual representation of queue operations using a GUI.
- To strengthen understanding of queue operations like enqueue, dequeue, and display.

---

# Data Structure: 
Circular Queue (implemented using a fixed-size array)

# Reason for Choosing Circular Queue:

- Efficient memory usage: Unlike a linear queue, circular queue reuses freed slots, preventing wasted space.
- Constant time operations: Enqueue and dequeue operations take O(1) time.
- Realistic simulation: Closely models a parking lot where cars arrive and leave in order.
- Concept demonstration: Circular queue allows visualization of pointer movement (front and rear), which is essential for DSA understanding.

# Why Tkinter Instead of Pygame?

- No external dependencies required
- Cross-platform compatibility
- Sufficient for 2D visualization needs
- Easier setup for college environment

---

# Algorithm/ working mechanism:

## Algorithm for Park Car (Enqueue):

- Check if the queue is full: (rear + 1) % MAX_SIZE == front.
If full, display “Parking is full”.
- If the queue is empty (front == -1), set front = 0 and rear = 0.
- Otherwise, move rear to next position using (rear + 1) % MAX_SIZE.
- Add the car number at parking[rear].
- Display success message.

## Algorithm for Remove Car (Dequeue):

- Check if the queue is empty (front == -1).
If empty, display “Parking is empty”.
- Remove the car at parking[front].
- If the removed car was the only car (front == rear), reset front = rear = -1.
- Otherwise, move front to (front + 1) % MAX_SIZE.
- Display removal success message.

## Algorithm for Display Parking Slots:

- If the queue is empty (front == -1), display “Parking is empty”.
- Otherwise, iterate through the parking array and show the car numbers in each slot.

---

# Basic Time Complexity Analysis:

Operation	               Time Complexity	                      Reason
Park Car (Enqueue)	            O(1)	           Direct index assignment and pointer update
Remove Car (Dequeue)          	O(1)	           Direct index removal and pointer update
Display Parking	                O(n)	           Iterates through all parking slots (MAX_SIZE = n)

---

# Future improvements
# References
....left to write more ..functions ko gui ko hola 
- learnt GUI from- https://www.youtube.com/watch?si=UCzMjn9mq-gtI54V&v=mop6g-c5HEY&feature=youtu.be-
- https://youtu.be/rUUrmGKYwHw?si=XGYRMcjNEgUM6P7m
- https://youtu.be/pWnH4Q3eMKI?si=L0ObHEjtil400N48
- https://youtu.be/ibf5cx221hk?si=KpzwJYVGbQ8F7NBE
- take screenshot from img for tkinter short notes
- add screenshot from GUI
- Queue data structure theory: Course lecture notes COMP202


