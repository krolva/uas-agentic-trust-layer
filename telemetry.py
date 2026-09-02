from dataclasses import dataclass


@dataclass
class Telemetry:
    aircraft_id: str
    sim_time_s: float

    latitude_deg: float
    longitude_deg: float

    altitude_ft: float
    track_deg: float

    ground_speed_knots: float
    vertical_speed_fpm: float

    in_conflict: bool