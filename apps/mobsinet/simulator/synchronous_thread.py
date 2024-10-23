# GENERATED WITH HELP FROM CHATGPT

from datetime import datetime
from threading import Thread
from .global_vars import Global

class SynchronousThread(Thread):
    
    def __init__(self, runtime=None):
        super().__init__()
        self.number_of_rounds = 0
        self.runtime = runtime  # Se estiver no modo GUI, mantém a referência ao GUIRuntime
        self.refresh_rate = 1    # Taxa de atualização da GUI

    def run(self):
        Global.is_running = True
        Global.start_time = datetime.now()

        # TODO: Colocar código existente em network_simulator.py : run()
        
        Global.is_running = False
