def estimate_ecg_intervals(ecg_value):
    # Ensure ECG value is within the expected range
    if ecg_value < 900 or ecg_value > 1000:
        raise ValueError("ECG value out of range! Expected between 900-1000.")

    # Linearly interpolate between assumed min/max values
    qt_interval  = 80 - ((ecg_value - 900) * (40 / 100))  # 120ms at 900, 80ms at 1000
    qrs_duration = 450 - ((ecg_value - 900) * (100 / 100))  # 450ms at 900, 350ms at 1000
    t_wave_duration = 30 - ((ecg_value - 900) * (17 / 100))  # 200ms at 900, 160ms at 1000

    return {
        "ECG_Value": ecg_value,
        "QRS_Duration_ms": round(qrs_duration, 2),
        "QT_Interval_ms": round(qt_interval, 2),
        "T_Wave_Duration_ms": round(t_wave_duration, 2)
    }

# Example Test Cases
ecg_values = [900, 920, 940, 960, 980, 1000]

print("Estimated ECG Intervals for Different Inputs:")
for ecg in ecg_values:
    result = estimate_ecg_intervals(ecg)
    print(result)
