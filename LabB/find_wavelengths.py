import csv
import numpy as np
import matplotlib.pyplot as plt

filenames = [
    'Wavelength_data_2026_11_27T11_37_07.csv',
    'Wavelength_data_2026_11_27T11_51_07.csv',
    'Wavelength_data_2026_11_27T12_05_08.csv',
    'Wavelength_data_2026_11_27T12_19_08.csv'
]

x_start, x_end = 200, 2200

# Define for ramp up and cool down at each temperature
intervals = {
    30: {'up': (195, 225), 'down': (2050, 2100)},
    40: {'up': (275, 335), 'down': (1600, 1650)},
    50: {'up': (400, 455), 'down': (1190, 1250)},
    60: {'up': (510, 575), 'down': (920, 1000)},
    70: {'up': (645, 675), 'down': (735, 765)},
}

time_sec, w2, w4 = [], [], []
t0 = None

for filename in filenames:
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for _ in range(3):
            next(reader, None)
        for row in reader:
            if not row or len(row) < 12:
                continue
            ts = float(row[1].strip())
            if t0 is None:
                t0 = ts
            time_sec.append((ts - t0) / 1e6)
            w2.append(float(row[9].strip()))
            w4.append(float(row[11].strip()))

t = np.array(time_sec)
s2 = np.array(w2)
s4 = np.array(w4)

fbg_t_points = []
fbg_b1_points = []
bars = []

for temp, bounds in intervals.items():
    for phase in ['up', 'down']:
        if bounds[phase] is not None:
            t1, t2 = bounds[phase]
            mask = (t >= t1) & (t <= t2)
            v2 = float(np.median(s2[mask]))
            v4 = float(np.median(s4[mask]))

            fbg_t_points.append((temp, v2))
            fbg_b1_points.append((temp, v4))
            bars.append((f"{temp}°C", t1, t2, v2, v4))

print("fbg_t_data =", fbg_t_points)
print("fbg_b1_data =", fbg_b1_points)

# Extract values and print report table thanks gemini
print(
    f"{'Temp':<12} | {'FBG_T Up (nm)':<14} | {'FBG_T Down (nm)':<15} | {'FBG_B1 Up (nm)':<14} | {'FBG_B1 Down (nm)':<15}")
print("-" * 82)

bars = []  # label, t1, t2, s2_val, s4_val

for temp, bounds in intervals.items():
    row_vals = {'up': (np.nan, np.nan), 'down': (np.nan, np.nan)}

    for phase in ['up', 'down']:
        if bounds[phase] is not None:
            t1, t2 = bounds[phase]
            mask = (t >= t1) & (t <= t2)
            v2 = np.median(s2[mask])
            v4 = np.median(s4[mask]) # Mean would be affected by noise hence median works better imo
            row_vals[phase] = (v2, v4)
            bars.append((f"{temp}°C", t1, t2, v2, v4))

    t_up, b_up = row_vals['up']
    t_dn, b_dn = row_vals['down']

    t_dn_str = f"{t_dn:.6f}" if not np.isnan(t_dn) else "-"
    b_dn_str = f"{b_dn:.6f}" if not np.isnan(b_dn) else "-"

    print(f"Approx. {temp}°C | {t_up:14.6f} | {t_dn_str:<15} | {b_up:14.6f} | {b_dn_str:<15}")

# Plot horizontal lines over the curves
fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

configs = [
    (axes[0], s2, 3, '#ff7f0e', 'S2 (FBG_T - Hotplate)'),
    (axes[1], s4, 4, '#d62728', 'S4 (FBG_B1 - Bimetallic)')
]

for ax, raw, col_idx, color, title in configs:
    ax.plot(t, raw, color=color, alpha=0.5, linewidth=1, label=title)

    for bar in bars:
        label, t1, t2 = bar[0], bar[1], bar[2]
        val = bar[col_idx]
        ax.hlines(val, t1, t2, colors='black', linewidth=2.5)
        ax.annotate(label, (0.5 * (t1 + t2), val), textcoords="offset points",
                    xytext=(0, 7), ha='center', fontsize=8.5, fontweight='bold')

    ax.set_ylabel('Wavelength (nm)')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.ticklabel_format(useOffset=False, style='plain', axis='y')

axes[-1].set_xlim(x_start, x_end)
axes[-1].set_xlabel('Elapsed Time (s)')
plt.tight_layout()
plt.show()