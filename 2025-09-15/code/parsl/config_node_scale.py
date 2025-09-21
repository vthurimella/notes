# config_node_scale.py
import parsl
from parsl.config import Config
from parsl.providers import SlurmProvider
from parsl.launchers import SrunLauncher
from parsl.executors import HighThroughputExecutor

config = Config(
    executors=[
        HighThroughputExecutor(
            label="slurm_htex_node",
            address="10.10.1.1",
            # KEY CHANGE: Only one worker per node makes each worker a "node worker"
            max_workers_per_node=1,
            provider=SlurmProvider(
                partition='debug',
                launcher=SrunLauncher(),
                # --- Scaling Parameters ---
                nodes_per_block=1,
                init_blocks=0,
                min_blocks=0,
                max_blocks=3,
                # --- Worker Setup ---
                worker_init='source ~/shared_parsl/mambaforge/envs/dask_parsl_env/bin/activate',
                walltime='00:20:00'
            ),
        )
    ],
    strategy='simple',
    max_idletime=45
)