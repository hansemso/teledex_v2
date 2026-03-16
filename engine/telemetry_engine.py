import random

def plot_entry(label, value):
    print(f"[Telemetry] Plotting {label}: {value}")

def plot_prediction(label, horizon=5):
    predictions = [round(random.uniform(10, 100), 2) for _ in range(horizon)]
    print(f"[Telemetry] Prediction for {label}: {predictions}")