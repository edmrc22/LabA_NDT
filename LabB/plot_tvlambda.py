import numpy as np
import matplotlib.pyplot as plt

fbg_t_data = [(30, 1540.051331), (30, 1540.073578), (40, 1540.118073), (40, 1540.109283), (50, 1540.237), (50, 1540.227661), (60, 1540.346039), (60, 1540.339172), (70, 1540.461945), (70, 1540.455353)]
fbg_b1_data = [(30, 1560.208496), (30, 1560.226624), (40, 1560.295563), (40, 1560.271118), (50, 1560.324127), (50, 1560.273315), (60, 1560.364227), (60, 1560.28952), (70, 1560.372742), (70, 1560.348846)]

average = False

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

datasets = [
    (axes[0], fbg_t_data, 'FBG_T', '#ff7f0e'),
    (axes[1], fbg_b1_data, 'FBG_B1', '#d62728')
]

for ax, data, title, color in datasets:
    arr = np.array(data)
    temps_up = arr[0::2, 0]
    vals_up = arr[0::2, 1]
    vals_down = arr[1::2, 1]

    if average:
        vals_avg = 0.5 * (vals_up + vals_down)
        ax.plot(temps_up, vals_avg, 'o-', color=color, linewidth=2, label='Average (Up & Down)')
    else:
        ax.plot(temps_up, vals_up, 'o-', color=color, linewidth=2, label='Ramp Up')
        ax.plot(temps_up, vals_down, 's--', color='black', linewidth=1.5, label='Ramp Down')

    ax.set_title(title)
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Peak Wavelength λ (nm)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.ticklabel_format(useOffset=False, style='plain', axis='y')

plt.tight_layout()
plt.show()