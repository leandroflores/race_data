import json
import os

from project_1.formula_1.models import (
    Circuit, 
    Constructor, 
    Driver,
    Race,
)

class DataReader:

    def __init__(self, year: int) -> None:
        self.folder: str = "database"
        self.year: int = year
        self.circuits: dict[str, Circuit] = self._read_circuits()
        self.drivers: dict[int, Driver] = self._read_circuits()
        
    def _read_race(self, round: int) -> Race:
        race: Race = Race()
        try:
            file_path: str = f"{self.folder}/{self.year}/{self.year}_{round}.json"
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    response: dict = json.loads(file.read())
            race_data: dict = response["MRData"]["RaceTable"]["Races"][0]
            race.circuit = 
        except Exception:
            return race
            
    
    def _read_circuits(self) -> dict[str, Circuit]:
        try:
            circuits: dict[str, dict] = {}
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
        
    def _read_constructors(self) -> dict[str, Constructor]:
        try:
            constructors: dict[str, Constructor] = {}
            response: dict = {}
            file_path: str = f"{self.folder}/{self.year}/constructors_{self.year}.json"
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    response = json.loads(file.read())
            constructor_data: dict = response["MRData"]
            for data in constructor_data["ConstructorTable"]["Constructors"]:
                constructor: Constructor = Constructor.from_dict(data)
                constructors[constructor.id] = constructor
            return constructors
        except Exception:
            return {}
        
    

        

def main() -> None:
    print(DataReader(2020)._read_constructors())

main()