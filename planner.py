from flight import Flight


class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class prevPointer:
    def __init__(self,flight,previous = None):
        self.flight = flight
        self.previous = previous
        
    
        
class LinkedQueue:

    def __init__(self):
        self.front  = None
        self.rear = None
        self.size = 0
    
    def is_empty(self):
        return self.size == 0

    def push_back(self,elem):
        node_to_add = Node(elem)
        if self.rear is not None:
            self.rear.next = node_to_add
        else:
            self.front = node_to_add
        
        self.rear = node_to_add
        self.size += 1
    
    def pop_front(self):
        if self.is_empty():
            raise IndexError("Cannot remove from an empty queue")
        val = self.front.data

        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size = self.size - 1
        return val


class Heap:    
    def __init__(self, comparison_function, init_array):

        self.heap = init_array
        self.comp_func = comparison_function
        self._heapify()
        


    def insert(self, value):
        
        # Write your code here
        self.heap.append(value)
        self._upheap(len(self.heap)-1)
    
    def extract(self):

        if self.heap:
            self._swap_data(0,len(self.heap)-1)
            x = self.heap.pop()
            self._downheap(0)
            return x

    
    def top(self):
        if self.heap:
            return self.heap[0]
        else:
            return None
    
 

    def _lc(self,i):
        return 2*i+1
    
    def _rc(self,i):
        return 2*i+2
    
    def _parent(self,i):
        return (i-1)//2

    def _lc_exists(self,i):
        return self._lc(i) < len(self.heap)

    def _rc_exists(self,i):
        return self._rc(i) < len(self.heap)
    
    def _swap_data(self,i,j):
        self.heap[i],self.heap[j] = self.heap[j],self.heap[i]


    def _heapify(self):
        start = self._parent(len(self.heap)-1)
        for i in range(start,-1,-1):
            self._downheap(i)

    def _downheap(self,index):
        if self._lc_exists(index):
            l = self._lc(index)
            small = l
            if self._rc_exists(index):
                r = self._rc(index)
                if not self.comp_func(self.heap[l],self.heap[r]):
                    small = r

            if self.comp_func(self.heap[small],self.heap[index]):
                self._swap_data(small,index)
                self._downheap(small)


    def _upheap(self,index):
        parent = self._parent(index)
        if index > 0  and  self.comp_func(self.heap[index],self.heap[parent]):
            self._swap_data(index,parent)
            self._upheap(parent)
    
    def is_empty(self):
        return (len(self.heap) == 0)
    
    def size(self): ##helper function for iterations over heap array
        return len(self.heap)
    

