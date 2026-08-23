======================================================================
Automaton Universale
======================================================================
*A Programmable Automata Abstraction Framework for Embedded AI Systems*

.. image:: https://img.shields.io/badge/Python-3.9+-blue.svg
   :alt: Python Version
.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :alt: License
.. image:: https://img.shields.io/badge/Domain-Edge%20AI%20%7C%20Robotics-orange.svg
   :alt: Domain

Overview
========

**Automaton Universale** is a lightweight, hardware-agnostic abstraction library designed to bridge **Embedded Artificial Intelligence** (Edge AI) and **Deterministic Cyber-Physical Control**.

In mission-critical autonomous systems (e.g., micro-aerial vehicles, planetary rovers, edge medical devices), probabilistic neural network outputs must interface with deterministic actuators and safety guardrails. This library formalizes this interaction through a modular **Perception-Decision-Action** architecture.

Key Features
============

* **Decoupled Model Abstraction (``Model`` & ``ModelConfig``)**:
  Uniform interface for embedded inference runtimes (TensorFlow Lite Micro, ONNX Runtime, TensorRT, or custom C/C++ backends) without coupling logic to hardware specifics.
* **Modular Organ & Actuator Dispatching (``Automata``)**:
  Dynamic registration and execution of hardware capabilities (actuators, radios, safety mechanisms) via functional hooks (``add_functionality`` / ``execute_functionality``).
* **Deterministic Guardrails**:
  Provides a structured foundation to convert probabilistic predictions into safe, verifiable physical actions.
* **Minimal Footprint**:
  Pure Python zero-dependency core designed for rapid prototyping and micro-framework portability.

Architecture
============

.. code-block:: text

   +-------------------------------------------------------------------+
   |                        SENSORY INPUT STREAM                       |
   |              (LiDAR, IMU, Optical Flow, Camera, etc.)             |
   +---------------------------------+---------------------------------+
                                     |
                                     v
   +-------------------------------------------------------------------+
   |                     MODEL INFERENCE (Perception)                  |
   |                Model.predict() via ModelConfig                    |
   |               (TFLite, ONNX, Quantized Embeddings)                |
   +---------------------------------+---------------------------------+
                                     |  Probabilistic Inference Result
                                     v
   +-------------------------------------------------------------------+
   |                     AUTOMATON (Decision Core)                     |
   |                 Reactive Dispatcher & Controller                  |
   +-------------------+-------------+-------------+-------------------+
                       |             |             |
        Execute Organ  |             |             |  Execute Organ
                       v             v             v
                +-------------+ +------------+ +---------------+
                | Motor Units | | Telemetry  | | Safety Chute  |
                | (Actuation) | | (Wireless) | | (Fail-Safe)   |
                +-------------+ +------------+ +---------------+

Repository Structure
====================

.. code-block:: text

   automaton_universale/
   ├── README.rst             # Research documentation & usage guide
   ├── main.py                # Demonstration: Autonomous Flight Controller
   ├── .gitignore             # Standard Python exclusion rules
   └── automata/              # Core library package
       ├── __init__.py        # Package exports
       ├── automata.py        # Automata & AutomataConfig abstractions
       └── model.py           # Model & ModelConfig runtime interfaces

Quick Start & Example
=====================

Here is a minimal demonstration showing how to subclass ``Model`` and build an autonomous agent with ``Automata``:

.. code-block:: python

   from automata import Automata, Model, ModelConfig

   # 1. Define Model Configuration
   class VisionConfig(ModelConfig):
       def load_cfg(self, config: dict):
           config.setdefault("confidence_threshold", 0.8)
           return config

   # 2. Implement the Perception Model
   class ObstacleDetector(Model):
       def load_model(self):
           self.runtime_model = "loaded_weights"

       def predict(self, sensor_frame):
           if sensor_frame.get("distance_m", 10.0) < 1.5:
               return {"status": "OBSTACLE_DETECTED", "confidence": 0.95}
           return {"status": "CLEAR", "confidence": 0.99}

   # 3. Define Actuators / Organ Functions
   def steer_vehicle(direction: str):
       print(f"Executing steering maneuver: {direction}")

   # 4. Instantiate & Configure the Automaton
   cfg = VisionConfig({"confidence_threshold": 0.85})
   model = ObstacleDetector(cfg)
   model.load_model()

   agent = Automata(model=model, name="AutonomousRover")
   agent.add_functionality("steering", steer_vehicle)

   # 5. Perception-Action Loop
   input_data = {"distance_m": 1.1}
   prediction = agent.model.predict(input_data)

   if prediction["status"] == "OBSTACLE_DETECTED":
       agent.execute_functionality("steering", direction="RIGHT_45DEG")

Running the Demo
================

Execute the included end-to-end flight controller demonstration:

.. code-block:: bash

   python3 main.py

Research Roadmap
================

* [ ] **Formal State Machine Engine**: Implement explicit hierarchical states (FSM/HSM) and transition guards.
* [ ] **Learning Hook Enhancements**: Extend the ``@learn`` decorator with runtime latency profiling, memory tracking, and online parameter adaptation.
* [ ] **Hardware-in-the-Loop (HIL) Integration**: Bindings for C/C++ embedded targets and ROS 2 nodes.
* [ ] **Formal Verification**: Safety invariant verification between state transitions.

License
=======

This project is licensed under the MIT License.