import scipy.io as sio
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import os

data_directory = "./Group4_Assignment1"
datax    = sio.loadmat(os.path.join(data_directory, 'test_strain_x_all.mat'))
datay    = sio.loadmat(os.path.join(data_directory, 'test_strain_y_all.mat'))
datacorr = sio.loadmat(os.path.join(data_directory, 'test_cc_max.mat'))
pi = np.loadtxt(os.path.join(data_directory, 'pi_00.txt'))
pj = np.loadtxt(os.path.join(data_directory, 'pj_00.txt'))

strain_x     = datax['strain_x_all']    # (7, 53, 5)
strain_y     = datay['strain_y_all']    # (6, 54, 5)
correlations = datacorr['cc_max']       # (7, 54, 5)

x = pi[:, 0]   # 7 values: short direction
y = pj[0, :]   # 54 values: long direction
x_mid = 0.5 * (x[:-1] + x[1:])   # 6 midpoints
y_mid = 0.5 * (y[:-1] + y[1:])   # 53 midpoints

corr_strain_x = 0.5 * (correlations[:, :-1, :] + correlations[:, 1:, :])  # (7, 53, 5)
corr_strain_y = 0.5 * (correlations[:-1, :, :] + correlations[1:, :, :])  # (6, 54, 5)

refine = 10 

xi = np.linspace(y_mid[0], y_mid[-1], refine * len(y_mid))   # 53×4 = 212 pts
yi = np.linspace(x[0],     x[-1],     refine * len(x))        # 7×4  = 28 pts
N_X, N_Y = len(xi), len(yi)
Xi, Yi   = np.meshgrid(xi, yi)

Ynod, Xmid = np.meshgrid(y_mid, x)    # (7, 53)
Ymid, Xnod = np.meshgrid(y,   x_mid)  # (6, 54)

THRESHOLD    = 0.9
USE_CORR_MASK = True

strain_x_fine = np.full((5, N_Y, N_X), np.nan)
strain_y_fine = np.full((5, N_Y, N_X), np.nan)

for i in range(5):
    vals = strain_x[:, :, i].ravel()
    good = (corr_strain_x[:, :, i].ravel() >= THRESHOLD) if USE_CORR_MASK \
           else np.ones(len(vals), dtype=bool)
    strain_x_fine[i] = griddata(
            np.column_stack([Ynod.ravel(), Xmid.ravel()])[good],
            vals[good], (Xi, Yi), method='linear')

    vals = strain_y[:, :, i].ravel()
    good = (corr_strain_y[:, :, i].ravel() >= THRESHOLD) if USE_CORR_MASK \
           else np.ones(len(vals), dtype=bool)
    strain_y_fine[i] = griddata(
            np.column_stack([Ymid.ravel(), Xnod.ravel()])[good],
            vals[good], (Xi, Yi), method='linear')

strain_x_fine *= 1e6
strain_y_fine *= 1e6

exx_vmin, exx_vmax = np.nanmin(strain_x_fine), np.nanmax(strain_x_fine)
eyy_vmin, eyy_vmax = np.nanmin(strain_y_fine), np.nanmax(strain_y_fine)


mask_label = f'correlation mask ≥ {THRESHOLD}' if USE_CORR_MASK else 'no correlation mask'

fig_x, axes_x = plt.subplots(5, 1, figsize=(10, 12), constrained_layout=True)
fig_y, axes_y = plt.subplots(5, 1, figsize=(10, 12), constrained_layout=True)

kw_exx = dict(origin='lower', aspect='auto', cmap='inferno',
              extent=[y[0], y[-1], x[0], x[-1]],
              vmin=exx_vmin, vmax=exx_vmax)
kw_eyy = {**kw_exx, 'vmin': eyy_vmin, 'vmax': eyy_vmax}

for i in range(5):
    im0 = axes_x[i].imshow(strain_x_fine[i], **kw_exx)
    axes_x[i].set_title(f'Frame {i + 1}')
    axes_x[i].set_xlim(y[0], y[-1])
    axes_x[i].set_ylim(x[0], x[-1])
    axes_x[i].xaxis.set_major_locator(ticker.MultipleLocator(500))
    axes_x[i].yaxis.set_major_locator(ticker.MultipleLocator(50))

im1 = None
for i in range(5):
    im1 = axes_y[i].imshow(strain_y_fine[i], **kw_eyy)
    axes_y[i].set_title(f'Frame {i + 1}')
    axes_y[i].set_xlim(y[0], y[-1])
    axes_y[i].set_ylim(x[0], x[-1])
    axes_y[i].xaxis.set_major_locator(ticker.MultipleLocator(500))
    axes_y[i].yaxis.set_major_locator(ticker.MultipleLocator(50))

axes_x[-1].set_xlabel('$y$ (px)')
axes_y[-1].set_xlabel('$y$ (px)')

fig_x.colorbar(im0, ax=axes_x, shrink=0.6, label=r'$\varepsilon_{xx}$ (με)')
fig_y.colorbar(im1, ax=axes_y, shrink=0.6, label=r'$\varepsilon_{yy}$ (με)')
fig_x.suptitle(r'$\varepsilon_{xx}$ — DIC strain fields (' + mask_label + ')', fontsize=13)
fig_y.suptitle(r'$\varepsilon_{yy}$ — DIC strain fields (' + mask_label + ')', fontsize=13)
plt.show()