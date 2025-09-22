def estimate_ecg_intervals(ecg_value):
    # Ensure ECG value is within the expected range
    if ecg_value < 900 or ecg_value > 1000:
        raise ValueError("ECG value out of range! Expected between 900-1000.")

    # Linearly interpolate between assumed min/max values
    qt_interval  = 80 - ((ecg_value - 900) * (40 / 100))  # 120ms at 900, 80ms at 1000
    qrs_duration = 450 - ((ecg_value - 900) * (100 / 100))  # 450ms at 900, 350ms at 1000
    t_wave_duration = 30 - ((ecg_value - 900) * (17 / 100))  # 200ms at 900, 160ms at 1000
    qrs=round(qrs_duration, 2)
    qt=round(qt_interval, 2)
    twave=round(t_wave_duration, 2)
    return qrs,qt,twave

# Example Test Cases
ecg = 950


qrs_val,qt_val,t_val = estimate_ecg_intervals(ecg)
print("QRS interval  {} \n Q-T interval {} \n T interval {}".format(qrs_val,qt_val,t_val))
