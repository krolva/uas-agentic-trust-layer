from pydantic import BaseModel, Field


class Telemetry(BaseModel):
    aircraft_id: str

    sim_time_s: float = Field(ge=0)

    latitude_deg: float = Field(ge=-90, le=90)
    longitude_deg: float = Field(ge=-180, le=180)

    altitude_ft: float

    track_deg: float = Field(ge=0, lt=360)

    ground_speed_knots: float = Field(ge=0)
    vertical_speed_fpm: float

    in_conflict: bool