def comp_func(a,b):
    return a[0] < b[0] if a[0] != b[0] else a[1] < b[1]

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        #size of graph defined by max_city
        self.graph_size = max(max(flight.start_city,flight.end_city) for flight in flights) 
        #initialised graph in form of adjacency list
        self.flight_graph = [[] for _ in range(self.graph_size + 1)]
        #filling up the adjacency list to complete the graph
        for flight in flights:
            self.flight_graph[flight.start_city].append(flight)
        self.num_flights = len(flights)
            
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        #Breadth-First Search
        #no need for flights to reach the same city
        if start_city == end_city:
            return  [] #empty list returned as directed
        
        #initialising an array of parent pointers to allow backtracking and prevent copying
        parent_array = [-1 for _ in range(self.graph_size + 1)]
        parent_array[start_city] = None

        #initialising a flights used array to backtrack
        flights_used = [None for _ in range(self.graph_size + 1)]

        #initialising a arrival_times array for comparisons
        arrival_times = [float('inf') for _ in range(self.graph_size + 1)]
        arrival_times[start_city] = t1

        #initialising a linked queue data structure
        queue = LinkedQueue()
        queue.push_back((start_city , t1))

        while not queue.is_empty():
            current_city , current_time = queue.pop_front()

            #check all flights scheduled to leave from the current city
            for flight in self.flight_graph[current_city]:
                arrival_time = flight.arrival_time
                dept_time = flight.departure_time

                next_city = flight.end_city
                #flight should not depart before t1 and should not end after t2 and should leave atleast 20 mins after the next flight
                if dept_time >= t1 and arrival_time <= t2 :
                    #fill-in the arrays with specified values
                    try:
                        if flight.start_city == start_city:
                            #dept_time >= t1 not t1+20
                            if arrival_time < arrival_times[next_city]:
                                arrival_times[next_city] = arrival_time
                                parent_array[next_city] = current_city
                                flights_used[next_city] = flight
                                queue.push_back((next_city,arrival_time))
                        else:
                            if dept_time >= current_time + 20:
                                if arrival_time < arrival_times[next_city]:
                                    arrival_times[next_city] = arrival_time
                                    parent_array[next_city] = current_city
                                    flights_used[next_city] = flight
                                    queue.push_back((next_city,arrival_time))
                    except:
                        print(flight.start_city)
                
        #back-track
        if arrival_times[end_city] != float('inf'):
            route = []
            current_city = end_city
            while current_city and parent_array[current_city] != -1:
                route.append(flights_used[current_city])
                current_city = parent_array[current_city]
            
            return route[::-1]
        else:
            return []#no possible routes -- time = inf


    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        #Djikstra's Algorithm
        if start_city == end_city:
            return  []
        
        #array of fares (weights) for djikstra
        fare_arr = [float('inf') for _ in range(self.graph_size + 1)]
        fare_arr[start_city] = 0

        #array of parent pointers for optimisation
        parent_array = [-1 for _ in range(self.graph_size + 1)]
        parent_array[start_city] = None

        #flights_used array
        flights_used = [None for _ in range(self.graph_size + 1)]

        #minheap for djikstra
        heap = Heap(init_array= [],comparison_function=comp_func)
        heap.insert((0,start_city,t1))

        while not heap.is_empty():
            current_fare , current_city , current_time = heap.extract()

            if current_city == end_city:
                break

            for flight in self.flight_graph[current_city]:
                arrival_time = flight.arrival_time
                dept_time = flight.departure_time
                next_city = flight.end_city
                flight_fare = flight.fare
                try:
                    if dept_time >= t1 and arrival_time <= t2 :
                        #fill-in the arrays with specified values
                        if flight.start_city == start_city:
                            new_fare = current_fare + flight_fare
                            if new_fare < fare_arr[next_city]:
                                fare_arr[next_city] = new_fare
                                parent_array[next_city] = current_city
                                flights_used[next_city] = flight
                                heap.insert((new_fare,next_city,arrival_time))
                        
                        else:
                            if dept_time >= current_time + 20:
                                new_fare = current_fare + flight_fare
                                if new_fare < fare_arr[next_city]:
                                    fare_arr[next_city] = new_fare
                                    parent_array[next_city] = current_city
                                    flights_used[next_city] = flight
                                    heap.insert((new_fare,next_city,arrival_time))
                except:
                    print(flight.start_city)

        #back-track
        if fare_arr[end_city] != float('inf'):
            current_city = end_city
            route = []
            while current_city and parent_array[current_city] != -1:
                route.append(flights_used[current_city])
                current_city = parent_array[current_city]
            
            return route[::-1]
        
        else:
            return []


    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest.
        """

                #BFS
        if start_city == end_city:
            return []
        
        parent_array = [-1 for _ in range(self.graph_size + 1)]
        parent_array[start_city] = None

        min_fare = [float('inf') for _ in range(self.graph_size + 1)]
        min_fare[start_city] = 0

        arrival_times = [float('inf') for _ in range(self.graph_size + 1)]
        arrival_times[start_city] = t1

        flights_used = [None for _ in range(self.graph_size + 1)]

        queue = LinkedQueue()
        queue.push_back((start_city,0,0,t1)) #current_city, current_fare, current_flights, current_time

        while not queue.is_empty():
            current_city, current_fare, current_flights, current_time = queue.pop_front()

            for flight in self.flight_graph[current_city]:
                next_city = flight.end_city
                dept_time = flight.departure_time 
                arrival_time = flight.arrival_time
                flight_fare = flight.fare
            
                try:
                    if dept_time >= t1 and arrival_time <= t2:

                        if start_city == current_city:

                            new_fare = current_fare + flight_fare
                            new_flights = current_flights + 1

                            if (new_flights < arrival_times[next_city]) or (new_flights == arrival_times[next_city] and new_fare < min_fare[next_city]):
                                arrival_times[next_city] = new_flights
                                min_fare[next_city] = new_fare
                                parent_array[next_city] = current_city
                                flights_used[next_city] = flight
                                queue.push_back((next_city,new_fare,new_flights,arrival_time))

                        else:
                            if dept_time >= current_time + 20:
                                new_fare = current_fare + flight_fare
                                new_flights = current_flights + 1

                                if (new_flights < arrival_times[next_city]) or (new_flights == arrival_times[next_city] and new_fare < min_fare[next_city]):
                                    arrival_times[next_city] = new_flights
                                    min_fare[next_city] = new_fare
                                    parent_array[next_city] = current_city
                                    flights_used[next_city] = flight
                                    queue.push_back((next_city,new_fare,new_flights,arrival_time))
                except:
                    print(flight.start_city)
        


        if arrival_times[end_city] != float('inf'):
            route = []
            current_city = end_city
            while current_city and parent_array[current_city] != -1:
                route.append(flights_used[current_city])
                current_city = parent_array[current_city]
            
            return route[::-1]
        else:
            return []

