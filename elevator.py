
from collections import deque
import heapq
import time
from enum import Enum 

class State(Enum):
    IDLE = 1 
    UP = 2 
    DOWN = 3
    EMERGENCY = 4

class ElevatorType(Enum):
    PASSENGER = 1
    SERVICE = 2

class RequestOrigin(Enum):
    INSIDE = 1 
    OUTSIDE = 2

class DoorState(Enum):
    OPEN = 1 
    CLOSED = 2 

# To req the elevator , user needs to press button from either inside or outside.
# This send request for passenger elevator

class Request:
    def __init__(self, origin, origin_floor, destination_floor=None):
        self.origin = origin
        self.direction = State.IDLE
        self.origin_floor = origin_floor
        self.destination_floor = destination_floor
        self.elevator_type = ElevatorType.PASSENGER 

        # If both origin and destination are provided 
        if destination_floor is not None:
            if origin_floor > destination_floor:
                self.direction = State.DOWN
            elif origin_floor < destination_floor:
                self.direction = State.UP

    def get_origin_floor(self):
        return self.origin_floor
    def get_destination_floor(self):
        return self.destination_floor
    def get_origin(self):
        return self.origin
    def get_direction(self):
        return self.direction
    # to determine order is within the heap
    def __lt__(self, other):
        #return self.destination_floor < other.destination_floor 
        # Check if self destination_floor is None
        if self.destination_floor is None:
            return False  # Treat None as greater than any int
        # Check if other destination_floor is None
        if other.destination_floor is None:
            return True  # Treat int as less than None
        # If neither is None, proceed with the original comparison
        return self.destination_floor < other.destination_floor
    
#This req is for service elevator

class ServiceRequest(Request):
    def __init__(self, origin, current_floor=None, destination_floor=None):
        if current_floor is not None and destination_floor is not None:
            super().__init__(origin, current_floor, destination_floor)
        else:
            super().__init__(origin, destination_floor)
        self.elevator_type = ElevatorType.SERVICE

# All the req will be handled here in the elevator class.

class Elevator:
    def __init__(self, current_floor, emergency_status):
        self.current_floor = current_floor
        self.state = State.IDLE
        self.emergency_status = emergency_status
        self.door_state = DoorState.CLOSED

    def open_door(self):
        self.door_state = DoorState.OPEN
        print(f"Open door on floor {self.current_floor}")

    def close_door(self):
        self.door_state = DoorState.CLOSED
        print("Closed doors")

    def wait_for_seconds(self, seconds):
        time.sleep(seconds)
    
    def operate(self):
        pass
    def process_emergency(self):
        pass
    def get_current_floor(self):
        return self.current_floor
    def get_state(self):
        return self.state
    def set_state(self, state):
        self.state = state
    def set_current_floor(self, floor):
        self.current_floor = floor
    def get_door_state(self):
        return self.door_state
    def set_emergency_status(self, status):
        self.emergency_status = status

# for individual passenger elevator

class PassengerElevator(Elevator):
    def __init__(self, current_floor, emergency_status):
        super().__init__(current_floor, emergency_status)
        self.passenger_up_queue = []
        self.passenger_down_queue = []

    def operate(self):
        while self.passenger_up_queue or self.passenger_down_queue:
            self.process_requests() 
        self.set_state(State.IDLE)
        print("Elevator is now ", self.get_state)

    def process_emergency(self):
        self.passenger_up_queue.clear()
        self.passenger_down_queue.clear()
        self.set_current_floor(1)
        self.set_state(State.IDLE)
        self.open_door()
        self.set_emergency_status(True)
        print("Queues cleared, current floor is ", self.get_current_floor())
    
    def add_up_request(self, request):
        if request.get_origin() == RequestOrigin.OUTSIDE:
            pick_up_request = Request(request.get_origin(), request.get_origin_floor(), request.get_origin_floor())
            heapq.heappush(self.passenger_up_queue, pick_up_request)
        heapq.heappush(self.passenger_up_queue, request)

    def add_down_request(self, request):
        if request.get_origin() == RequestOrigin.OUTSIDE:
            pick_up_request = Request(request.get_origin(), request.get_origin_floor(), request.get_origin_floor())
            heapq.heappush(self.passenger_down_queue, pick_up_request)
        heapq.heappush(self.passenger_down_queue, request)

    def process_up_requests(self):
        while self.passenger_up_queue:
            up_request = heapq.heappop(self.passenger_up_queue)
            if self.get_current_floor() == up_request.get_destination_floor():
                print("We are Currently on floor ",self.get_current_floor(),". Same as destination.")
                continue
            print("The current floor is", self.get_current_floor(), ". Next stop: ", up_request.get_destination_floor())
            try:
                print("Moving ", end="")
                for _ in range(3):
                    print(".", end="", flush=True)
                    time.sleep(0.5) 
                time.sleep(1) 
                print()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print("Error:", e)

            self.set_current_floor(up_request.get_destination_floor())
            print("Arrived at", self.get_current_floor())

            self.open_door()
            self.wait_for_seconds(3)
            self.close_door()
        print("All request completed.")
    
    def process_down_requests(self):
        while self.passenger_down_queue:
            down_request = heapq.heappop(self.passenger_down_queue)
            if self.get_current_floor() == down_request.get_destination_floor():
                print("Current on the same floor as destination, ",self.get_current_floor())
                continue
            print("The current floor is", self.get_current_floor(), ". Next stop: ", down_request.get_destination_floor())
            try:
                print("Moving ", end="")
                for _ in range(3):
                    print(".", end="", flush=True)
                    time.sleep(0.5)
                time.sleep(1)
                print()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print("Error:", e)
            
            self.set_current_floor(down_request.get_destination_floor())
            print("Arrived at", self.get_current_floor())

            self.open_door()
            self.wait_for_seconds(3)
            self.close_door()
        print("All request completed.")

    def process_requests(self):
        if self.get_state() == State.UP or self.get_state() == State.IDLE:
            self.process_up_requests()
            if self.passenger_down_queue:
                print("Now processing down requests")
                self.process_down_requests()
            else:
                self.process_down_requests()
                if self.passenger_up_queue:
                    print("Now processing up requests")
                    self.process_up_requests()

