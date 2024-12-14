import os
import subprocess
import time
from datetime import datetime

# Define simulation
SIMULATION ="Default"
INSTRUCTIONS = 100000000

# Define paths and settings
GEM5_PATH = "./build/ARM/gem5.opt"  # Replace with the path to your gem5 directory
SE_SCRIPT = "configs/example/se.py"  # Path to se.py script
OUTPUT_DIR = "spec_results/"  # Directory to store simulation outputs

BENCHMARKS = [
    ("401bzip", "spec_cpu2006/401.bzip2/src/specbzip","spec_cpu2006/401.bzip2/data/input.program 10"),
    ("429mcf", "spec_cpu2006/429.mcf/src/specmcf", "spec_cpu2006/429.mcf/data/inp.in"),
    ("456hmmer","spec_cpu2006/456.hmmer/src/spechmmer", "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm"),
    ("458sjeng","spec_cpu2006/458.sjeng/src/specsjeng", "spec_cpu2006/458.sjeng/data/test.txt"),
    ("470lbm","spec_cpu2006/470.lbm/src/speclibm", "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of"),
    
]
#OPTIONS = "--cpu-type=MinorCPU --caches --l2cache"  # Common options for all simulations
OPTION_SETS = [
    #("1GHz", "--cpu-type=MinorCPU --cpu-clock=1GHz --caches --l2cache"),
    #("3GHz", "--cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache"),
    #("DDR3_2133", "--cpu-type=MinorCPU --mem-type=DDR3_2133_8x8 --caches --l2cache"),
    #("L1_icache_size_64kB", "--cpu-type=MinorCPU --caches --l2cache --l1i_size=64kB"),
    #("L1_icache_size_16kB", "--cpu-type=MinorCPU --caches --l2cache --l1i_size=16kB"),
    #("L1_icache_assoc_4", "--cpu-type=MinorCPU --caches --l2cache --l1i_assoc=4"),
    #("L1_icache_assoc_1", "--cpu-type=MinorCPU --caches --l2cache --l1i_assoc=1"),
    #("L1_dcache_size_128kB", "--cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB"),
    #("L1_dcache_size_32kB", "--cpu-type=MinorCPU --caches --l2cache --l1d_size=32kB"),
    #("L1_dcache_assoc_4", "--cpu-type=MinorCPU --caches --l2cache --l1d_assoc=4"),
    #("L1_dcache_assoc_1", "--cpu-type=MinorCPU --caches --l2cache --l1d_assoc=1"),
    #("L2_cache_size_4MB", "--cpu-type=MinorCPU --caches --l2cache --l2_size=4MB"),
    #("L2_cache_size_1MB", "--cpu-type=MinorCPU --caches --l2cache --l2_size=1MB"),
    #("L2_cache_assoc_4", "--cpu-type=MinorCPU --caches --l2cache --l2_assoc=4"),
    #("L2_cache_assoc_2", "--cpu-type=MinorCPU --caches --l2cache --l2_assoc=2"),
    #("Cacheline_size_32", "--cpu-type=MinorCPU --caches --l2cache --cacheline_size=32"),
    #("Cacheline_size_128", "--cpu-type=MinorCPU --caches --l2cache --cacheline_size=128"),
    ("opt1","--cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache --l1i_size=32kB --l1i_assoc=2 --l1d_size=32kB --l1d_assoc=2 --l2_size=512kB --l2_assoc=8 --cacheline_size=64"),
    ("opt2","--cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache --l1i_size=64kB --l1i_assoc=4 --l1d_size=64kB --l1d_assoc=4 --l2_size=2MB --l2_assoc=8 --cacheline_size=128"),
    ("opt3","--cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache --l1i_size=32kB --l1i_assoc=4 --l1d_size=64kB --l1d_assoc=4 --l2_size=4MB --l2_assoc=8 --cacheline_size=128"),
    ("opt4","--cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache --l1i_size=128kB --l1i_assoc=4 --l1d_size=128kB --l1d_assoc=4 --l2_size=2MB --l2_assoc=16 --cacheline_size=128"),
    ("opt5","--cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache --l1i_size=128kB --l1i_assoc=8 --l1d_size=128kB --l1d_assoc=8 --l2_size=4MB --l2_assoc=16 --cacheline_size=128"),
]

# Utility to run a single simulation
def run_simulation(benchmark_name, binary_path, output_dir, benchmark_o, options):
    output_path = os.path.join(output_dir, SIMULATION, benchmark_name)
    os.makedirs(output_path, exist_ok=True)  # Create output directory if it doesn't exist

    # Construct gem5 command
    cmd = [
        GEM5_PATH,
        "-d", output_path,
        SE_SCRIPT,
    ] + options.split() + [
        "-c", binary_path,
        "-o", benchmark_o,
        "-I", str(INSTRUCTIONS)
    ]
    # Log the command being executed
    print(f"Starting simulation for {benchmark_name} with options: '{options}' at {datetime.now()}")
    print("Command:"," ".join(cmd))

    # Run the command and log output
    log_file = os.path.join(output_path, "simulation.log")
    with open(log_file, "w") as log:
        process = subprocess.run(cmd, stdout=log, stderr=log)

    # Check if the simulation completed successfully
    if process.returncode == 0:
        print(f"Simulation for {benchmark_name} completed successfully!")
    else:
        print(f"Simulation for {benchmark_name} failed. Check log: {log_file}")

# Main function to iterate through benchmarks
def run_benchmarks():
    start_time = time.time()
    for option_name, options in OPTION_SETS:
        print(f"\nStarting simulations with option set '{option_name}': {options}\n")
        
        # Update simulation name to reflect the current option set
        global SIMULATION
        SIMULATION = option_name  # Use the provided name for the option set
        
        # Run all benchmarks with the current option set
        for name, path, o in BENCHMARKS:
            run_simulation(name, path, OUTPUT_DIR, o, options)
    
    total_time = time.time() - start_time
    print(f"All simulations completed in {total_time / 3600:.2f} hours.")

# Entry point
if __name__ == "__main__":
    run_benchmarks()

