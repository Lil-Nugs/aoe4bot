"""Configuration management for AoE4 Bot."""
import os
import yaml
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Tuple


@dataclass
class GameConfig:
    """Game-specific configuration."""
    window_title: str = "Age of Empires IV"
    screen_width: int = 3840  # 4K resolution
    screen_height: int = 2160  # 4K resolution
    game_speed: float = 1.0

    # Game UI positions (calibrated using calibrate_ui.py)
    minimap_region: Tuple[int, int, int, int] = (0, 0, 400, 400)  # x, y, w, h

    # Resource bar positions (for OCR - read values from screen)
    resources_food_pos: Tuple[int, int] = (0, 0)  # x, y of food resource number
    resources_wood_pos: Tuple[int, int] = (0, 0)  # x, y of wood resource number
    resources_gold_pos: Tuple[int, int] = (0, 0)  # x, y of gold resource number
    resources_stone_pos: Tuple[int, int] = (0, 0)  # x, y of stone resource number

    # Other UI positions (for OCR - read values from screen)
    population_pos: Tuple[int, int] = (0, 0)  # x, y of population counter
    game_time_pos: Tuple[int, int] = (0, 0)  # x, y of game time display
    queue_indicator_pos: Tuple[int, int] = (0, 0)  # x, y of queue indicator (to check production)

    # OCR region sizes (width, height around the position)
    ocr_region_size: Tuple[int, int] = (100, 40)  # Default size for OCR regions

    # Game hotkeys (for actions - faster than clicking!)
    hotkey_select_tc: str = 'h'  # Select town center
    hotkey_idle_economy: str = '.'  # Select idle economy unit (villager, fishing ship, trader)
    hotkey_queue_villager: str = 'q'  # Queue villager (when TC selected)
    hotkey_attack_move: str = 'a'  # Attack move

    # Action delays (seconds)
    click_delay: float = 0.05
    command_delay: float = 0.1


@dataclass
class TrainingConfig:
    """RL training configuration."""
    # PPO hyperparameters
    learning_rate: float = 3e-4
    n_steps: int = 2048
    batch_size: int = 64
    n_epochs: int = 10
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_range: float = 0.2
    ent_coef: float = 0.01
    vf_coef: float = 0.5
    max_grad_norm: float = 0.5

    # Training settings
    total_timesteps: int = 10_000_000
    save_freq: int = 50_000
    eval_freq: int = 10_000
    eval_episodes: int = 5

    # Environment settings
    n_envs: int = 1  # Parallel environments (start with 1)
    frame_skip: int = 4  # Take action every N frames
    observation_size: Tuple[int, int] = (84, 84)  # Reduced resolution for CNN


@dataclass
class RewardConfig:
    """Reward function weights."""
    villager_queued: float = 10.0
    villager_created: float = 50.0
    sheep_collected: float = 100.0
    map_explored: float = 1.0  # Per % of map revealed
    scout_death: float = -100.0
    tc_danger_penalty: float = -10.0  # Per second near enemy TC
    idle_villager_penalty: float = -5.0


class Config:
    """Main configuration manager."""

    def __init__(self, config_path: str = None):
        self.root_dir = Path(__file__).parent.parent
        self.config_path = config_path or self.root_dir / "config" / "game_config.yaml"

        # Directories
        self.models_dir = self.root_dir / "models"
        self.logs_dir = self.root_dir / "logs"
        self.data_dir = self.root_dir / "data"

        # Create directories
        self.models_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)

        # Load configs
        self.game = GameConfig()
        self.training = TrainingConfig()
        self.rewards = RewardConfig()

        # Load from file if exists
        if self.config_path.exists():
            self.load()

    def load(self):
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            data = yaml.safe_load(f)

        if 'game' in data:
            self.game = GameConfig(**data['game'])
        if 'training' in data:
            self.training = TrainingConfig(**data['training'])
        if 'rewards' in data:
            self.rewards = RewardConfig(**data['rewards'])

    def save(self):
        """Save configuration to YAML file."""
        self.config_path.parent.mkdir(exist_ok=True)

        data = {
            'game': asdict(self.game),
            'training': asdict(self.training),
            'rewards': asdict(self.rewards)
        }

        with open(self.config_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)

    def __str__(self):
        return f"Config(game={self.game}, training={self.training}, rewards={self.rewards})"


if __name__ == "__main__":
    # Generate default config file
    config = Config()
    config.save()
    print(f"Configuration saved to {config.config_path}")
