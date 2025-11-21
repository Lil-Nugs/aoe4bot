"""OpenAI Gym environment for Age of Empires IV."""
import gymnasium as gym
import numpy as np
import cv2
from gymnasium import spaces
from typing import Tuple, Dict, Any
from game_interface import GameInterface, GameState
from config import Config


class AoE4Env(gym.Env):
    """
    Custom Gym environment for AoE4.

    Observation Space:
        - Preprocessed game screenshot (grayscale, downscaled)
        - Game state features (resources, population, etc.)

    Action Space:
        - Discrete actions for basic game controls
    """

    metadata = {'render_modes': ['human', 'rgb_array'], 'render_fps': 30}

    def __init__(self, config: Config = None, render_mode: str = None):
        super().__init__()

        self.config = config or Config()
        self.render_mode = render_mode

        # Game interface
        self.game = GameInterface(self.config.game.window_title)

        # Observation space: small grayscale image + game features
        obs_width, obs_height = self.config.training.observation_size
        self.observation_space = spaces.Dict({
            'screen': spaces.Box(
                low=0, high=255,
                shape=(obs_height, obs_width, 1),
                dtype=np.uint8
            ),
            'features': spaces.Box(
                low=-np.inf, high=np.inf,
                shape=(10,),  # [resources(4), pop(2), queue(1), time(1), scout_alive(1), sheep_count(1)]
                dtype=np.float32
            )
        })

        # Action space: discrete actions for Phase 1
        # 0: No-op
        # 1: Queue villager
        # 2-9: Move scout (8 directions)
        # 10: Select scout
        # 11: Collect nearby sheep
        self.action_space = spaces.Discrete(12)

        # Episode tracking
        self.steps = 0
        self.max_steps = 5000  # ~5-10 minutes of game time
        self.episode_reward = 0.0

        # Game state tracking
        self.last_villager_count = 0
        self.last_sheep_count = 0
        self.explored_tiles = set()
        self.scout_alive = True

    def reset(self, seed: int = None, options: dict = None) -> Tuple[Dict, Dict]:
        """Reset the environment for a new episode."""
        super().reset(seed=seed)

        # Reset tracking
        self.steps = 0
        self.episode_reward = 0.0
        self.last_villager_count = 0
        self.last_sheep_count = 0
        self.explored_tiles = set()
        self.scout_alive = True

        # TODO: Implement game restart logic
        # For now, assume game is manually started
        print("Please start a new game manually. Waiting 5 seconds...")
        import time
        time.sleep(5)

        # Get initial observation
        obs = self._get_observation()
        info = self._get_info()

        return obs, info

    def step(self, action: int) -> Tuple[Dict, float, bool, bool, Dict]:
        """Execute one action and return the result."""
        self.steps += 1

        # Execute action
        self._execute_action(action)

        # Wait for game to update
        import time
        time.sleep(0.1 * self.config.training.frame_skip)

        # Get new observation
        obs = self._get_observation()

        # Calculate reward
        reward = self._calculate_reward()

        # Check if episode is done
        terminated = self._check_game_over()
        truncated = self.steps >= self.max_steps

        info = self._get_info()

        self.episode_reward += reward

        return obs, reward, terminated, truncated, info

    def _get_observation(self) -> Dict[str, np.ndarray]:
        """Get current observation from game state."""
        state = self.game.get_game_state()

        # Preprocess screenshot
        screen = self._preprocess_screen(state.screenshot)

        # Extract features (placeholder values for now)
        features = np.array([
            0.0,  # food
            0.0,  # wood
            0.0,  # gold
            0.0,  # stone
            0.0,  # current population
            0.0,  # max population
            0.0,  # villager queue status
            self.steps / 1000.0,  # normalized time
            1.0 if self.scout_alive else 0.0,
            float(self.last_sheep_count)
        ], dtype=np.float32)

        return {
            'screen': screen,
            'features': features
        }

    def _preprocess_screen(self, screenshot: np.ndarray) -> np.ndarray:
        """Preprocess screenshot for neural network."""
        # Convert to grayscale
        gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

        # Resize to observation size
        obs_width, obs_height = self.config.training.observation_size
        resized = cv2.resize(gray, (obs_width, obs_height))

        # Add channel dimension
        return resized[:, :, np.newaxis]

    def _execute_action(self, action: int):
        """Execute the given action in the game."""
        if action == 0:
            # No-op
            pass

        elif action == 1:
            # Queue villager
            self.game.queue_villager()

        elif 2 <= action <= 9:
            # Move scout in direction (scaled for 4K)
            direction = action - 2
            dx, dy = self._get_direction_offset(direction)

            # Move relative to current screen center
            center_x = self.game.screen_width // 2
            center_y = self.game.screen_height // 2

            self.game.select_scout()
            self.game.move_to_position(center_x + dx, center_y + dy)

        elif action == 10:
            # Select scout
            self.game.select_scout()

        elif action == 11:
            # Collect nearby sheep (simplified)
            self.game.select_scout()
            # TODO: Implement sheep detection and collection

    def _get_direction_offset(self, direction: int) -> Tuple[int, int]:
        """Get x, y offset for movement direction (0-7 for 8 directions)."""
        # Scale movement offsets for 4K (200 pixels instead of 100)
        offsets = [
            (0, -200),   # North
            (200, -200), # Northeast
            (200, 0),    # East
            (200, 200),  # Southeast
            (0, 200),    # South
            (-200, 200), # Southwest
            (-200, 0),   # West
            (-200, -200) # Northwest
        ]
        return offsets[direction % 8]

    def _calculate_reward(self) -> float:
        """Calculate reward for current step."""
        reward = 0.0

        # TODO: Implement proper reward calculation based on game state
        # For now, use step penalty to encourage efficiency
        reward -= 0.1  # Small step penalty

        # Rewards from config
        # if villager_queued:
        #     reward += self.config.rewards.villager_queued
        # if new_villager_created:
        #     reward += self.config.rewards.villager_created
        # if sheep_collected:
        #     reward += self.config.rewards.sheep_collected
        # etc.

        return reward

    def _check_game_over(self) -> bool:
        """Check if game is over (win/loss)."""
        # TODO: Implement game over detection
        return False

    def _get_info(self) -> Dict[str, Any]:
        """Get additional info about current state."""
        return {
            'episode_steps': self.steps,
            'episode_reward': self.episode_reward,
            'scout_alive': self.scout_alive,
            'sheep_collected': self.last_sheep_count
        }

    def render(self):
        """Render the environment."""
        if self.render_mode == 'rgb_array':
            state = self.game.get_game_state()
            return state.screenshot
        elif self.render_mode == 'human':
            # Game is already visible
            pass

    def close(self):
        """Clean up resources."""
        pass


