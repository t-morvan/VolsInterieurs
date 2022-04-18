import logging

import pandas as pd
import yaml
from tqdm import tqdm

from utils import getDuration, get_stations, get_coords, get_flights, in_metro


def main() -> None:

    # API params
    with open("config.yaml", "r", encoding="utf-8") as f:
        params_API = yaml.safe_load(f)

    # data
    flights = get_flights()
    stations = get_stations()

    # setup
    train_duration = getDuration(**params_API)
    logging.basicConfig(filename="data/geocode.log", level=logging.INFO)

    links = []
    for flight in tqdm(flights.itertuples(), total=flights.shape[0]):

        # geocode departure/arrival
        try:
            lat_d, lon_d = get_coords(flight.departure)
            lat_a, lon_a = get_coords(flight.arrival)
        except TypeError:
            logging.warning("Geocode error : %s-%s}", flight.departure, flight.arrival)
            continue

        # keep only metro flight
        if not in_metro(lat_d, lon_d) or not in_metro(lat_a, lon_a):
            continue

        # compute train duration
        departure_station = stations[flight.departure]
        arrival_station = stations[flight.arrival]
        duration = train_duration.compute(departure_station, arrival_station)

        links.append(
            {
                "departure": flight.departure,
                "arrival": flight.arrival,
                "lat_d": lat_d,
                "lon_d": lon_d,
                "lat_a": lat_a,
                "lon_a": lon_a,
                "duration": duration,
            }
        )

    links_df = pd.DataFrame(links)
    links_df = links_df.merge(flights, on=["departure", "arrival"])
    links_df.to_csv("data/links.csv")


if __name__ == "__main__":
    main()
