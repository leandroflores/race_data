import matplotlib.pyplot as plt

from functools import reduce
from project_1.formula_1.models import Season
from project_1.formula_1.readers import DataReader

def main() -> None:
    
    driver_id: str = input("Type driver code [3 letters]: ")

    
    years: list[int] = []
    points: list[int] = []
    
    for year in range(1997, 2024):
        print(year)
        reader: DataReader = DataReader(year)
        season: Season = reader.read_season()

        driver_result: dict = season.driver_races(driver_id)
        if len(driver_result) > 0:
            years.append(year)
            points.append(
                reduce(
                    lambda points, position: points + position.points,
                    driver_result,
                    0
                ),
            )
            

        # print(driver_result)

    print(years)
    print(points)

    # results: dict = season.constructor_classification()

    # drivers: list[str] = [result["constructor"] for result in results]
    # points: list[str] = [result["points"] for result in results]

    # print(drivers)
    # print(points)

    # plt.bar(drivers, points)

    # plt.title(f"Constructor's Result {year}")
    # plt.xlabel("Constructors")
    # plt.ylabel("Points")

    # plt.show()

main()