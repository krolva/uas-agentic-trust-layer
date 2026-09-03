from models.telemetry import Telemetry


def format_telemetry(telemetry: list[Telemetry]) -> str:

    lines = [
        "Current aircraft telemetry:",
        "",
    ]

    for aircraft in telemetry:

        lines.extend([
            f"Aircraft: {aircraft.aircraft_id}",
            f"Simulation time: {aircraft.sim_time_s:.1f} seconds",
            f"Latitude: {aircraft.latitude_deg:.6f} degrees",
            f"Longitude: {aircraft.longitude_deg:.6f} degrees",
            f"Altitude: {aircraft.altitude_ft:.0f} feet",
            f"Track: {aircraft.track_deg:.1f} degrees",
            f"Ground speed: {aircraft.ground_speed_knots:.1f} knots",
            f"Vertical speed: {aircraft.vertical_speed_fpm:.0f} feet/minute",
            f"BlueSky conflict detected: {aircraft.in_conflict}",
            "",
        ])

    return "\n".join(lines)