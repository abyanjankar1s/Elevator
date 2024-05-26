# Elevator
Object Oriented Programming: Designing Elevator

 # DEMO 

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

        

            We are Currently on floor  1 . Same as destination.
            The current floor is 1 . Next stop:  2
            Moving ...
            Arrived at 2
            Open door on floor 2
            Closed doors
            The current floor is 2 . Next stop:  4
            Moving ...
            Arrived at 4
            Open door on floor 4
            Closed doors
            The current floor is 4 . Next stop:  6
            Moving ...
            Arrived at 6
            Open door on floor 6
            Closed doors
            All request completed.
            Now processing down requests
            The current floor is 6 . Next stop:  5
            Moving ...
            Arrived at 5
            Open door on floor 5
            Closed doors
            The current floor is 5 . Next stop:  6
            Moving ...
            Arrived at 6
            Open door on floor 6
            Closed doors
            All request completed.


