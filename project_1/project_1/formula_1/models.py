from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from itertools import chain

@dataclass
class Constructor:
    id: str
    name: str
    country: str
    url: str

    @staticmethod
    def from_dict(adict: dict) -> "Constructor":
        return Constructor(
            adict.get("constructorId", None),
            adict.get("name", None),
            adict.get("nationality", None),
            adict.get("url", None)
        )
    
    def __repr__(self) -> str:
        return self.id
    
@dataclass
class Circuit:
    id: str
    name: str
    city: str
    country: str
    url: str

    @staticmethod
    def from_dict(adict: dict) -> "Circuit":
        return Circuit(
            adict.get("circuitId", None),
            adict.get("circuitName", None),
            adict.get("Location", {}).get("locality", None),
            adict.get("Location", {}).get("country", None),
            adict.get("url", None)
        )
    
    @property
    def location(self) -> str:
        return f"{self.city} - {self.country}"
    
    def __repr__(self) -> str:
        return self.id

@dataclass
class Driver:
    number: int
    code: str
    identifier: str
    first_name: str
    last_name: str
    birth_data: str
    nationality: str
    url_page: str
    
    @staticmethod
    def from_dict(adict: dict) -> "Driver":
        return Driver(
            int(adict.get("permanentNumber", 0)),
            adict.get("code", None),
            adict.get("driverId", None),
            adict.get("givenName", None),
            adict.get("familyName", None),
            adict.get("dateOfBirth", None),
            adict.get("nationality", None),
            adict.get("url", None)
        )
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
        
    def __repr__(self) -> str:
        return self.identifier

@dataclass
class RacePosition:
    driver: Driver
    constructor: Constructor
    position: int
    grid: int
    points: float
    time: str
    time_in_ms: float
    status: str

    def __init__(
            self, 
            driver: Driver,
            constructor: Constructor,
            data: dict,
        ) -> None:
        self.driver = driver
        self.constructor = constructor
        self.position = int(data.get("position", 0))
        self.grid = int(data.get("grid", 0))
        self.points = float(data.get("points", 0))
        self.time = self._time(data)
        self.time_in_ms = self._time_in_ms(data)
        self.status = data.get("status", None)

    def _time(self, data: dict) -> None:
        try:
            return data["Time"]["time"]
        except Exception:
            return ""
        
    def _time_in_ms(self, data: dict) -> None:
        try:
            return float(data["Time"]["millis"])
        except Exception:
            return float("inf")
        
    @property
    def details(self) -> str:
        return f"{self.position} - {self.driver.code} = {self.points}"
        
    def __str__(self) -> str:
        return f"{self.driver} - {self.position} - {self.time} ({self.status})"

@dataclass
class Race:
    circuit: Circuit
    date: str
    round: str
    positions: list[RacePosition]

    def __init__(self) -> None:
        self.positions = []

    def classification(self) -> list[RacePosition]:
        return sorted(deepcopy(self.positions), key=lambda driver: driver.position)
    
    def details(self) -> None:
        for position in self.classification():
            print(position.details)

    def driver_races(self, driver_id: str) -> list[RacePosition]:
        return list(
            filter(
                lambda race_position: race_position.driver.code == driver_id,
                self.positions
            )
        )
    
    def constructor_races(self, constructor_id: str) -> list[RacePosition]:
        return list(
            filter(
                lambda race_position: race_position.constructor.id == constructor_id,
                self.positions
            )
        )

    def __repr__(self) -> str:
        return self.circuit.name + " - " + self.date

@dataclass
class Season:
    year: str
    rounds: int
    races: list[Race]
    drivers: dict[int, Driver]
    circuits: dict[str, Circuit]
    constructors: dict[str, Constructor]

    def __init__(self) -> None:
        self.races: list[Race] = []
        self.drivers: dict[int, Driver] = []
        self.circuits: dict[str, Circuit] = []
        self.constructors: dict[str, Constructor] = []
    
    def driver_classification(self) -> dict:
        classification: list[dict] = []
        for driver in self.drivers.keys():
            driver_id: str = self.drivers[driver].code
            positions: list["RacePosition"] = self.driver_races(driver_id)
            classification.append(
                {
                    "driver": driver_id,
                    "points": reduce(
                        lambda points, position: points + position.points,
                        positions,
                        0
                    ),
                    "positions": self.grid_positions(driver_id),
                }
            )
        return sorted(classification, key=lambda driver: driver["points"], reverse=True)
    
    def constructor_classification(self) -> dict:
        classification: list[dict] = []
        for constructor in self.constructors.keys():
            constructor: str = self.constructors[constructor].id
            positions: list["RacePosition"] = self.constructor_races(constructor)
            classification.append(
                {
                    "constructor": constructor,
                    "points": reduce(
                        lambda points, position: points + position.points,
                        positions,
                        0
                    ),
                }
            )
        return sorted(classification, key=lambda driver: driver["points"], reverse=True)

    def driver_races(self, driver_id: str) -> list["RacePosition"]:
        return list(
            chain.from_iterable(
                race.driver_races(driver_id) for race in self.races
            )
        )
    
    def constructor_races(self, constructor_id: str) -> list["RacePosition"]:
        return list(
            chain.from_iterable(
                race.constructor_races(constructor_id) for race in self.races
            )
        )
    
    def grid_positions(self, driver_id: str) -> list[int]:
        return [race.position for race in self.driver_races(driver_id)]
