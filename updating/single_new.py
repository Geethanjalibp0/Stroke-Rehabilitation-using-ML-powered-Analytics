def estimate_ecg_intervals(ecg_value):
    # Define min/max ECG values
    min_ecg, max_ecg = 800, 1500

    # Define assumed ECG interval ranges
    min_qt, max_qt   = 30, 205      # QRS duration (slower HR = longer QRS, faster HR = shorter QRS)
    min_qrs, max_qrs = 232, 509       # QT interval
    min_twave, max_twave = -179, 179 # T-wave duration

    # Ensure ECG value stays within range
    ecg_value = max(min_ecg, min(ecg_value, max_ecg))

    # Linear interpolation for different intervals
    qrs_duration = max_qrs + (min_qrs - max_qrs) * (max_ecg - ecg_value) / (max_ecg - min_ecg)
    qt_interval = max_qt + (min_qt - max_qt) * (max_ecg - ecg_value) / (max_ecg - min_ecg)
    t_wave_duration = max_twave + (min_twave - max_twave) * (max_ecg - ecg_value) / (max_ecg - min_ecg)

    # Round values
    return round(qrs_duration, 2), round(qt_interval, 2), round(t_wave_duration, 2)

ecgg=1400

qrs_val, qt_val, t_val = estimate_ecg_intervals(ecgg)
print(f"ECG Value: {ecgg}")
print(f"  QRS interval: {qrs_val} ms")
print(f"  QT interval: {qt_val} ms")
print(f"  T-wave interval: {t_val} ms\n")


# # Example Test Cases
# test_ecg_values = [800, 850, 900, 1000, 1100, 1200, 1300, 1400, 1500]

# for ecg in test_ecg_values:
#     qrs_val, qt_val, t_val = estimate_ecg_intervals(ecg)
#     print(f"ECG Value: {ecg}")
#     print(f"  QRS interval: {qrs_val} ms")
#     print(f"  QT interval: {qt_val} ms")
#     print(f"  T-wave interval: {t_val} ms\n")
