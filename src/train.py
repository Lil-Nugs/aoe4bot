"""Training script for AoE4 Bot using PPO."""
import os
import argparse
from pathlib import Path
from datetime import datetime

import torch
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack

from config import Config
from aoe4_env import AoE4Env


def make_env(config: Config):
    """Create and wrap the environment."""
    def _init():
        env = AoE4Env(config=config, render_mode='human')
        env = Monitor(env)
        return env
    return _init


def train(config: Config, resume: str = None):
    """Train the AoE4 bot using PPO."""
    print("=" * 50)
    print("AoE4 Bot Training")
    print("=" * 50)
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
    print(f"Training config: {config.training}")
    print("=" * 50)

    # Create environment
    print("\nCreating environment...")
    env = DummyVecEnv([make_env(config) for _ in range(config.training.n_envs)])

    # Frame stacking (optional, useful for capturing motion)
    # env = VecFrameStack(env, n_stack=4)

    # Create save directories
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = config.models_dir / f"ppo_aoe4_{timestamp}"
    log_dir = config.logs_dir / f"ppo_aoe4_{timestamp}"
    save_dir.mkdir(exist_ok=True, parents=True)
    log_dir.mkdir(exist_ok=True, parents=True)

    # Callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=config.training.save_freq,
        save_path=str(save_dir),
        name_prefix="aoe4_bot"
    )

    # Create or load model
    if resume:
        print(f"\nLoading model from {resume}")
        model = PPO.load(resume, env=env)
        model.learning_rate = config.training.learning_rate
    else:
        print("\nCreating new PPO model...")
        model = PPO(
            "MultiInputPolicy",  # For Dict observation space
            env,
            learning_rate=config.training.learning_rate,
            n_steps=config.training.n_steps,
            batch_size=config.training.batch_size,
            n_epochs=config.training.n_epochs,
            gamma=config.training.gamma,
            gae_lambda=config.training.gae_lambda,
            clip_range=config.training.clip_range,
            ent_coef=config.training.ent_coef,
            vf_coef=config.training.vf_coef,
            max_grad_norm=config.training.max_grad_norm,
            verbose=1,
            tensorboard_log=str(log_dir),
            device='auto'
        )

    print(f"\nModel architecture:")
    print(model.policy)

    # Train
    print(f"\nStarting training for {config.training.total_timesteps:,} timesteps...")
    print(f"Checkpoints will be saved to: {save_dir}")
    print(f"Logs will be saved to: {log_dir}")
    print("\nTo monitor training with TensorBoard, run:")
    print(f"  tensorboard --logdir {log_dir}")
    print("\n" + "=" * 50)

    try:
        model.learn(
            total_timesteps=config.training.total_timesteps,
            callback=checkpoint_callback,
            progress_bar=True
        )

        # Save final model
        final_path = save_dir / "final_model.zip"
        model.save(final_path)
        print(f"\n✓ Training complete! Final model saved to: {final_path}")

    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user")
        interrupt_path = save_dir / "interrupted_model.zip"
        model.save(interrupt_path)
        print(f"Model saved to: {interrupt_path}")

    finally:
        env.close()


def test(model_path: str, config: Config, episodes: int = 5):
    """Test a trained model."""
    print(f"Testing model: {model_path}")

    # Create environment
    env = AoE4Env(config=config, render_mode='human')
    env = Monitor(env)

    # Load model
    model = PPO.load(model_path)

    # Run episodes
    for episode in range(episodes):
        obs, info = env.reset()
        episode_reward = 0
        done = False
        step = 0

        print(f"\n=== Episode {episode + 1}/{episodes} ===")

        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            episode_reward += reward
            step += 1

            if step % 100 == 0:
                print(f"Step {step}: Reward = {episode_reward:.2f}")

        print(f"Episode finished after {step} steps")
        print(f"Total reward: {episode_reward:.2f}")
        print(f"Info: {info}")

    env.close()


def main():
    parser = argparse.ArgumentParser(description='Train AoE4 Bot with PPO')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--resume', type=str, help='Path to model to resume training')
    parser.add_argument('--test', type=str, help='Path to model to test')
    parser.add_argument('--episodes', type=int, default=5, help='Number of test episodes')

    args = parser.parse_args()

    # Load configuration
    config = Config(args.config)

    if args.test:
        test(args.test, config, args.episodes)
    else:
        train(config, args.resume)


if __name__ == "__main__":
    main()