# Wrapper for additional preprocessing
class AoE4EnvWrapper(gym.Wrapper):
    """Additional wrapper for frame stacking, normalization, etc."""

    def __init__(self, env: AoE4Env, frame_stack: int = 4):
        super().__init__(env)
        self.frame_stack = frame_stack
        self.frames = []

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        # Initialize frame stack
        self.frames = [obs['screen']] * self.frame_stack
        obs['screen'] = np.concatenate(self.frames, axis=-1)
        return obs, info

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        # Update frame stack
        self.frames.append(obs['screen'])
        self.frames.pop(0)
        obs['screen'] = np.concatenate(self.frames, axis=-1)
        return obs, reward, terminated, truncated, info


if __name__ == "__main__":
    # Test the environment
    print("Testing AoE4 Environment...")

    config = Config()
    env = AoE4Env(config)

    print(f"Observation space: {env.observation_space}")
    print(f"Action space: {env.action_space}")

    # Test reset
    obs, info = env.reset()
    print(f"Initial observation keys: {obs.keys()}")
    print(f"Screen shape: {obs['screen'].shape}")
    print(f"Features shape: {obs['features'].shape}")

    # Test a few random actions
    for i in range(5):
        action = env.action_space.sample()
        print(f"Taking action: {action}")
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"Reward: {reward}, Done: {terminated or truncated}")

    env.close()
    print("Environment test complete!")
