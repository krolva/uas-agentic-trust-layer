from PyQt6.QtCore import QCoreApplication, QTimer

import bluesky as bs
from bluesky.core import Base
from bluesky.network import subscriber
from bluesky.network.client import Client

METERS_TO_FEET = 3.28084
MPS_TO_KNOTS = 1.94384
MPS_TO_FPM = 196.8504

class TelemetryReader(Base):

    @subscriber
    def acdata(self, data):
        for i, aircraft_id in enumerate(data.id):

            altitude_ft = data.alt[i] * METERS_TO_FEET
            ground_speed_knots = data.gs[i] * MPS_TO_KNOTS
            vertical_speed_fpm = data.vs[i] * MPS_TO_FPM

            print("\n--- Aircraft State ---")
            print(f"Aircraft: {aircraft_id}")
            print(f"Latitude: {data.lat[i]:.6f}")
            print(f"Longitude: {data.lon[i]:.6f}")
            print(f"Altitude: {altitude_ft:.0f} ft")
            print(f"Track: {data.trk[i]:.1f}°")
            print(f"Ground Speed: {ground_speed_knots:.1f} kt")
            print(f"Vertical Speed: {vertical_speed_fpm:.0f} ft/min")
            print(f"Simulation Time: {data.simt:.1f} s")
            print(f"In Conflict: {bool(data.inconf[i])}")
            print("----------------------")

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