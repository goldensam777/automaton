# AI Agent model for intelligent control of autonomous robots, drones, and vehicles.
# Note: This is an abstration, for the API manipulation.
# Define your model to use the API.

from abc import ABC, abstractmethod

from automata import Model, ModelConfig


class Cortex(Model):
    def __init__(self, config: ModelConfig):
        super().__init__(config)

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def predict(self, input_data: dict):
        pass