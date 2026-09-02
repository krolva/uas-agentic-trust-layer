from PyQt6.QtCore import QCoreApplication, QTimer

import bluesky as bs
from bluesky.core import Base
from bluesky.network import subscriber
from bluesky.network.client import Client

from telemetry import Telemetry

METERS_TO_FEET = 3.28084
MPS_TO_KNOTS = 1.94384
MPS_TO_FPM = 196.8504

class TelemetryReader(Base):

    @subscriber
    def acdata(self, data):
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

            print(telemetry)

if __name__ == "__main__":

    app = QCoreApplication([])

    # Initialise BlueSky as an external client
    bs.init(mode="client")

    # Create our subscriber object
    reader = TelemetryReader()

    # Create BlueSky network client
    client = Client()

    # BlueSky communication is asynchronous,
    # so periodically process network messages
    timer = QTimer()
    timer.timeout.connect(client.update)
    timer.start(20)

    # Connect to the running BlueSky server
    client.connect()

    print("Connected. Waiting for BlueSky telemetry...")

    app.exec()