"""Model class abstraction for AI Model used in the embedded stack."""

from abc import ABC, abstractmethod


class ModelConfig(ABC):

    def __init__(self, model_cfg):
        self.config = model_cfg

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = self.load_cfg(config)

    @abstractmethod
    def load_cfg(self, config):
        """Charge, valide et retourne la configuration (ex: dict, namespace)."""


class Model(ABC):

    def __init__(self, model_cfg: ModelConfig):
        # On stocke l'objet de configuration avec un nom explicite
        self.config_manager = model_cfg

        # Raccourci pour accéder directement aux données de configuration nettoyées
        self.config = model_cfg.config

        # Attribut qui contiendra le modèle chargé en mémoire (ONNX, TFLite, etc.)
        self.runtime_model = None

    @abstractmethod
    def load_model(self):
        """Alloue la mémoire et charge les poids du modèle sur la cible embarquée."""

    @abstractmethod
    def predict(self, input_data):
        """Exécute l'inférence sur le matériel embarqué."""
