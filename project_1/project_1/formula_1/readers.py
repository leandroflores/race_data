import json
import os

from project_1.formula_1.models import Circuit, Driver

class DataReader:

    def __init__(self, year: int) -> None:
        self.folder: str = "database"
        self.year: int = year
        

    def _read_drivers(self) -> dict[int, Driver]:
        try:
            drivers: dict[int, Driver] = {}
            response: dict = {}
            file_path: str = f"{self.folder}/{self.year}/drivers_{self.year}.json"
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    response: dict = json.loads(file.read())
            driver_data: dict = response["MRData"]
            for data in driver_data["DriverTable"]["Drivers"]:
                driver: Driver= Driver.from_dict(data)
                drivers[driver.number] = driver
            return drivers
        except Exception:
            return {}
        
    def _read_circuits(self) -> dict[int, Circuit]:
        try:
            circuits: dict[int, dict] = {}
            response: dict = {}
            file_path: str = f"{self.folder}/{self.year}/circuits_{self.year}.json"
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    response: dict = json.loads(file.read())
            circuit_data: dict = response["MRData"]
            for data in circuit_data["CircuitTable"]["Circuits"]:
                print(data)
                circuit: Circuit = Circuit.from_dict(data)
                circuits[circuit.id] = circuit
            return circuits
        except Exception:
            return {}

        

def main() -> None:
    print(DataReader(2020)._read_circuits())

main()