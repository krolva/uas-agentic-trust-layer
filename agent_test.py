import time
from dotenv import load_dotenv

load_dotenv()

from agent.drone_agent import drone_agent



def main():

    telemetry = """
Aircraft telemetry:

Aircraft: TEST1
Simulation time: 100.0 seconds
Latitude: 52.0000 degrees
Longitude: 3.0000 degrees
Altitude: 15000 feet
Track: 180 degrees
Ground speed: 300 knots
Vertical speed: 0 feet/minute
In conflict: false
"""

    start = time.perf_counter()

    result = drone_agent.run_sync(telemetry)

    elapsed = time.perf_counter() - start

    print("\nAgent output:")
    print(result.output)

    print(f"\nLatency: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()