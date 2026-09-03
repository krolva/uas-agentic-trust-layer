import asyncio

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from agent.drone_agent import drone_agent
from models.action import ProposedAction


class AgentWorker(QObject):

    action_ready = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # One persistent asyncio event loop for this worker.
        # Every Pydantic AI / Gemini request will use this same loop.
        self._loop = asyncio.new_event_loop()

    @pyqtSlot(str)
    def run_agent(self, prompt: str):

        try:
            asyncio.set_event_loop(self.loop)

            result = self._loop.run_until_complete(
                drone_agent.run(prompt)
            )

            action: ProposedAction = result.output

            self.action_ready.emit(action)

        except Exception as exc:
            self.error_occurred.emit(str(exc))

    @pyqtSlot()
    def close(self):

        if not self._loop.is_closed():
            self._loop.close()