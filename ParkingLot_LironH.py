from datetime import datetime
import json
import os


def check_admin(username, password):
    return username == "admin" and password == "admin"


def get_login_from_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username, password


def admin_login():
    while True:
        username, password = get_login_from_user()
        if check_admin(username, password):
            return True
        elif username == "0" and password == "0":
            return False
        else:
            print("Unauthorized access. Please provide admin username and password.")


def save_parking_lot_data(parking_lot):
    data = {
        "max_capacity": parking_lot.max_capacity,
        "available_spaces": parking_lot.available_spaces,
        "hourly_rate": parking_lot.hourly_rate,
        "cars": {car_id: entry_time.isoformat() for car_id, entry_time in parking_lot.cars.items()}
    }
    with open("parking_lot_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


def load_parking_lot_data(parking_lot):
    try:
        with open("parking_lot_data.json", "r") as json_file:
            data = json.load(json_file)
            parking_lot.max_capacity = data["max_capacity"]
            parking_lot.hourly_rate = data["hourly_rate"]
            parking_lot.available_spaces = data["available_spaces"]
            parking_lot.cars = {car_id: datetime.fromisoformat(entry_time) for car_id, entry_time in
                                data["cars"].items()}
    except FileNotFoundError:
        pass


class Car:
    def __init__(self, car_id, car_type, phone_number):
        self.car_id = car_id
        self.car_type = car_type
        self.phone_number = phone_number
        self.entry_timestamp = None

    def enter_parking_lot(self):
        self.entry_timestamp = datetime.now()

    def __str__(self):
        entry_time_str: str = str(self.entry_timestamp) if self.entry_timestamp else "Not entered yet"
        return f"Car ID: {self.car_id}\nCar Type: {self.car_type}\nPhone Number: {self.phone_number}\n" \
               f"Entry Time: {entry_time_str}"


class ParkingLot:
    def __init__(self, max_capacity=1, hourly_rate=1):
        self.max_capacity = max_capacity
        self.hourly_rate = hourly_rate
        self.available_spaces = max_capacity
        self.cars = {}

    def park_car(self, car):
        if self.available_spaces > 0:
            if car.car_id not in self.cars:
                entry_time = datetime.now()
                self.cars[car.car_id] = entry_time
                self.available_spaces -= 1
                print(f"Car ID: {car.car_id}\nCar Type: {car.car_type}\nPhone Number: {car.phone_number}\n"
                      f"Entry Time: {entry_time} \nTo Liron's Parking Lot")  # f"Car {car_id} parked at {entry_time}"
            else:
                print("Car is already parked.")
        else:
            print("Parking lot is full.")

    def display_available_spaces(self):
        print(f"Available parking spaces: {self.available_spaces}/{self.max_capacity}")

    def calculate_parking_fee(self, car_id):
        if car_id in self.cars:
            entry_time = self.cars[car_id]
            exit_time = datetime.now()
            parked_duration = (exit_time - entry_time).total_seconds() / 3600  # in hours
            parking_fee = parked_duration * self.hourly_rate
            return parking_fee
        else:
            return None

    def remove_car(self, car_id):
        if car_id in self.cars:
            entry_time = self.cars[car_id]
            exit_time = datetime.now()
            parked_duration = (exit_time - entry_time).total_seconds() / 3600  # in hours
            parking_fee = self.calculate_parking_fee(car_id)
            print(f"Car {car_id} was parked for {parked_duration:.2f} hours.")
            print(f"Parking fee: ${parking_fee:.2f}")
            del self.cars[car_id]
            self.available_spaces += 1
        else:
            print("Car is not parked in the lot.")

    def change_hourly_rate(self, new_rate):
        self.hourly_rate = new_rate
        print(f"Hourly rate changed to ${new_rate:.2f}")

    def change_max_capacity(self, new_capacity):
        self.max_capacity = new_capacity
        self.available_spaces = new_capacity
        print(f"Max capacity changed to {new_capacity}")

    def reset_parking_lot(self):
        try:
            os.remove("parking_lot_data.json")
        except FileNotFoundError:
            pass
        self.max_capacity = 0
        self.available_spaces = 0
        self.hourly_rate = 0
        self.cars = {}
        print("Parking lot reset.")

    def generate_current_parking_report(self):
        print("Current parked cars:")
        for car_id, entry_time in self.cars.items():
            print(f"Car {car_id} parked at {entry_time}")

    def generate_long_term_parking_report(self):
        print("Cars parked for more than 24 hours:")
        current_time = datetime.now()
        for car_id, entry_time in self.cars.items():
            parked_duration = (current_time - entry_time).total_seconds() / 3600  #
            if parked_duration > 24:
                print(f"Car {car_id} parked for {parked_duration:.2f} hours.")


parking_lot = ParkingLot(max_capacity=50, hourly_rate=5)
load_parking_lot_data(parking_lot)

while True:
    print("\nOptions:")
    print("1. Park a car")
    print("2. Show Hourly Rate and Available Spaces")
    print("3. Remove a car")
    print("4. Change hourly rate")
    print("5. Change max capacity")
    print("6. Reset parking lot")
    print("7. Generate current parking report")
    print("8. Generate long-term parking report")
    print("9. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        try:
            while True:
                car_id = input("Enter car ID: ")
                car_id = car_id.replace(" ", "").replace("-", "")
                if car_id.isdigit() and len(car_id) > 6:
                    break
                else:
                    print("Invalid car id, please enter at least 7 digit.")
            while True:
                car_type = input("Enter car type (Privet, Van, Public): ").lower()
                if car_type in ["privet", "van", "public"]:
                    break
                else:
                    print("Invalid car type. Please choose Privet, Van, or Public.")

            while True:
                phone_number = input("Enter phone number: ")
                phone_number = phone_number.replace(" ", "").replace("-", "")
                if phone_number.isdigit() and len(phone_number) == 10:
                    break
                else:
                    print("Invalid phone number. Please enter exactly 10 digits.")
            car = Car(car_id, car_type, phone_number)
            car.enter_parking_lot()
            parking_lot.park_car(car)
            save_parking_lot_data(parking_lot)
        except ValueError:
            print("Invalid input. Please enter a valid car ID.")

    elif choice == "2":
        print(f"Hourly Rate: ${parking_lot.hourly_rate:.2f}")
        parking_lot.display_available_spaces()

    elif choice == "3":
        car_id = input("Enter car ID: ")
        parking_lot.remove_car(car_id)
        save_parking_lot_data(parking_lot)

    elif choice == "4" or choice == "5" or choice == "6":
        print("Press 0 to go back to main menu")
        if admin_login():
            if choice == "4":
                try:
                    new_rate = float(input("Enter new hourly rate: "))
                    parking_lot.change_hourly_rate(new_rate)
                    save_parking_lot_data(parking_lot)
                except ValueError:
                    print("Invalid input. Please enter a valid hourly rate.")
            elif choice == "5":
                try:
                    new_capacity = int(input("Enter new max capacity: "))
                    parking_lot.change_max_capacity(new_capacity)
                    save_parking_lot_data(parking_lot)
                except ValueError:
                    print("Invalid input. Please enter a valid max capacity.")
            elif choice == "6":
                parking_lot.reset_parking_lot()
                save_parking_lot_data(parking_lot)

    elif choice == "7":
        parking_lot.generate_current_parking_report()

    elif choice == "8":
        parking_lot.generate_long_term_parking_report()

    elif choice == "9":
        save_parking_lot_data(parking_lot)
        print("Thank you for using Liron's parking lot, \nSee you soon!")
        break
    else:
        print("Invalid choice. Please try again.")
