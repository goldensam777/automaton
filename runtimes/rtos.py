# An abstraction code for the RTOS runtime environment used in the embedded stack.
# A RTOS implemented in Rust will be soon available to run the whole system as an OS.


#  _                                      _       _         
# | | ___ _   _ _ __ ___   __ _ ___      | | __ _| |__  ___ 
# | |/ _ \ | | | '_ ` _ \ / _` / __|_____| |/ _` | '_ \/ __|
# | |  __/ |_| | | | | | | (_| \__ \_____| | (_| | |_) \__ \
# |_|\___|\__,_|_| |_| |_|\__,_|___/     |_|\__,_|_.__/|___/

# Coming soon...

from abc import ABC, abstractmethod


class _OS(ABC):
    def __init__(self, _os_configs, **kwargs):
        self.name = "Automata RTOS Runtime"
        self.version = "1.0.0"
        self.supported_features = ["task_scheduling", "inter_task_communication", "timers"]

class _OSManager(ABC):
    def __init__(self, _os_configs, **kwargs):
        self.name = "Automata RTOS Manager"
        self.version = "1.0.0"
        self.supported_features = ["task_management", "resource_allocation", "system_monitoring"]
