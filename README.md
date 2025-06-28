# Flight-Optimization

This project implements a flight routing system that supports efficient planning of air travel routes based on:

- ✈️ Least number of flights
- 💰 Cheapest total fare
- ⏱️ Earliest arrival
- 🧭 Hybrid of least flights and cheapest fare

It includes:
- Custom data structures (`LinkedQueue`, `MinHeap`)
- Graph traversal algorithms (BFS, Dijkstra’s)
- Real-world constraints like layover time and valid time windows

---

## 📦 File Structure
📁 Flight_Optimization/
├── planner.py # Main logic and algorithms
├── flight.py # Flight class (assumed to be provided)


---

## 📘 Features

### ✅ Route Algorithms

1. **least_flights_earliest_route**
   - Finds a valid path with the **fewest flights**
   - Among paths with same length, prefers the **earliest arrival**

2. **cheapest_route**
   - Computes a path with the **minimum total fare** using Dijkstra’s algorithm

3. **least_flights_cheapest_route**
   - Among all paths with the **least number of flights**, chooses the **cheapest one**

### ✅ Realistic Constraints

- Flights must:
  - **Start after `t1`**
  - **End before `t2`**
  - **Allow at least 20 mins layover between flights**

---

## 🧱 Core Data Structures

### 🔗 `LinkedQueue`
- Used for BFS traversal
- Linked list–based queue implementation

### 🔻 `Heap` (Min-Heap)
- Used in Dijkstra’s algorithm
- Orders routes based on (fare, timestamp)

---

## 🚀 Planner API

### `Planner(flights)`
Initializes the planner with a list of `Flight` objects.

Each `Flight` object must have:
```python
start_city: int
end_city: int
departure_time: int
arrival_time: int
fare: int
