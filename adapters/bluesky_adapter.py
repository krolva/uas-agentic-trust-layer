from bluesky.core import Base
from bluesky.network import subscriber
from bluesky.stack import stack

from models.telemetry import Telemetry
from models.action import ProposedAction, ActionType


METERS_TO_FEET = 3.28084
MPS_TO_KNOTS = 1.94384
MPS_TO_FPM = 196.8504

class BlueSkyAdapter(Base):

    def __init__(self):
        super().__init__()

        # Most recent telemetry for each aircraft
        self._latest_telemetry: dict[str, Telemetry] = {}

    @subscriber
    def acdata(self, data):
        """
        Called whenever BlueSky publishes aircraft state.
        """

        for i, aircraft_id in enumerate(data.id):

            telemetry = Telemetry(
                aircraft_id=aircraft_id,

                sim_time_s=float(data.simt),

                latitude_deg=float(data.lat[i]),
                longitude_deg=float(data.lon[i]),

                altitude_ft=float(data.alt[i]) * METERS_TO_FEET,

                track_deg=float(data.trk[i]),

                ground_speed_knots=float(data.gs[i]) * MPS_TO_KNOTS,
                vertical_speed_fpm=float(data.vs[i]) * MPS_TO_FPM,

                in_conflict=bool(data.inconf[i]),
            )

            self._latest_telemetry[aircraft_id] = telemetry
            
    def get_telemetry(self, aircraft_id: str) -> Telemetry | None:
        """
        Return the latest telemetry for one aircraft.
        """

        return self._latest_telemetry.get(aircraft_id)

    def get_all_telemetry(self) -> list[Telemetry]:
        """
        Return latest telemetry for all aircraft.
        """

        return list(self._latest_telemetry.values())

    def change_heading(self, aircraft_id: str, heading_deg: float):
        stack(f"HDG {aircraft_id} {heading_deg}")

    def change_altitude(self, aircraft_id: str, altitude_ft: float):
        stack(f"ALT {aircraft_id} {altitude_ft}")

    def change_speed(self, aircraft_id: str, speed_knots: float):
        stack(f"SPD {aircraft_id} {speed_knots}")

    def execute_action(self, action: ProposedAction):
        """
        Translate our internal action model into BlueSky commands.
        """

        if action.action_type == ActionType.MAINTAIN:
            return

        if action.value is None:
            raise ValueError(
                f"{action.action_type} requires a value"
            )

        if action.action_type == ActionType.CHANGE_HEADING:
            self.change_heading(
                action.aircraft_id,
                action.value,
            )

        elif action.action_type == ActionType.CHANGE_ALTITUDE:
            self.change_altitude(
                action.aircraft_id,
                action.value,
            )

        elif action.action_type == ActionType.CHANGE_SPEED:
            self.change_speed(
                action.aircraft_id,
                action.value,
            )

        else:
            raise ValueError(
                f"Unsupported action: {action.action_type}"
            )