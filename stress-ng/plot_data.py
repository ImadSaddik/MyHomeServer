import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("temperature_data.csv")
df.columns = df.columns.str.strip()

plt.figure(figsize=(16, 9))
plt.plot(
    df["timestamp"],
    df["platform"],
    color="red",
    linewidth=2,
    label="CPU Package (Platform)",
)

plt.title("CPU stress test temperature curve", fontsize=16, fontweight="bold")
plt.xlabel("Time", fontsize=12)
plt.ylabel("Temperature (°C)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.fill_between(df["timestamp"], df["platform"], 30, color="red", alpha=0.1)

step = max(1, len(df) // 10)
plt.xticks(df["timestamp"][::step], rotation=45)

plt.axhline(y=70, color="orange", linestyle="--", label="Max observed temp (70°C)")
plt.axhline(y=85, color="darkred", linestyle="-", label="Critical limit (85°C)")
plt.legend(loc="upper left", fontsize=10, frameon=True, shadow=True)
plt.tight_layout()

plt.savefig("../images/cpu_stress_test.png")
print("Successfully saved plot.")
