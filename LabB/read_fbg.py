import csv
import matplotlib.pyplot as plt

filenames = [
    'Wavelength_data_2026_11_27T11_37_07.csv',
    'Wavelength_data_2026_11_27T11_51_07.csv',
    'Wavelength_data_2026_11_27T12_05_08.csv',
    'Wavelength_data_2026_11_27T12_19_08.csv'
]

# Set x-axis start and end in seconds 
x_start = 200
x_end = 2200

time_sec = []
w2, w4 = [], []
t0 = None

for filename in filenames:
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')

        # Skip to numbers
        for _ in range(3):
            next(reader, None)

        for row in reader:
            if not row or len(row) < 12:  # Skip empty lines
                continue

            # Column 1 is packet_ts (microseconds) - convert to elapsed seconds
            ts = float(row[1].strip())
            if t0 is None:
                t0 = ts
            time_sec.append((ts - t0) / 1e6)

            # Columns 9 and 11 are wavelength 2 (S2) and wavelength 4 (S4)
            w2.append(float(row[9].strip()))
            w4.append(float(row[11].strip()))

# Plot
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 6), sharex=True)

signals = [w2, w4]
labels = ['S2', 'S4']
colors = ['#ff7f0e', '#d62728']

for ax, data, label, color in zip(axes, signals, labels, colors):
    ax.plot(time_sec, data, label=label, color=color, linewidth=1)
    ax.set_ylabel('Wavelength (nm)')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.ticklabel_format(useOffset=False, style='plain', axis='y')

axes[-1].set_xlim(left=x_start, right=x_end)
axes[-1].set_xlabel('Elapsed Time (s)')
plt.tight_layout()
plt.show()