import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Define thread counts
thread_counts = [2, 4, 6, 8, 10, 12, 14]

# Initialize lists to store data
context_switches = []
cache_references = []
cache_misses = []
cycles = []
instructions = []
# throughput = []  # Instructions per cycle

# Read data from each file
for threads in thread_counts:
    filename = f"perf_results_{threads}.txt"
    with open(filename, "r") as file:
        data = file.readline().strip().split()
        
        # Convert values while removing commas
        ctx_sw = int(data[1].replace(",", ""))
        cache_ref = int(data[2].replace(",", ""))
        cache_miss = int(data[3].replace(",", ""))
        cycle = int(data[4].replace(",", ""))
        instr = int(data[5].replace(",", ""))
        
        context_switches.append(ctx_sw)
        cache_references.append(cache_ref)
        cache_misses.append(cache_miss)
        cycles.append(cycle)
        instructions.append(instr)
        # throughput.append(instr / cycle)  # Compute throughput

# Convert to DataFrame
df = pd.DataFrame({
    "Threads": thread_counts,
    "Context Switches": context_switches,
    "Cache References": cache_references,
    "Cache Misses": cache_misses,
    "Cycles": cycles,
    "Instructions": instructions,
    # "Throughput": throughput
})

# Plot settings
sns.set(style="whitegrid")
fig, axes = plt.subplots(3, 2, figsize=(14, 12))
fig.suptitle("Performance Metrics vs. Thread Count", fontsize=16)

# Plot each metric
sns.lineplot(ax=axes[0, 0], x=df["Threads"], y=df["Context Switches"], marker="o", label="Context Switches", color="blue")
axes[0, 0].set_title("Context Switches vs. Threads")

sns.lineplot(ax=axes[0, 1], x=df["Threads"], y=df["Cache References"], marker="o", label="Cache References", color="green")
axes[0, 1].set_title("Cache References vs. Threads")

sns.lineplot(ax=axes[1, 0], x=df["Threads"], y=df["Cache Misses"], marker="o", label="Cache Misses", color="red")
axes[1, 0].set_title("Cache Misses vs. Threads")

sns.lineplot(ax=axes[1, 1], x=df["Threads"], y=df["Cycles"], marker="o", label="Cycles", color="purple")
axes[1, 1].set_title("Cycles vs. Threads")

sns.lineplot(ax=axes[2, 0], x=df["Threads"], y=df["Instructions"], marker="o", label="Instructions", color="orange")
axes[2, 0].set_title("Instructions vs. Threads")

# sns.lineplot(ax=axes[2, 1], x=df["Threads"], y=df["Throughput"], marker="o", label="Throughput", color="brown")
# axes[2, 1].set_title("Throughput vs. Threads")

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("performance_plots.png")  # Save the plot as an image
plt.show()
