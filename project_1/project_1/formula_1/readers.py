import json
import os

from project_1.formula_1.models import (
    Circuit, 
    Constructor, 
    Driver,
    Race,
    RacePosition,
    Season,
)

class DataReader:

    def __init__(self, year: int) -> None:
        self.folder: str = "database"
        self.year: int = year
        self.circuits: dict[str, Circuit] = self._read_circuits()
        self.drivers: dict[int, Driver] = self._read_drivers()
        self.constructors: dict[str, Constructor] = self._read_constructors()

    def read_season(self) -> Season:
        try:
            file_path: str = f"{self.folder}/{self.year}/{self.year}.json"
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    response = json.loads(file.read())

            response_data: dict = response["MRData"]
            season: Season = Season()
            season.year = self.year
            season.rounds = int(response_data["total"])
            season.races = [
                self._read_race(round) 
                for round in range(1, season.rounds + 1)
            ]
            season.circuits = self.circuits
            season.drivers = self.drivers
            season.constructors = self.constructors

            return season
        except Exception as e:
            import traceback
            traceback.print_exc(e)
            return None
        
    def _read_race(self, round: int) -> Race:
        race: Race = Race()
        file_path: str = f"{self.folder}/{self.year}/{self.year}_{round}.json"
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                response: dict = json.loads(file.read())
        race_data: dict = response["MRData"]["RaceTable"]["Races"][0]
        race.circuit = self.circuits[race_data["Circuit"]["circuitId"]]
        race.date = race_data.get("date", "")
        race.round = race_data.get("round", "")
        race.positions = self._read_race_positions(race_data)
        return race
        
    def _read_race_positions(self, race_data: dict) -> list[RacePosition]:
        positions: list[RacePosition] = []
        for lap_data in race_data["Results"]:
            # print("0" * 50)
            # print(lap_data)
            # print("0" * 50)
            driver_id: str = lap_data["Driver"]["driverId"]
            constructor_id: str = lap_data["Constructor"]["constructorId"]
            positions.append(
                RacePosition(
                    self.drivers[driver_id],
                    self.constructors[constructor_id],
                    lap_data,
                )
            )
        return positions
    
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
                circuit: Circuit = Circuit.from_dict(data)
                circuits[circuit.id] = circuit
            return circuits
        except Exception:
            return {}

    def _read_drivers(self) -> dict[str, Driver]:
        try:
            drivers: dict[str, Driver] = {}
            response: dict = {}
            file_path: str = f"{self.folder}/{self.year}/drivers_{self.year}.json"
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    response: dict = json.loads(file.read())
            driver_data: dict = response["MRData"]
            for data in driver_data["DriverTable"]["Drivers"]:
                print(data["driverId"])
                driver: Driver= Driver.from_dict(data)
                drivers[driver.identifier] = driver
                print(drivers)
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
    import time
    reader: DataReader = DataReader(2004)
    season: Season = reader.read_season()
    print(season.drivers)
    print("=" * 50)
    print(season.driver_classification())
    # print("=" * 50)
    # print(season.races[0].details())
    # print("#" * 50)
    # for race in season.races:
    #     print(race.circuit.location)
    #     print(race.details())
    #     print("#" * 50)
    #     time.sleep(5)
    #     print(race.positions)
    #     print("")

main()