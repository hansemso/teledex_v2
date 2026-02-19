from telemetry_engine import plot_entry

# Dummy test entry
test_entry = {
    "label": "Test Sensor",
    "x": "days",
    "y": "42"
}

# Plot it
plot_entry(test_entry)
