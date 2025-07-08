import matplotlib.pyplot as plt
import seaborn as sns
import re

# Define thread counts
thread_counts = [2, 4, 6, 8, 10, 12, 14]

# Initialize lists to store extracted data
execution_time = []
throughput = []

# Read data from each file
for threads in thread_counts:
    filename = f"perf_{threads}.txt"
    try:
        with open(filename, "r") as file:
            content = file.read()
        
        # Print file contents for debugging
        print(f"\n--- Contents of {filename} ---\n{content}\n")

        # Extract Execution Time and Throughput
        exec_time_match = re.search(r"Execution Time:\s*([\d.]+)", content)
        throughput_match = re.search(r"Throughput:\s*([\d.]+)", content)

        if exec_time_match and throughput_match:
            exec_time = float(exec_time_match.group(1))
            through_put = float(throughput_match.group(1))

            execution_time.append(exec_time)
            throughput.append(through_put)

            print(f"✅ Extracted Execution Time: {exec_time} seconds")
            print(f"✅ Extracted Throughput: {through_put} items/sec")

        else:
            print(f"⚠️ Warning: No match found in {filename}. Check format.")
            execution_time.append(0.0)
            throughput.append(0.0)

    except FileNotFoundError:
        print(f"❌ Warning: {filename} not found. Skipping.")
        execution_time.append(0.0)
        throughput.append(0.0)

# Plot settings
sns.set(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Execution Time & Throughput vs. Thread Count", fontsize=16)

# Plot Execution Time
sns.lineplot(ax=axes[0], x=thread_counts, y=execution_time, marker="o", color="black")
axes[0].set_title("Execution Time vs. Threads")
axes[0].set_xlabel("Number of Threads")
axes[0].set_ylabel("Execution Time (seconds)")

# Plot Throughput
sns.lineplot(ax=axes[1], x=thread_counts, y=throughput, marker="o", color="blue")
axes[1].set_title("Throughput vs. Threads")
axes[1].set_xlabel("Number of Threads")
axes[1].set_ylabel("Throughput (items/sec)")

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("execution_throughput_plots.png")  
plt.show()