import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pylab import rcParams
import os

dirname = os.path.dirname(__file__)

rcParams['axes.xmargin'] = 0
rcParams['axes.ymargin'] = 0.05

# data_cal = np.genfromtxt(os.path.join(dirname, "data_21_07_2022/data.csv"), delimiter=',')
data_cal = np.genfromtxt(os.path.join(dirname, "data_22_07_2022/data.csv"), delimiter=',')
data_no_cal = np.genfromtxt(os.path.join(dirname, "data_21_07_2022/data_no_cal.csv"), delimiter=',')

angles_cal = data_cal[:,2]
angles_no_cal = data_no_cal[:,2]

Rx_PLL_phase_cal = data_cal[:,0]
Rx_PLL_phase_no_cal = data_no_cal[:,0]

Tx_PLL_phase_cal = data_cal[:,1]
Tx_PLL_phase_no_cal = data_no_cal[:,1]

if np.shape(data_cal)[1] == 4 :
    max_pwr_cal = data_cal[:,3]
    print(f"mean received max. power : {np.mean(max_pwr_cal)}")

# Recalculate angles from [-90°, 90°] to [0°,180°]
for i in range(len(angles_cal)):
    if angles_cal[i] > 0 :
        angles_cal[i] = angles_cal[i]
    else :
        angles_cal[i] = angles_cal[i] + 180

for i in range(len(angles_no_cal)):
    if angles_no_cal[i] > 0 :
        angles_no_cal[i] = angles_no_cal[i]
    else :
        angles_no_cal[i] = angles_no_cal[i] + 180

# Statistical properties :
mean_cal = np.round(np.mean(angles_cal), 1)
var_cal = angles_cal.var()
std_cal = np.round(angles_cal.std(), 1)


print(f"mean max. power angle : {mean_cal}°")

# FIG #1
bins = np.linspace(0, 180,180)
kwargs = dict(alpha=0.6, bins = bins)

fig = plt.figure()
plt.hist(angles_no_cal, **kwargs, color="orange", label="Without calibration")
plt.hist(angles_cal, **kwargs, color="dodgerblue", label="With Tx/Rx calibration")
plt.axvline(mean_cal, color="dodgerblue", linestyle='dashed', label=f"Mean calibrated= {mean_cal}°")
plt.axvline(mean_cal-std_cal, color="dodgerblue", linestyle='dotted', label=f"Std. dev. calibrated= {std_cal}°")
plt.axvline(mean_cal+std_cal, color="dodgerblue", linestyle='dotted')
plt.legend(loc='upper right');plt.xlabel("Angles (°)");plt.ylabel("Occurences")
fig.suptitle("Angles of Maximum power (data)", fontsize=12)

# FIG #2
bins = np.linspace(-180,180,180)
kwargs = dict(alpha=0.6, bins = bins)

fig, ax = plt.subplots(2, sharex=True)
ax[0].hist(Rx_PLL_phase_cal, **kwargs, color="green", label="Rx PLLs phase shift")
ax[0].legend(loc='upper right')
ax[0].axhline(7, linestyle='dashed' , color="green")
ax[0].set_ylabel("Occurences")
ax[1].hist(Tx_PLL_phase_cal, **kwargs, color="red", label="Tx PLLs phase shift")
ax[1].legend(loc='upper right')
ax[1].set_xlabel("Phase shift (°)")
ax[1].set_ylabel("Occurences")
fig.suptitle("PLLs phase differences (data)", fontsize=12)

# # FIG #3
# fig, ax = plt.subplots(2, sharex=True)
# ax[0].plot(max_pwr_cal)
# fig.suptitle("PLLs phase differences (data)", fontsize=12)

plt.show()