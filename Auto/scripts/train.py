if __name__ != "__main__":
    raise Exception("This is a SCRIPT and should be run as __main__!")


# Stdlib Imports
import argparse

# PyPI Imports
import ray
import ray.tune as tune

# Workspace Imports
from autockt.envs.ngspice_vanilla_opamp import TwoStageAmp


parser = argparse.ArgumentParser()
parser.add_argument("--checkpoint_dir", "-cpd", type=str)
args = parser.parse_args()


ray.init()


# configures training of the agent with associated hyperparameters
# See Ray documentation for details on each parameter
config_train = {
    # "sample_batch_size": 200,
    "train_batch_size": 1200,
    # "sgd_minibatch_size": 1200,
    # "num_sgd_iter": 3,
    # "lr":1e-3,
    # "vf_loss_coeff": 0.5,
    "horizon": 30,
    "num_gpus": 0,
    "model": {
        "fcnet_hiddens": [64, 64],
    },
    "num_workers": 1,
    "env_config": {
        "generalize": True,
        "run_valid": False,
    },
}


config_experiment = {
    "checkpoint_freq": 1,
    "run": "PPO",
    "env": TwoStageAmp,
    "config": config_train,
}


# Runs training and saves the result in ~/ray_results/train_ngspice_45nm
# If checkpoint fails for any reason, training can be restored
if not args.checkpoint_dir:
    tune.run_experiments(
        {
            "train_45nm_ngspice": config_experiment
            | {
                "stop": {"episode_reward_mean": -0.02},
            }
        }
    )
else:
    print("RESTORING NOW!!!!!!")
    tune.run_experiments(
        {
            "restore_ppo": config_experiment
            | {
                "restore": args.checkpoint_dir,
            }
        }
    )
