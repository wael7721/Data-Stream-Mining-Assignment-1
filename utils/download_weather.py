"""
download_weather.py
-------------------
Download hourly historical weather from Open-Meteo for one or more Portuguese
cities and save ONE CSV PER CITY in the data/ folder.

Usage as a function:
    from download_weather import download_weather
    paths = download_weather(["Funchal", "Lisboa"])                  # 2018-01-01 -> 7 days ago
    paths = download_weather(["Funchal", "Lisboa"], "2018-01-01", "2025-12-31")

Usage from the command line:
    python download_weather.py Funchal Lisboa
    python download_weather.py Funchal Lisboa --start 2018-01-01 --end 2025-12-31

Output columns (hourly, chronological, no rows dropped or altered):
    time, temperature, relative_humidity, precipitation, wind_speed
Units: degC, %, mm, km/h (Open-Meteo defaults).
"""

from __future__ import annotations
import os
import argparse
import time
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://archive-api.open-meteo.com/v1/archive"

# Open-Meteo variable name -> column name used in the report/handbook
VARIABLES = {
    "temperature_2m": "temperature",
    "relative_humidity_2m": "relative_humidity",
    "precipitation": "precipitation",
    "wind_speed_10m": "wind_speed",
}

# The 25 cities of the PA01-PA50 catalogue: name -> (latitude, longitude)
CITY_COORDS = {
    "Lisboa": (38.7223, -9.1393),
    "Funchal": (32.6669, -16.9241),
}

def _year_chunks(start: date, end: date):
    """Split [start, end] into calendar-year chunks (keeps each request small)."""
    cur = start
    while cur <= end:
        chunk_end = min(date(cur.year, 12, 31), end)
        yield cur, chunk_end
        cur = chunk_end + timedelta(days=1)


def _fetch_chunk(lat, lon, start, end, timezone, retries=5, pause=2.0) -> pd.DataFrame:
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "hourly": ",".join(VARIABLES),
        "timezone": timezone,
    }
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(API_URL, params=params, timeout=60)
            if resp.status_code == 200:
                hourly = resp.json()["hourly"]
                df = pd.DataFrame(hourly)
                df["time"] = pd.to_datetime(df["time"])
                return df.rename(columns=VARIABLES)
            if resp.status_code in (429, 500, 502, 503, 504):
                last_error = f"HTTP {resp.status_code}"
            else:  # 400 etc.: not worth retrying
                raise RuntimeError(f"Open-Meteo error {resp.status_code}: {resp.text[:300]}")
        except requests.RequestException as exc:
            last_error = str(exc)
        time.sleep(pause * attempt)  # simple backoff
    raise RuntimeError(f"Open-Meteo request failed after {retries} attempts: {last_error}")


def download_weather(
    cities,
    start_date: str = "2018-01-01",
    end_date: str | None = None,
    data_dir: str | Path = "../data/",
    timezone: str = "UTC",
) -> dict[str, Path]:
    """
    Download hourly weather for each city and save one CSV per city.

    Parameters
    ----------
    cities     : list of city names (see CITY_COORDS), e.g. ["Funchal", "Lisboa"].
                 A single string is also accepted.
    start_date : "YYYY-MM-DD", default "2018-01-01".
    end_date   : "YYYY-MM-DD". Default None = 7 days ago (the archive lags a few
                 days). For reproducibility, pass a fixed date and record it.
    data_dir   : output folder (created if missing), default "data".
    timezone   : same value for every city so timestamps align. Default "UTC".

    Returns
    -------
    dict {city name: path of the saved CSV}
    """
    if isinstance(cities, str):
        cities = [cities]

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = (
        datetime.strptime(end_date, "%Y-%m-%d").date()
        if end_date
        else date.today() - timedelta(days=7)
    )
    if start > end:
        raise ValueError(f"start_date ({start}) is after end_date ({end}).")

    out_dir = Path(data_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    paths: dict[str, Path] = {}
    for city in cities:
        
        if os.path.exists(path):
            print(f"[{city}] Data already exists at {path}. Skipping download.")
            paths[city] = path
            continue
    
        lat, lon = CITY_COORDS[city]
        print(f"[{city}] downloading {start} -> {end} (lat={lat}, lon={lon}, tz={timezone})")

        frames = [
            _fetch_chunk(lat, lon, s, e, timezone) for s, e in _year_chunks(start, end)
        ]
        df = pd.concat(frames, ignore_index=True).sort_values("time").reset_index(drop=True)

        path = os.path.join(out_dir, f"{city}.csv")
        df.to_csv(path, index=False)
        paths[city] = path

        # Report only; nothing is dropped or modified.
        n_missing = int(df[list(VARIABLES.values())].isna().sum().sum())
        n_dupes = int(df["time"].duplicated().sum())
        print(
            f"[{city}] saved {len(df)} rows to {path} "
            f"({df['time'].min()} .. {df['time'].max()}, "
            f"{n_missing} missing values, {n_dupes} duplicate timestamps)"
        )

    return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Open-Meteo hourly weather per city.")
    parser.add_argument("cities", nargs="+", help='e.g. Funchal Lisboa (quote names with spaces)')
    parser.add_argument("--start", default="2018-01-01", help="YYYY-MM-DD (default 2018-01-01)")
    parser.add_argument("--end", default=None, help="YYYY-MM-DD (default: 7 days ago)")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--timezone", default="UTC")
    args = parser.parse_args()
    download_weather(args.cities, args.start, args.end, args.data_dir, args.timezone)