import matplotlib.pyplot as plt

from project_1.formula_1.models import Season
from project_1.formula_1.readers import DataReader

def main() -> None:
    
    year: int = int(input("Type session year: "))

    reader: DataReader = DataReader(year)
    season: Season = reader.read_season()

    results: dict = season.driver_classification()

    drivers: list[str] = [result["driver"] for result in results]
    points: list[str] = [result["points"] for result in results]

    print(drivers)
    print(points)

    plt.bar(drivers, points)

    plt.title(f"Driver's Result {year}")
    plt.xlabel("Drivers")
    plt.ylabel("Points")

    plt.show()

main()