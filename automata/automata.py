from abc import ABC, abstractmethod
from functools import wraps

from model import Model


def learn(function):
    """Décorateur destiné aux algorithmes d'apprentissage (ML/DL)."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper

class AutomataConfig(ABC):

    def __init__(self, automata_cfg):
        self.config = automata_cfg

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = self.load_cfg(config)

    @abstractmethod
    def load_cfg(self, config):
        """Charge, valide et retourne la configuration (ex: dict, namespace)."""


class Automata(ABC):

    def __init__(self, model: Model, name: str = "") -> None:
        self.__name = name
        self.__model = model
        self.__functionalities = {}

    def add_functionality(self, function_name: str, function):
        """Ajoute une fonctionnalité (un 'organe') à l'automate."""
        self.__functionalities[function_name] = function
        print(f"[Automata] Functionality '{function_name}' added to {self.__name}")

    def execute_functionality(self, function_name: str, *args):
        """Exécute une fonctionnalité enregistrée."""
        if function_name in self.__functionalities:
            return self.__functionalities[function_name](*args)
        else:
            raise ValueError(f"Functionality '{function_name}' not found.")

    def train(self):
        # Implement your own abstraction here
        pass

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, val):
        if isinstance(val, Model):
            # Correction : modification directe de l'attribut privé
            # pour éviter la récursion infinie
            self.__model = val

    def config(self):
        # Implement your own abstraction here
        pass
