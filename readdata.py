import scipy.io as sio
import numpy as np

datax = sio.loadmat('./Group4_Assignment1/test_strain_x_all.mat')
datay = sio.loadmat('./Group4_Assignment1/test_strain_y_all.mat')
pi = np.loadtxt('./Group4_Assignment1/pi_00.txt')
pj = np.loadtxt('./Group4_Assignment1/pj_00.txt')

print("pi shape:", pi.shape)
print("pj shape:", pj.shape)

print("\npi coordinates:\n", pi)
print("\npj coordinates:\n", pj)

print(datax.keys())
print(datay.keys())

strain_x = datax['strain_x_all']
strain_y = datay['strain_y_all']

print("Type:", type(strain_x))
print("Shape:", strain_x.shape)
print("Dimensions:", strain_x.ndim)
print("Data type:", strain_x.dtype)


print("Type:", type(strain_y))
print("Shape:", strain_y.shape)
print("Dimensions:", strain_y.ndim)
print("Data type:", strain_y.dtype)

