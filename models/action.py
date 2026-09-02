from enum import Enum

from pydantic import BaseModel


class ActionType(str, Enum):
    MAINTAIN = "maintain"
    CHANGE_HEADING = "change_heading"
    CHANGE_ALTITUDE = "change_altitude"
    CHANGE_SPEED = "change_speed"


class ProposedAction(BaseModel):
    aircraft_id: str
    action_type: ActionType
    value: float | None = None
    reason: str