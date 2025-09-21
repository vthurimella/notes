# parsl_scale_test.py
import parsl
import time
import pandas as pd
import matplotlib.pyplot as plt
import sys
import importlib
import subprocess
import json

# A simple Parsl app to trigger worker allocation
@parsl.python_app
def probe_app():
    return True

def run_single_test(config_module, num_units, unit_name):
    """This function runs ONE isolated Parsl test and returns the result."""
    parsl.load(config_module.config)
    dfk = parsl.dfk()
    # Get the first defined executor from the loaded config
    executor = dfk.executors[list(dfk.executors.keys())[0]]
    
    try:
        # Submit probe tasks to trigger scaling
        [probe_app() for _ in range(num_units)]

        # Start timer and wait for workers to connect
        start_time = time.time()
        
        while executor.connected_workers() < num_units:
            time.sleep(0.01)
            if time.time() - start_time > 300: # 5-minute timeout
                raise TimeoutError("Timed out waiting for workers to connect")

        end_time = time.time()
        allocation_time = end_time - start_time
        return {'status': 'success', 'time': allocation_time}

    finally:
        # Clean up Parsl
        dfk.cleanup()
        parsl.clear()

def analyze_and_plot(all_results, unit_name):
    """This function is for analysis and plotting, unchanged from before."""
    if not all_results:
        print("No data collected, cannot generate plot.")
        return

    raw_df = pd.DataFrame(all_results)
    print("\n📊 Raw Results:")
    print(raw_df.to_string())
    
    csv_filename = f'parsl_{unit_name}_allocation_raw_data.csv'
    raw_df.to_csv(csv_filename, index=False)
    print(f"\n💾 Raw data saved to {csv_filename}")
    
    stats_df = raw_df.groupby(unit_name)['allocation_time'].agg(['mean', 'std']).reset_index()
    stats_df['std'] = stats_df['std'].fillna(0)
    
    print("\n📈 Statistical Summary:")
    print(stats_df.to_string())
    
    plt.figure(figsize=(10, 6))
    plt.errorbar(
        stats_df[unit_name], 
        stats_df['mean'], 
        yerr=stats_df['std'], 
        fmt='-o', capsize=5, label='Mean ± Std Dev'
    )
    plt.title(f'Mean Parsl {unit_name.capitalize()} Allocation Time on SLURM')
    plt.xlabel(f'Number of {unit_name.capitalize()}s Requested')
    plt.ylabel('Allocation Time (seconds)')
    plt.xticks(stats_df[unit_name])
    plt.grid(True, which='both', linestyle='--')
    plt.legend()
    
    plot_filename = f'parsl_{unit_name}_allocation_stats.png'
    plt.savefig(plot_filename)
    print(f"\n📈 Plot with error bars saved to {plot_filename}")
    # plt.show() # Commented out to prevent hanging in non-interactive sessions

# =================================================================================
# MAIN SCRIPT LOGIC
# =================================================================================
if __name__ == "__main__":
    # This special block runs a single, isolated test when the script calls itself.
    if '--run-single' in sys.argv:
        config_name = sys.argv[2]
        num_units = int(sys.argv[3])
        unit_name = sys.argv[4]
        config_module = importlib.import_module(config_name)
        try:
            result = run_single_test(config_module, num_units, unit_name)
            # Print result as JSON so the main process can read it
            print(json.dumps(result))
        except Exception as e:
            print(json.dumps({'status': 'error', 'error_message': str(e)}))
        sys.exit(0)

    # This is the main "controller" that orchestrates the experiment.
    if len(sys.argv) != 4:
        print("Usage: python parsl_scale_test.py <config_file> <max_units> <unit_name>")
        print("Example (CPU): python parsl_scale_test.py config_cpu_scale 24 worker")
        print("Example (Node): python parsl_scale_test.py config_node_scale 3 node")
        sys.exit(1)

    config_name = sys.argv[1]
    max_units = int(sys.argv[2])
    unit_name = sys.argv[3]
    
    worker_range = range(1, max_units + 1)
    num_runs = 10
    all_results = []
    
    print(f"🚀 Starting Parsl {unit_name} allocation experiment...")
    print(f"Will test for {list(worker_range)} {unit_name}s, repeating each test {num_runs} times.")

    for num_units in worker_range:
        for run_num in range(1, num_runs + 1):
            print(f"\n--- Testing {num_units} {unit_name}(s), Run {run_num}/{num_runs} ---")
            
            # Use a subprocess to call this same script in "single run" mode.
            # This ensures each Parsl run is completely isolated and clean.
            cmd = [
                sys.executable, __file__, '--run-single', 
                config_name, str(num_units), unit_name
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=360)
                output = json.loads(result.stdout)

                if output['status'] == 'success':
                    allocation_time = output['time']
                    print(f"✅ Success! Allocated {num_units} {unit_name}(s) in {allocation_time:.2f} seconds.")
                    all_results.append({unit_name: num_units, 'run': run_num, 'allocation_time': allocation_time})
                else:
                    error_msg = output.get('error_message', 'Unknown error')
                    print(f"❌ Error during Run {run_num} for {num_units} {unit_name}(s): {error_msg}")
                    all_results.append({unit_name: num_units, 'run': run_num, 'allocation_time': float('nan')})

            except subprocess.TimeoutExpired:
                print(f"❌ Error: Subprocess timed out after 6 minutes.")
                all_results.append({unit_name: num_units, 'run': run_num, 'allocation_time': float('nan')})
            except Exception as e:
                print(f"❌ An unexpected error occurred: {e}")
                all_results.append({unit_name: num_units, 'run': run_num, 'allocation_time': float('nan')})

    # Once all subprocesses are done, analyze and plot the collected results.
    analyze_and_plot(all_results, unit_name)