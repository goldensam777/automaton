"""
Main entry point and demonstration of the Automaton library.
Use case: Autonomous Edge-AI Drone Controller (Perception -> Decision -> Action loop).
"""

#  _                                      _       _         
# | | ___ _   _ _ __ ___   __ _ ___      | | __ _| |__  ___ 
# | |/ _ \ | | | '_ ` _ \ / _` / __|_____| |/ _` | '_ \/ __|
# | |  __/ |_| | | | | | | (_| \__ \_____| | (_| | |_) \__ \
# |_|\___|\__,_|_| |_| |_|\__,_|___/     |_|\__,_|_.__/|___/


from automata import Automata, Model, ModelConfig, learn


# ==============================================================================
# 1. Hardware & Model Configuration
# ==============================================================================
class ObstacleModelConfig(ModelConfig):
    """Handles and validates hyperparameters for the Edge Obstacle Detector."""

    def load_cfg(self, config: dict) -> dict:
        validated = dict(config)
        validated.setdefault("confidence_threshold", 0.75)
        validated.setdefault("target_fps", 30)
        validated.setdefault("input_channels", ["lidar", "sonar", "optical_flow"])
        return validated


# ==============================================================================
# 2. Embedded AI Model Abstraction
# ==============================================================================
class EdgeObstacleDetector(Model):
    """Simulates an on-device lightweight perception model (e.g., TFLite / ONNX Runtime)."""

    def load_model(self):
        print(f"[{self.__class__.__name__}] Allocating memory buffers and loading weights...")
        self.runtime_model = "tflite_micro_obstacle_v2_quantized.tflite"
        print(f"[{self.__class__.__name__}] Model loaded successfully into runtime memory.")

    @learn
    def predict(self, sensor_frame: dict) -> dict:
        """Inference step: analyzes distance and optical flow to classify flight risk."""
        distance_m = sensor_frame.get("distance_m", 10.0)
        optical_flow_divergence = sensor_frame.get("flow_div", 0.0)

        if distance_m < 1.0 or optical_flow_divergence > 0.8:
            return {
                "decision": "CRITICAL_OBSTACLE",
                "confidence": 0.96,
                "recommended_action": "EMERGENCY_LAND",
            }
        elif distance_m < 3.5 or optical_flow_divergence > 0.4:
            return {
                "decision": "WARNING_OBSTACLE",
                "confidence": 0.84,
                "recommended_action": "AVOIDANCE_MANEUVER",
            }
        return {
            "decision": "PATH_CLEAR",
            "confidence": 0.99,
            "recommended_action": "CRUISE",
        }


# ==============================================================================
# 3. Dynamic Hardware Functionalities / Actuators ("Organs")
# ==============================================================================
def control_motors(maneuver: str, thrust_pct: int = 100):
    print(f"  └─► [Actuator: Motors] Executing maneuver: '{maneuver}' at {thrust_pct}% thrust.")

def trigger_emergency_parachute(reason: str):
    print(f"  └─► [Safety: Parachute] CRITICAL TRIGGER! Deploying recovery chute (Reason: {reason})")

def transmit_telemetry(packet: dict):
    print(f"  └─► [Radio: LoRa] Transmitting packet to Ground Station: {packet}")


# ==============================================================================
# 4. Main Simulation Loop
# ==============================================================================
def main():
    print("=" * 70)
    print(" Automaton Universale - Embedded AI Controller Demo")
    print(" Project Concept for Autonomous Systems & Edge AI")
    print("=" * 70)

    # 1. Initialize configuration and AI model
    cfg_data = {"confidence_threshold": 0.80, "target_fps": 60}
    model_cfg = ObstacleModelConfig(cfg_data)
    detector = EdgeObstacleDetector(model_cfg)
    detector.load_model()

    # 2. Instantiate the Automaton (Drone Controller)
    drone = Automata(model=detector, name="Caltech-AeroBot-1")

    # 3. Register modular organs / actuators dynamically
    drone.add_functionality("motors", control_motors)
    drone.add_functionality("safety_parachute", trigger_emergency_parachute)
    drone.add_functionality("telemetry", transmit_telemetry)

    # 4. Simulated Sensor Telemetry Stream (Perception inputs over time)
    sensor_telemetry_stream = [
        {"timestamp_ms": 100, "distance_m": 12.0, "flow_div": 0.05, "desc": "Open corridor"},
        {"timestamp_ms": 200, "distance_m": 2.8,  "flow_div": 0.45, "desc": "Approaching wall"},
        {"timestamp_ms": 300, "distance_m": 0.6,  "flow_div": 0.92, "desc": "Imminent collision"},
    ]

    print("\n>>> Launching Autonomous Flight Mission <<<\n")

    for step, sensor_data in enumerate(sensor_telemetry_stream, start=1):
        print(f"[Tick {step}] Sensor Input ({sensor_data['desc']}): distance={sensor_data['distance_m']}m, flow={sensor_data['flow_div']}")

        # Step A: Perception (Inference via Model)
        inference = drone.model.predict(sensor_data)
        print(f"  [Perception] Status: {inference['decision']} (Confidence: {inference['confidence']*100:.1f}%)")

        # Step B: Reactive Decision & Execution via Automata
        decision = inference["decision"]
        if decision == "PATH_CLEAR":
            drone.execute_functionality("motors", maneuver="CRUISE_FORWARD", thrust_pct=90)
        elif decision == "WARNING_OBSTACLE":
            drone.execute_functionality("motors", maneuver="DEFLECT_RIGHT_45DEG", thrust_pct=60)
            drone.execute_functionality("telemetry", packet={"event": "OBSTACLE_AVOIDANCE", "step": step})
        elif decision == "CRITICAL_OBSTACLE":
            drone.execute_functionality("safety_parachute", reason="IMMINENT_PROXIMITY_COLLISION")
            drone.execute_functionality("telemetry", packet={"event": "EMERGENCY_ABORT", "step": step})
            print("\n[Mission] Safe shutdown initiated.")
            break
        print("-" * 50)

    print("\nMission simulation completed successfully.")


if __name__ == "__main__":
    main()