# Now a class for service elevator.

class ServiceElevator(Elevator):
    def __init__(self, current_floor, emergency_status):
        super().__init__(current_floor, emergency_status)
        self.service_queue = deque()

    def operate(self):
        while self.service_queue:
            curr_request = self.service_queue.popleft()
            print()
            print("CUrrently at", self.get_current_floor())
            try:
                time.sleep(1)
                print(curr_request.get_direction(), end="")
                for _ in range(3):
                    print(".", end="", flush=True)
                    time.sleep(0.5)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print("Error:", e)

            self.set_current_floor(curr_request.get_destination_floor())
            self.set_state(curr_request.get_direction())
            print("Arrivied at", self.get_current_floor())

            self.open_door()
            self.wait_for_seconds(3)
            self.close_door()
        self.set_state(State.IDLE)
        print("All request completed.")

    def add_request_to_queue(self, request):
        self.service_queue.append(request)

    def process_emergency(self):
        self.service_queue.clear()
        self.set_current_floor(1)
        self.set_state(State.IDLE)
        self.open_door()
        self.set_emergency_status(True)
        print("Queue cleared due to emergency.")

# Abstract the above instantiation using factory class.

class ElevatorFactory:
    @staticmethod
    def create_elevator(elevator_type: ElevatorType):
        if elevator_type == ElevatorType.PASSENGER:
            return PassengerElevator(1, False)
        elif elevator_type == ElevatorType.SERVICE:
            return ServiceElevator(1, False)
        else:
            return None
        
# Controller class is where user interacts with the elevator

class Controller:
    def __init__(self, factory):
        self.factory = factory
        self.passenger_elevator = factory.create_elevator(ElevatorType.PASSENGER)
        self.service_elevator = factory.create_elevator(ElevatorType.SERVICE)

    def send_passenger_up_requests(self, request):
        self.passenger_elevator.add_up_request(request)

    def send_passenger_down_requests(self, request):
        self.passenger_elevator.add_down_request(request)

    def send_service_request(self, request):
        self.service_elevator.add_request_to_queue(request)

    def handle_passenger_requests(self):
        self.passenger_elevator.operate()

    def handle_service_requests(self):
        self.service_elevator.operate()

    def handle_emergency(self):
        self.passenger_elevator.process_emergency()
        self.service_elevator.process_emergency()

class Main:
    @staticmethod
    def main():
        factory = ElevatorFactory()
        controller = Controller(factory)

        controller.send_passenger_up_requests(
            Request(RequestOrigin.OUTSIDE, 2, 4)
        )
        controller.send_passenger_down_requests(
            Request(RequestOrigin.OUTSIDE, 5, 6)
        )
        controller.send_passenger_up_requests(
            Request(RequestOrigin.OUTSIDE, 1, 6)
        )
        controller.handle_passenger_requests()

        controller.send_passenger_up_requests(
            Request(RequestOrigin.OUTSIDE, 1, 4)
        )
        controller.send_passenger_down_requests(
            Request(RequestOrigin.INSIDE, 6))
        controller.send_passenger_up_requests(
            Request(RequestOrigin.OUTSIDE, 8, 12)
        )
        controller.send_passenger_down_requests(
            Request(RequestOrigin.OUTSIDE, 1, 12)
        )
        controller.handle_passenger_requests()

        print("Now processing service requests")

        controller.send_service_request(
            ServiceRequest(RequestOrigin.INSIDE, 3))
        controller.send_service_request(
            ServiceRequest(RequestOrigin.OUTSIDE, 3, 1)
        )
        controller.send_service_request(
            ServiceRequest(RequestOrigin.INSIDE, 3, 5)
        )

        controller.handle_service_requests()

if __name__ == "__main__":
    Main.main()

        