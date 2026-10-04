# Here write your code
class Human():
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name


class Car:
    def __init__(self, brand: str, seats: int = 5) -> None:
        self.brand = brand
        self.seats = seats
        self.passengers: list[None | Human] = [None] * self.seats

    def add_passenger(self, passenger_name: str, seat: int | None = None) -> bool:
        if seat is None:
            for i in range(self.seats):
                if self.passengers[i] is None:
                    self.passengers[i] = Human(passenger_name)
                    return True
            return False
        try:
            if self.passengers[seat] is None:
                self.passengers[seat] = Human(passenger_name)
                return True
        except IndexError:
            return False
        return False

    def __str__(self) -> str:
        retval: str = f"{self.brand}\n"
        for passenger in self.passengers:
            if passenger is None:
                retval += "  - (empty seat)\n"
            else:
                retval += f"  - {passenger}\n"
        return retval.strip()


if __name__ == "__main__":
    # Here write your own tests
    pass
