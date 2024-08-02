import json
import os
import requests

class ImportData:
    
    def __init__(self, year: int) -> None:
        self.url_base: str = "http://ergast.com/api/f1"
        self.folder: str = "database"
        self.year: int = year

    def _create_file(self, model: str) -> bool:
        try:
            url: str = f"{self.url_base}/{self.year}/{model}s.json"
            path: str = f"{self.folder}/{self.year}/{model}s_{self.year}.json"
            response: requests.Response = requests.get(url)
            data: str = json.dumps(response.json())
            with open(path, "w") as file:
                file.write(data)
            return True
        except Exception:
            return False
        
    def create_season_file(self) -> bool:
        try:
            folder_path: str = f"{self.folder}/{self.year}"
            if not os.path.isdir(folder_path):
                os.makedirs(folder_path)

                url: str = f"{self.url_base}/{self.year}.json"
                path: str = f"{self.folder}/{self.year}/{self.year}.json"
                response: requests.Response = requests.get(url)
                data: str = response.json()
                rounds: int = int(data["MRData"]["total"])
                if not os.path.isfile(path):
                    with open(path, "w") as file:
                        file.write(json.dumps(data))
                
                self._create_race_files(rounds)
                self._create_circuit_file()
                self._create_driver_file()
                self._create_constructor_file()

            return True
        except Exception:
            return False

    def _create_race_files(self, rounds: int) -> None:
        for round in range(1, rounds + 1):
            self._create_race_file(round)

    def _create_race_file(self, round: int) -> bool:
        try:
            url: str = f"{self.url_base}/{self.year}/{round}/results.json"
            path: str = f"{self.folder}/{self.year}/{self.year}_{round}.json"
            response: requests.Response = requests.get(url)
            data: str = json.dumps(response.json())
            if not os.path.isfile(path):
                with open(path, "w") as file:
                    file.write(data)
            return True
        except Exception:
            return False

    def _create_constructor_file(self) -> bool:
        return self._create_file("constructor")
    
    def _create_driver_file(self) -> bool:
        return self._create_file("driver")
    
    def _create_circuit_file(self) -> bool:
        return self._create_file("circuit")


def main() -> None:
    years: range[int] = range(2010, 2024)
    for year in years:
        print(year)
        ImportData(year).create_season_file()

main()