from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from agent.drone_agent import drone_agent
from models.action import ProposedAction


class AgentWorker(QObject):

    action_ready = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

    @pyqtSlot(str)
    def run_agent(self, prompt: str):

        try:
            result = drone_agent.run_sync(prompt)

            action: ProposedAction = result.output

            self.action_ready.emit(action)

        except Exception as exc:
            self.error_occurred.emit(str(exc))