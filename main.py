from PyQt6.QtCore import QCoreApplication, QTimer

import bluesky as bs
from bluesky.network.client import Client

from adapters.bluesky_adapter import BlueSkyAdapter


def main():

    app = QCoreApplication([])

    # Initialize BlueSky library as an external client
    bs.init(mode="client")

    # Our integration layer
    adapter = BlueSkyAdapter()

    # BlueSky network client
    client = Client()

    network_timer = QTimer()
    network_timer.timeout.connect(client.update)
    network_timer.start(20)

    client.connect()

    print("Connected to BlueSky.")

    # Print aircraft state once per second
    def show_state():

        aircraft = adapter.get_all_telemetry()

        if not aircraft:
            print("Waiting for aircraft telemetry...")
            return

        print("\n--- Current Aircraft ---")

        for telemetry in aircraft:
            print(telemetry)

    state_timer = QTimer()
    state_timer.timeout.connect(show_state)
    state_timer.start(1000)

    app.exec()


if __name__ == "__main__":
    main()