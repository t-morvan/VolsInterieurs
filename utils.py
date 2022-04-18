"""
Utils to load data and call the SNCF API
"""

import logging
from typing import Dict, Union, Tuple

import pandas as pd
import requests

URL_OSM = "https://nominatim.openstreetmap.org/search/"
URL_SNCF = "https://api.sncf.com/v1/coverage/sncf/journeys"
FR_BOX = [-7.382813, 41.129021, 11.403809, 51.082822]


class getDuration:
    """
    Compute journey duration between two stations given by their adminisrative code
    """

    def __init__(self, key: str, date: str) -> None:
        self.session = requests.Session()
        self.session.auth = (key, None)
        self.date = date

    def make_params(self, departure: str, arrival: str) -> Dict[str, Union[str, int]]:
        return {
            "datetime": self.date,
            "datetime_represents": "departure",
            "timeframe_duration": 86400,
            "from": f"admin:fr:{departure}",
            "to": f"admin:fr:{arrival}",
        }

    def compute(self, departure: str, arrival: str) -> float:
        params = self.make_params(departure, arrival)
        res = self.session.get(url=URL_SNCF, params=params)
        if res.status_code == 200:
            trajets = res.json()["journeys"]
            return min(trajet["duration"] for trajet in trajets)
        else:
            logging.warning(
                "SNCF API error %s : %s-%s", res.status_code, departure, arrival
            )
            return float("nan")


def get_flights() -> pd.DataFrame:
    #  lecture data
    flights = pd.read_csv("data/flights.csv")
    flights = flights.replace(":", 0)
    flights = flights[:-3]
    # sélection des vols intérieurs (dont DOM-TOM)
    flights = flights[flights.CODE.str.match(r"FR\_\w+\_FR\w+")]
    # avant 2001 pas de distinction entre Roissy et Orly, juste Airport System, Paris Airport
    flights["PAIR"] = flights["PAIR"].str.replace("airport SYSTEM - ", "")
    flights["PAIR"] = flights["PAIR"].str.replace("airport", "")
    # extraction arrivee/depart
    flights[["departure", "arrival"]] = flights["PAIR"].str.split(" - ", 1, expand=True)
    flights["departure"] = flights["departure"].str.slice(stop=-1)
    flights["arrival"] = flights["arrival"].str.slice(stop=-1)
    return flights


def get_stations() -> Dict[str, str]:
    # crée un dictionnaire aéroport - code administratif de la ville associée
    stations = pd.read_csv("data/gares.csv", dtype={"code": str}, index_col="aeroport")
    return stations["code"].to_dict()


def get_coords(place: str) -> Union[None, Tuple[float, float]]:
    params = {"q": place, "format": "json"}
    response = requests.get(URL_OSM, params=params).json()
    if response:
        return response[0]["lat"], response[0]["lon"]
    else:
        return None


def in_metro(lat: float, lon: float) -> bool:
    lon = float(lon)
    lat = float(lat)
    return (lon > FR_BOX[0]) & (lat > FR_BOX[1]) & (lon < FR_BOX[2]) & (lat < FR_BOX[3])
