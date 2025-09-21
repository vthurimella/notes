# config_cpu_scale.py
import parsl
from parsl.config import Config
from parsl.providers import SlurmProvider
from parsl.launchers import SrunLauncher
from parsl.executors import HighThroughputExecutor

config = Config(
    executors=[
        HighThroughputExecutor(
            label="slurm_htex_cpu",
            address="10.10.1.1",
            # Allows packing multiple workers (up to 8) onto a single node
            max_workers_per_node=8,
            provider=SlurmProvider(
                partition='debug',
                launcher=SrunLauncher(),
                # --- Scaling Parameters ---
                nodes_per_block=1,  # Request one node at a time
                init_blocks=0,
                min_blocks=0,
                max_blocks=3,       # Allow scaling up to all 3 nodes
                # --- Worker Setup ---
                worker_init='source ~/shared_parsl/mambaforge/envs/dask_parsl_env/bin/activate',
                walltime='00:20:00'
            ),
        )
    ],
    strategy='simple',
    max_idletime=45
)