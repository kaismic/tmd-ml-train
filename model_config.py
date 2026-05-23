from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path
import constants
import hashlib
import yaml

@dataclass
class ModelConfig:
    # Fields loaded from YAML
    transport_modes: Dict[str, int] = field(default_factory=dict)
    sensors: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    window_size_seconds: int = 10
    window_next_step_seconds: int = 5

    # Derived fields — excluded from __init__, populated in __post_init__
    id: str = field(init=False, default='')
    cleaned_data_path: Path = field(init=False, default_factory=Path)
    transformed_data_path: Path = field(init=False, default_factory=Path)
    models_path: Path = field(init=False, default_factory=Path)
    sensor_features_in_order: List[str] = field(init=False, default_factory=list)

    @classmethod
    def from_yaml(cls, path: str = "model.config.yaml") -> "ModelConfig":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(
            transport_modes=data["transport_modes"],
            sensors=data["sensors"],
            features=data["features"],
            window_size_seconds=data["window_size_seconds"],
            window_next_step_seconds=data["window_next_step_seconds"],
        )

    def __post_init__(self) -> None:
        self.id = self.generate_config_id()
        self.cleaned_data_path = constants.DATA_PATH / self.id / constants.CLEANED_DATA_DIR
        self.transformed_data_path = constants.DATA_PATH / self.id / constants.TRANSFORMED_DATA_DIR
        self.models_path = constants.ROOT_PATH / constants.MODELS_DIR / self.id
        self.sensor_features_in_order = [
            f"{sensor}#{feature}"
            for sensor in self.sensors
            for feature in self.features
        ]
        print(self)

    def generate_config_id(self) -> str:
        sorted_transport_modes = sorted(self.transport_modes.keys())
        sorted_sensors = sorted(self.sensors)
        sorted_features = sorted(self.features)
        hash_input = ''.join([
            *sorted_transport_modes,
            *sorted_sensors,
            *sorted_features,
            hex(self.window_size_seconds),
            hex(self.window_next_step_seconds),
        ])
        return hashlib.sha256(hash_input.encode()).hexdigest()[:8]


if __name__ == '__main__':
    config = ModelConfig.from_yaml()