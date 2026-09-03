from PyQt6.QtCore import QCoreApplication, QTimer, QThread, pyqtSignal, QObject

from dotenv import load_dotenv

load_dotenv()

from observability import configure_observability

configure_observability()

import bluesky as bs
from bluesky.network.client import Client

from adapters.bluesky_adapter import BlueSkyAdapter

from agent.worker import AgentWorker
from agent.telemetry_formatter import format_telemetry


class AgentTrigger(QObject):
    run = pyqtSignal(str)


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

    # -------------------------
    # Agent worker thread
    # -------------------------

    agent_thread = QThread()

    agent_worker = AgentWorker()
    agent_worker.moveToThread(agent_thread)

    agent_trigger = AgentTrigger()

    agent_trigger.run.connect(agent_worker.run_agent)

    agent_state = {
        "busy": False
    }

    def handle_action(action):
    
        agent_state["busy"] = False
    
        print("\n--- Agent Decision ---")
        print(action)
    
    def handle_error(error):
    
        agent_state["busy"] = False
    
        print("\n--- Agent Error ---")
        print(error)

    agent_worker.action_ready.connect(handle_action)
    agent_worker.error_occurred.connect(handle_error)

    agent_thread.start()

    # -------------------------
    # Agent decision loop
    # -------------------------

    def agent_decision():

        if agent_state["busy"]:
            print("[Agent still processing previous request]")
            return

        telemetry = adapter.get_all_telemetry()

        if not telemetry:
            return

        prompt = format_telemetry(telemetry)

        print("\nSending telemetry snapshot to agent...")

        agent_state["busy"] = True

        agent_trigger.run.emit(prompt)


    agent_timer = QTimer()
    agent_timer.timeout.connect(agent_decision)
    agent_timer.start(5000)

    # -------------------------
    # Debug telemetry output
    # -------------------------

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

    # -------------------------
    # Application
    # -------------------------

    exit_code = app.exec()

    agent_thread.quit()
    agent_thread.wait()

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())