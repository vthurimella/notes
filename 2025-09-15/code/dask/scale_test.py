# ===================================================================
# THIS LOGGING BLOCK CAN BE HELPFUL FOR DEBUGGING
# ===================================================================
import logging
# logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)
# logging.getLogger("dask_jobqueue").setLevel(logging.DEBUG)
# ===================================================================

import dask
import dask.array as da
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
import time
import os
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Get the full, absolute path to the shared directory
    home_dir = os.path.expanduser("~")
    mamba_path = f"{home_dir}/shared_parsl/mambaforge"
    
    # Define the prologue commands using the full path
    prologue = [
        f'source {mamba_path}/etc/profile.d/conda.sh',
        f'conda activate {mamba_path}/envs/dask_parsl_env'
    ]

    # --- Experiment Setup ---
    worker_counts_to_test = range(1, 24)  # Test with 1, 2, 3, 4, 5 workers
    runs_per_worker_count = 10            # Number of times to repeat the test for each worker count
    all_results = []
    
    print(f"🚀 Starting Dask worker allocation experiment...")
    print(f"Will test for {list(worker_counts_to_test)} workers, repeating each test {runs_per_worker_count} times.")

    # Outer loop for worker counts
    for num_workers in worker_counts_to_test:
        # Inner loop for repeated runs
        for run_num in range(1, runs_per_worker_count + 1):
            print(f"\n--- Testing {num_workers} worker(s), Run {run_num}/{runs_per_worker_count} ---")
            
            # 1. Configure and create a FRESH SLURM cluster for each test
            cluster = SLURMCluster(
                queue='debug',
                account='prismgt-PG0',
                cores=1,
                memory='7GB',
                walltime='00:20:00',
                job_script_prologue=prologue,
                log_directory='dask-logs',
                local_directory='/tmp'
            )

            # 2. Connect a Dask client
            client = Client(cluster)
            
            try:
                # 3. Start timer and scale to the desired number of workers
                start_time = time.time()
                cluster.scale(jobs=num_workers)
                
                # 4. Wait for exactly that many workers to connect
                print(f"Requesting {num_workers} worker(s) and waiting...")
                client.wait_for_workers(n_workers=num_workers, timeout=300)
                end_time = time.time()
                
                allocation_time = end_time - start_time
                print(f"✅ Success! Allocated {num_workers} worker(s) in {allocation_time:.2f} seconds.")
                
                # 5. Store the raw result
                all_results.append({'workers': num_workers, 'run': run_num, 'allocation_time': allocation_time})

            except Exception as e:
                print(f"❌ Error during Run {run_num} for {num_workers} worker(s): {e}")
                all_results.append({'workers': num_workers, 'run': run_num, 'allocation_time': float('nan')})
            
            finally:
                # 6. Clean up for the next run
                print("Shutting down client and cluster for this iteration.")
                client.close()
                cluster.close()
                time.sleep(5) # Brief pause to ensure resources are released

    print("\n--- Experiment Finished ---")

    # --- Data Analysis and Plotting ---
    if not all_results:
        print("No data collected, cannot generate plot.")
    else:
        # Convert raw results to a DataFrame
        raw_df = pd.DataFrame(all_results)
        print("\n📊 Raw Results:")
        print(raw_df.to_string())
        
        # --- NEW: SAVE DATA TO CSV ---
        csv_filename = 'worker_allocation_raw_data.csv'
        raw_df.to_csv(csv_filename, index=False)
        print(f"\n💾 Raw data saved to {csv_filename}")
        # -----------------------------
        
        # Calculate statistics (mean and standard deviation) for each worker count
        stats_df = raw_df.groupby('workers')['allocation_time'].agg(['mean', 'std']).reset_index()
        stats_df['std'] = stats_df['std'].fillna(0) # Replace NaN std with 0
        
        print("\n📈 Statistical Summary:")
        print(stats_df.to_string())
        
        # Create the plot with error bars
        plt.figure(figsize=(10, 6))
        plt.errorbar(
            stats_df['workers'], 
            stats_df['mean'], 
            yerr=stats_df['std'], 
            fmt='-o',          # Format line and markers
            capsize=5,         # Add caps to error bars
            label='Mean ± Std Dev'
        )
        
        plt.title('Mean Dask Worker Allocation Time on SLURM')
        plt.xlabel('Number of Workers Requested')
        plt.ylabel('Allocation Time (seconds)')
        plt.xticks(stats_df['workers']) # Ensure x-axis ticks are integers
        plt.grid(True, which='both', linestyle='--')
        plt.legend()
        
        # Save the plot to a file
        plot_filename = 'worker_allocation_stats.png'
        plt.savefig(plot_filename)
        print(f"\n📈 Plot with error bars saved to {plot_filename}")
        plt.show()