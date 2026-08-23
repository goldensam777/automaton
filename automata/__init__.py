"""Automata: Programmable automaton abstraction library for embedded AI systems."""

from .automata import Automata, AutomataConfig, learn
from .model import Model, ModelConfig

__all__ = [
    "Automata",
    "AutomataConfig",
    "learn",
    "Model",
    "ModelConfig",
]
