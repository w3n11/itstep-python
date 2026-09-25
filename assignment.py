# Here implement your functions
class Human:
    def __init__(self, name: str | None = None) -> None:
        if name is None:
            self.name = "John Doe"
        else:
            self.name = name

    def __str__(self) -> str:
        return self.name


class Car:
    def __init__(self, brand: str, seats: int = 5) -> None:
        self.brand = brand
        self.seats = seats
        self.passengers: list[None | Human] = [None for _ in range(self.seats)]

    def add_passenger(self, passenger_name: str, seat: int | None = None) -> bool:
        if seat is None:
            for i in range(len(self.passengers)):
                if self.passengers[i] is None:
                    self.passengers[i] = Human(passenger_name)
                    return True
            return False

        try:
            if self.passengers[seat] is None:
                self.passengers[seat] = Human(passenger_name)
                return True
            return False
        except IndexError:
            return False

    def __str__(self) -> str:
        retval: str = f"{self.brand}\n"
        car_empty: bool = all(x is None for x in self.passengers)
        if not car_empty:
            for passenger in self.passengers:
                if passenger is None:
                    continue
                retval += f"  - {passenger}\n"
        else:
            retval += "  (the car is empty)"
        return retval.strip()


if __name__ == "__main__":
    # Here write your own tests
    pass
